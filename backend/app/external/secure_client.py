from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid
from backend.app.audit.audit_logger import audit_logger, SecurityEventType
from backend.app.core.config import settings
from backend.app.external.challenge_response import generate_client_hmac_proof
from backend.app.external.models import SecureDataPacket, ExternalFetchResponse
from backend.app.external.packet_verifier import verify_packet_security
from backend.app.ingestion.engine import ingestion_engine
from backend.app.ingestion.envelope import create_envelope
from mock_official_system.provider import mock_provider

class SecureExternalClient:
    """
    Secure client orchestrating zero-trust external data integration:
    - Fresh nonce-based challenge response
    - HMAC-SHA-256 verification
    - Ed25519 digital signature verification
    - SHA-256 evidence integrity
    - Provenance preservation & automated ingestion
    - Tamper-evident audit logging
    """
    def __init__(
        self,
        client_id: str = settings.OFFICIAL_PROVIDER_CLIENT_ID,
        shared_secret: str = settings.OFFICIAL_PROVIDER_SHARED_SECRET
    ):
        self.client_id = client_id
        self.shared_secret = shared_secret

    def fetch_verified_external_data(
        self,
        resource_id: str,
        provider_type: str,
        case_id: str,
        user_badge: str = "DL-INV-301",
        user_id: str = "USR-INV-001"
    ) -> ExternalFetchResponse:
        request_id = f"REQ-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        # 1. Audit Log: External Request Initiated
        audit_logger.log(
            event_type=SecurityEventType.EXTERNAL_DATA_REQUEST,
            operation="FETCH_EXTERNAL_DATA",
            status="INITIATED",
            user_id=user_id,
            case_id=case_id,
            request_id=request_id,
            details={"resource_id": resource_id, "provider_type": provider_type}
        )

        # 2. Request Challenge Nonce from Provider
        challenge_res = mock_provider.request_challenge(
            client_id=self.client_id,
            request_id=request_id,
            resource=resource_id
        )
        nonce = challenge_res["nonce"]
        req_timestamp = datetime.now(timezone.utc).isoformat()

        audit_logger.log(
            event_type=SecurityEventType.CHALLENGE_ISSUED,
            operation="CHALLENGE_HANDSHAKE",
            status="ISSUED",
            user_id=user_id,
            case_id=case_id,
            request_id=request_id,
            details={"challenge_id": challenge_res["challenge_id"]}
        )

        # 3. Compute Client HMAC-SHA-256 Proof
        hmac_proof = generate_client_hmac_proof(
            client_id=self.client_id,
            request_id=request_id,
            nonce=nonce,
            timestamp=req_timestamp,
            resource=resource_id,
            shared_secret=self.shared_secret
        )

        # 4. Fetch Secure Packet from Provider with HMAC proof
        try:
            raw_packet = mock_provider.fetch_data(
                client_id=self.client_id,
                request_id=request_id,
                nonce=nonce,
                timestamp=req_timestamp,
                resource=resource_id,
                hmac_proof=hmac_proof
            )
        except Exception as e:
            audit_logger.log(
                event_type=SecurityEventType.CHALLENGE_REJECTED,
                operation="EXTERNAL_DATA_FETCH",
                status="FAILED",
                user_id=user_id,
                case_id=case_id,
                request_id=request_id,
                details={"error": str(e)}
            )
            raise PermissionError(f"Official provider rejected challenge: {e}")

        # 5. Parse and Validate Packet Schema
        packet = SecureDataPacket(**raw_packet)

        audit_logger.log(
            event_type=SecurityEventType.PACKET_RECEIVED,
            operation="RECEIVE_SECURE_PACKET",
            status="SUCCESS",
            user_id=user_id,
            case_id=case_id,
            request_id=request_id,
            packet_id=packet.packet_id,
            source_system=packet.source_system
        )

        # 6. Verify Digital Signature & SHA-256 Integrity
        is_valid, reason = verify_packet_security(packet)
        if not is_valid:
            audit_logger.log(
                event_type=SecurityEventType.PACKET_VALIDATION_FAILED,
                operation="VERIFY_PACKET_INTEGRITY",
                status="FAILED",
                user_id=user_id,
                case_id=case_id,
                request_id=request_id,
                packet_id=packet.packet_id,
                details={"reason": reason}
            )
            raise ValueError(f"Packet verification failed: {reason}")

        audit_logger.log(
            event_type=SecurityEventType.PACKET_SIGNATURE_VERIFIED,
            operation="VERIFY_SIGNATURE",
            status="SUCCESS",
            user_id=user_id,
            case_id=case_id,
            request_id=request_id,
            packet_id=packet.packet_id
        )

        audit_logger.log(
            event_type=SecurityEventType.EVIDENCE_INTEGRITY_VERIFIED,
            operation="VERIFY_INTEGRITY",
            status="SUCCESS",
            user_id=user_id,
            case_id=case_id,
            request_id=request_id,
            packet_id=packet.packet_id,
            details={"sha256": packet.integrity.hash}
        )

        # 7. Preserve Raw Provenance & Feed into Ingestion Pipeline
        prov_envelope = create_envelope(
            source_type=provider_type,
            raw_content={
                "external_packet_id": packet.packet_id,
                "external_request_id": packet.request_id,
                "source_system": packet.source_system,
                "retrieval_timestamp": packet.created_at,
                "verified_signature": packet.signature.value,
                "raw_payload": packet.data
            },
            badge_id=user_badge,
            record_id=f"REC-EXT-{packet.packet_id}"
        )

        # Ingest into normalized knowledge graph
        ingestion_engine.ingest_envelope(prov_envelope)

        audit_logger.log(
            event_type=SecurityEventType.DATA_INGESTED,
            operation="INGEST_VERIFIED_DATA",
            status="SUCCESS",
            user_id=user_id,
            case_id=case_id,
            request_id=request_id,
            packet_id=packet.packet_id,
            details={"record_id": prov_envelope["record_id"]}
        )

        return ExternalFetchResponse(
            status="VERIFIED_AND_INGESTED",
            packet_id=packet.packet_id,
            request_id=packet.request_id,
            source_system=packet.source_system,
            verified_integrity=True,
            verified_signature=True,
            provenance_record_id=prov_envelope["record_id"],
            data=packet.data
        )

secure_external_client = SecureExternalClient()
