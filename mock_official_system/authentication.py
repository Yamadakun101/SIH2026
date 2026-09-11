from datetime import datetime, timezone
import hashlib
import hmac
import time
from typing import Tuple
from backend.app.core.config import settings
from mock_official_system.challenge import challenge_manager
from mock_official_system.replay_protection import replay_tracker

def build_canonical_message(client_id: str, request_id: str, nonce: str, timestamp: str, resource: str) -> str:
    """Builds standard canonical string for challenge HMAC proof."""
    return f"{client_id}:{request_id}:{nonce}:{timestamp}:{resource}"

def compute_hmac(shared_secret: str, canonical_message: str) -> str:
    """Computes HMAC-SHA-256 over canonical message."""
    return hmac.new(
        shared_secret.encode("utf-8"),
        canonical_message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def verify_challenge_proof(
    client_id: str,
    request_id: str,
    nonce: str,
    timestamp: str,
    resource: str,
    submitted_hmac: str,
    shared_secret: str = settings.OFFICIAL_PROVIDER_SHARED_SECRET,
    allowed_clock_skew_seconds: int = 300
) -> Tuple[bool, str]:
    """
    Verifies the client's HMAC challenge proof with replay and expiration protections.
    Returns (is_valid, reason).
    """
    # 1. Replay Check
    if replay_tracker.is_replayed(request_id, nonce):
        return False, "Replay attack detected: nonce or request ID has already been consumed"

    # 2. Challenge Existence and Expiration Check
    if not challenge_manager.validate_nonce(nonce):
        return False, "Invalid or expired challenge nonce"

    challenge_record = challenge_manager.get_challenge(nonce)
    if not challenge_record:
        return False, "Challenge not found"

    # 3. Match Request and Resource to Issued Challenge
    if challenge_record.client_id != client_id:
        return False, "Client ID does not match issued challenge"
    if challenge_record.request_id != request_id:
        return False, "Request ID does not match issued challenge"
    if challenge_record.resource != resource:
        return False, "Requested resource does not match issued challenge"

    # 4. Timestamp Freshness Window Check
    try:
        ts_clean = timestamp.replace("Z", "+00:00") if timestamp.endswith("Z") else timestamp
        dt = datetime.fromisoformat(ts_clean)
        req_epoch = dt.timestamp()
        now_epoch = time.time()
        if abs(now_epoch - req_epoch) > allowed_clock_skew_seconds:
            return False, "Timestamp is outside the allowed freshness window"
    except Exception:
        return False, "Malformed timestamp format"

    # 5. Compute Expected HMAC
    canonical_msg = build_canonical_message(client_id, request_id, nonce, timestamp, resource)
    expected_hmac = compute_hmac(shared_secret, canonical_msg)

    # 6. Constant-time Comparison
    if not hmac.compare_digest(expected_hmac, submitted_hmac):
        return False, "HMAC signature verification failed"

    # 7. Consume Nonce and Mark Replay Tracker
    challenge_manager.consume_nonce(nonce)
    replay_tracker.mark_consumed(request_id, nonce)

    return True, "Verified"
