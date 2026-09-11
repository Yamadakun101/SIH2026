from datetime import datetime, timezone
import time
import pytest
from backend.app.core.config import settings
from backend.app.external.challenge_response import generate_client_hmac_proof
from mock_official_system.authentication import verify_challenge_proof
from mock_official_system.challenge import challenge_manager
from mock_official_system.replay_protection import replay_tracker

@pytest.fixture(autouse=True)
def reset_security_trackers():
    challenge_manager.reset()
    replay_tracker.reset()
    yield
    challenge_manager.reset()
    replay_tracker.reset()

def test_valid_challenge_handshake():
    client_id = settings.OFFICIAL_PROVIDER_CLIENT_ID
    request_id = "REQ-TEST-001"
    resource = "VEHICLE:DL-01-AB-9921"
    timestamp = datetime.now(timezone.utc).isoformat()

    # 1. Issue challenge
    challenge = challenge_manager.issue_challenge(client_id, request_id, resource)
    nonce = challenge["nonce"]

    # 2. Compute valid HMAC proof
    hmac_proof = generate_client_hmac_proof(
        client_id, request_id, nonce, timestamp, resource, settings.OFFICIAL_PROVIDER_SHARED_SECRET
    )

    # 3. Verify
    is_valid, reason = verify_challenge_proof(
        client_id, request_id, nonce, timestamp, resource, hmac_proof
    )
    assert is_valid is True
    assert reason == "Verified"

def test_replay_attack_rejected():
    client_id = settings.OFFICIAL_PROVIDER_CLIENT_ID
    request_id = "REQ-TEST-REPLAY"
    resource = "CDR:DL-2026-0412"
    timestamp = datetime.now(timezone.utc).isoformat()

    challenge = challenge_manager.issue_challenge(client_id, request_id, resource)
    nonce = challenge["nonce"]
    hmac_proof = generate_client_hmac_proof(
        client_id, request_id, nonce, timestamp, resource, settings.OFFICIAL_PROVIDER_SHARED_SECRET
    )

    # First attempt: succeeds
    is_valid_1, _ = verify_challenge_proof(client_id, request_id, nonce, timestamp, resource, hmac_proof)
    assert is_valid_1 is True

    # Second attempt (Replay): must fail
    is_valid_2, reason_2 = verify_challenge_proof(client_id, request_id, nonce, timestamp, resource, hmac_proof)
    assert is_valid_2 is False
    assert "replay" in reason_2.lower()

def test_tampered_request_id_rejected():
    client_id = settings.OFFICIAL_PROVIDER_CLIENT_ID
    request_id = "REQ-ORIGINAL"
    resource = "BANK:HDFC-4091"
    timestamp = datetime.now(timezone.utc).isoformat()

    challenge = challenge_manager.issue_challenge(client_id, request_id, resource)
    nonce = challenge["nonce"]
    hmac_proof = generate_client_hmac_proof(
        client_id, request_id, nonce, timestamp, resource, settings.OFFICIAL_PROVIDER_SHARED_SECRET
    )

    # Submit with modified request_id
    is_valid, reason = verify_challenge_proof(
        client_id, "REQ-TAMPERED", nonce, timestamp, resource, hmac_proof
    )
    assert is_valid is False
    assert "request id does not match" in reason.lower()

def test_tampered_nonce_rejected():
    client_id = settings.OFFICIAL_PROVIDER_CLIENT_ID
    request_id = "REQ-NONCE-TEST"
    resource = "VEHICLE:DL-01-AB-9921"
    timestamp = datetime.now(timezone.utc).isoformat()

    challenge_manager.issue_challenge(client_id, request_id, resource)
    fake_nonce = "0123456789abcdef0123456789abcdef"
    hmac_proof = generate_client_hmac_proof(
        client_id, request_id, fake_nonce, timestamp, resource, settings.OFFICIAL_PROVIDER_SHARED_SECRET
    )

    is_valid, reason = verify_challenge_proof(
        client_id, request_id, fake_nonce, timestamp, resource, hmac_proof
    )
    assert is_valid is False
    assert "invalid or expired" in reason.lower()

def test_tampered_resource_rejected():
    client_id = settings.OFFICIAL_PROVIDER_CLIENT_ID
    request_id = "REQ-RES-TEST"
    resource = "CDR:DL-2026-0412"
    timestamp = datetime.now(timezone.utc).isoformat()

    challenge = challenge_manager.issue_challenge(client_id, request_id, resource)
    nonce = challenge["nonce"]
    hmac_proof = generate_client_hmac_proof(
        client_id, request_id, nonce, timestamp, resource, settings.OFFICIAL_PROVIDER_SHARED_SECRET
    )

    # Submit requesting a different unauthorized resource
    is_valid, reason = verify_challenge_proof(
        client_id, request_id, nonce, timestamp, "BANK:UNAUTHORIZED-999", hmac_proof
    )
    assert is_valid is False
    assert "requested resource does not match" in reason.lower()

def test_invalid_hmac_rejected():
    client_id = settings.OFFICIAL_PROVIDER_CLIENT_ID
    request_id = "REQ-HMAC-TEST"
    resource = "VEHICLE:DL-01-AB-9921"
    timestamp = datetime.now(timezone.utc).isoformat()

    challenge = challenge_manager.issue_challenge(client_id, request_id, resource)
    nonce = challenge["nonce"]

    # Submit invalid HMAC string
    is_valid, reason = verify_challenge_proof(
        client_id, request_id, nonce, timestamp, resource, "deadbeefcafebabe12345678"
    )
    assert is_valid is False
    assert "hmac signature verification failed" in reason.lower()

def test_expired_challenge_rejected():
    client_id = settings.OFFICIAL_PROVIDER_CLIENT_ID
    request_id = "REQ-EXP-TEST"
    resource = "VEHICLE:DL-01-AB-9921"
    timestamp = datetime.now(timezone.utc).isoformat()

    # Issue challenge with 0 second validity
    challenge = challenge_manager.issue_challenge(client_id, request_id, resource, validity_seconds=-1)
    nonce = challenge["nonce"]
    hmac_proof = generate_client_hmac_proof(
        client_id, request_id, nonce, timestamp, resource, settings.OFFICIAL_PROVIDER_SHARED_SECRET
    )

    is_valid, reason = verify_challenge_proof(
        client_id, request_id, nonce, timestamp, resource, hmac_proof
    )
    assert is_valid is False
    assert "invalid or expired" in reason.lower()
