from datetime import datetime, timezone
from typing import Any, Dict
import uuid
from backend.app.ingestion.envelope import compute_sha256
from mock_official_system.keys import get_provider_public_key_hex
from mock_official_system.signer import sign_data_hash

def generate_secure_packet(
    request_id: str,
    source_system: str,
    data: Dict[str, Any],
    packet_id: str = None
) -> Dict[str, Any]:
    """
    Creates an authenticated, tamper-evident Secure Data Packet
    containing a SHA-256 data digest and an Ed25519 digital signature.
    """
    if not packet_id:
        packet_id = f"PKT-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    created_at = datetime.now(timezone.utc).isoformat()
    data_hash = compute_sha256(data)
    signature_hex = sign_data_hash(data_hash)
    public_key_hex = get_provider_public_key_hex()

    return {
        "packet_id": packet_id,
        "request_id": request_id,
        "source_system": source_system,
        "schema_version": "1.0",
        "created_at": created_at,
        "data": data,
        "integrity": {
            "algorithm": "SHA-256",
            "hash": data_hash
        },
        "signature": {
            "algorithm": "Ed25519",
            "public_key_hex": public_key_hex,
            "value": signature_hex
        }
    }
