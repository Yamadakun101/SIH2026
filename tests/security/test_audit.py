import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.audit.audit_logger import audit_logger, SecurityEventType
from backend.app.auth.jwt import create_access_token
from backend.app.main import app

def test_audit_logger_sanitizes_secrets():
    audit_logger.clear()
    event = audit_logger.log(
        event_type=SecurityEventType.LOGIN_SUCCESS,
        operation="TEST_OP",
        status="SUCCESS",
        user_id="USR-001",
        details={
            "safe_field": "123",
            "password": "SuperSecretPassword!",
            "api_secret": "my-secret-key",
            "private_key": "private_data"
        }
    )
    assert event.details.get("safe_field") == "123"
    assert "password" not in event.details
    assert "api_secret" not in event.details
    assert "private_key" not in event.details

@pytest.mark.anyio
async def test_failed_login_creates_audit_event():
    audit_logger.clear()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post("/api/v1/auth/login", json={"username": "investigator", "password": "WrongPassword"})

    events = audit_logger.get_events(event_type=SecurityEventType.LOGIN_FAILED)
    assert len(events) >= 1
    assert events[0].details["username"] == "investigator"
    assert events[0].status == "FAILED"

@pytest.mark.anyio
async def test_external_fetch_creates_full_audit_trail():
    audit_logger.clear()
    token = create_access_token(
        {"sub": "USR-INV-001", "username": "investigator", "role": "INVESTIGATOR"}
    )
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "provider_type": "VEHICLE",
        "resource_id": "VEHICLE:DL-01-AB-9921",
        "case_id": "DL-2026-0412"
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/external/fetch", json=payload, headers=headers)
    assert res.status_code == 200

    all_events = [e.event_type for e in audit_logger.get_events(limit=20)]
    assert SecurityEventType.EXTERNAL_DATA_REQUEST in all_events
    assert SecurityEventType.CHALLENGE_ISSUED in all_events
    assert SecurityEventType.PACKET_RECEIVED in all_events
    assert SecurityEventType.PACKET_SIGNATURE_VERIFIED in all_events
    assert SecurityEventType.EVIDENCE_INTEGRITY_VERIFIED in all_events
    assert SecurityEventType.DATA_INGESTED in all_events
