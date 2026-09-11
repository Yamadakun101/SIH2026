from datetime import datetime, timezone
import secrets
import time
from typing import Dict, Optional
import uuid

class ChallengeRecord:
    def __init__(self, challenge_id: str, client_id: str, request_id: str, resource: str, nonce: str, expires_at: float):
        self.challenge_id = challenge_id
        self.client_id = client_id
        self.request_id = request_id
        self.resource = resource
        self.nonce = nonce
        self.created_at = time.time()
        self.expires_at = expires_at
        self.status = "ISSUED"

class ChallengeManager:
    """Issues and tracks cryptographic nonces for challenge-response authentication."""
    def __init__(self, default_validity_seconds: int = 120):
        self._challenges: Dict[str, ChallengeRecord] = {}  # nonce -> ChallengeRecord
        self.default_validity_seconds = default_validity_seconds

    def issue_challenge(self, client_id: str, request_id: str, resource: str, validity_seconds: Optional[int] = None) -> Dict[str, str]:
        validity = validity_seconds or self.default_validity_seconds
        nonce = secrets.token_hex(16)
        challenge_id = f"CHAL-{uuid.uuid4().hex[:8].upper()}"
        expires_at = time.time() + validity

        record = ChallengeRecord(
            challenge_id=challenge_id,
            client_id=client_id,
            request_id=request_id,
            resource=resource,
            nonce=nonce,
            expires_at=expires_at
        )
        self._challenges[nonce] = record

        return {
            "challenge_id": challenge_id,
            "nonce": nonce,
            "client_id": client_id,
            "request_id": request_id,
            "resource": resource,
            "expires_in_seconds": validity,
            "issued_at": datetime.now(timezone.utc).isoformat()
        }

    def get_challenge(self, nonce: str) -> Optional[ChallengeRecord]:
        return self._challenges.get(nonce)

    def validate_nonce(self, nonce: str) -> bool:
        """Returns True if nonce exists, is ISSUED, and has not expired."""
        rec = self._challenges.get(nonce)
        if not rec:
            return False
        if rec.status != "ISSUED":
            return False
        if time.time() > rec.expires_at:
            rec.status = "EXPIRED"
            return False
        return True

    def consume_nonce(self, nonce: str):
        if nonce in self._challenges:
            self._challenges[nonce].status = "CONSUMED"

    def reset(self):
        self._challenges.clear()

challenge_manager = ChallengeManager()
