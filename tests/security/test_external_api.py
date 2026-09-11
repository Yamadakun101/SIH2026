import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.auth.jwt import create_access_token
from backend.app.main import app
from mock_official_system.challenge import challenge_manager
from mock_official_system.replay_protection import replay_tracker

@pytest.fixture(autouse=True)
def clean_mock_state():
    challenge_manager.reset()
    replay_tracker.reset()
    yield
    challenge_manager.reset()
    replay_tracker.reset()

@pytest.mark.anyio
async def test_get_external_providers():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/external/providers")
    assert res.status_code == 200
    providers = res.json()
    assert len(providers) >= 4
    names = [p["provider_id"] for p in providers]
    assert "DOT_OFFICIAL_CDR_GATEWAY" in names
    assert "VAHAN_NATIONAL_REGISTRY" in names

@pytest.mark.anyio
async def test_successful_external_fetch_and_ingestion():
    token = create_access_token(
        {"sub": "USR-INV-001", "username": "investigator", "role": "INVESTIGATOR"}
    )
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "provider_type": "CDR",
        "resource_id": "CDR:DL-2026-0412",
        "case_id": "DL-2026-0412"
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/external/fetch", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "VERIFIED_AND_INGESTED"
    assert data["verified_integrity"] is True
    assert data["verified_signature"] is True
    assert data["packet_id"].startswith("PKT-")
    assert "records" in data["data"]

@pytest.mark.anyio
async def test_unauthenticated_external_fetch_blocked():
    payload = {
        "provider_type": "CDR",
        "resource_id": "CDR:DL-2026-0412",
        "case_id": "DL-2026-0412"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/external/fetch", json=payload)
    assert res.status_code == 401
