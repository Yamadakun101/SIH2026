import json
from pathlib import Path
from typing import Any, Dict
from mock_official_system.authentication import verify_challenge_proof
from mock_official_system.challenge import challenge_manager
from mock_official_system.packet_generator import generate_secure_packet

class MockOfficialProviderService:
    """
    Simulated government API provider gateway (e.g. DoT, Vahan, FIU, NHAI).
    Enforces cryptographic challenge-response authentication, single-use nonces,
    and returns digitally signed data packets.
    """
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self._datasets: Dict[str, Dict[str, Any]] = {}
        self._load_datasets()

    def _load_datasets(self):
        for name in ["cdr", "vehicles", "banking", "cctv"]:
            path = self.data_dir / f"{name}.json"
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self._datasets.update(json.load(f))

    def request_challenge(self, client_id: str, request_id: str, resource: str) -> Dict[str, Any]:
        """Step 1: Client requests challenge; Provider generates fresh nonce."""
        return challenge_manager.issue_challenge(client_id, request_id, resource)

    def fetch_data(
        self,
        client_id: str,
        request_id: str,
        nonce: str,
        timestamp: str,
        resource: str,
        hmac_proof: str
    ) -> Dict[str, Any]:
        """
        Step 2: Client presents HMAC proof.
        Provider verifies proof, checks replay, creates digitally signed packet.
        """
        is_valid, reason = verify_challenge_proof(
            client_id=client_id,
            request_id=request_id,
            nonce=nonce,
            timestamp=timestamp,
            resource=resource,
            submitted_hmac=hmac_proof
        )

        if not is_valid:
            raise PermissionError(f"External authentication failed: {reason}")

        # Fetch resource
        data = self._datasets.get(resource)
        if not data:
            # Fallback synthetic generic for testing arbitrary resource requests
            data = {
                "source_system": "MOCK_NATIONAL_CRIME_INTELLIGENCE",
                "resource_requested": resource,
                "status": "RECORD_LOCATED",
                "extracted_fields": {"case_id": "DL-2026-0412", "confidence": 0.94}
            }

        source_system = data.get("source_system", "MOCK_OFFICIAL_PROVIDER")
        packet = generate_secure_packet(
            request_id=request_id,
            source_system=source_system,
            data=data
        )
        return packet

mock_provider = MockOfficialProviderService()
