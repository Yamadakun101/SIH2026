from datetime import timedelta
import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.auth.jwt import create_access_token
from backend.app.main import app

@pytest.mark.anyio
async def test_valid_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {"username": "investigator", "password": "Investigator@2026"}
        res = await ac.post("/api/v1/auth/login", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "investigator"
    assert data["role"] == "INVESTIGATOR"

@pytest.mark.anyio
async def test_invalid_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Wrong password
        res = await ac.post("/api/v1/auth/login", json={"username": "investigator", "password": "WrongPassword!"})
        assert res.status_code == 401
        assert "Invalid credentials" in res.json()["detail"]

        # Unknown user
        res_unk = await ac.post("/api/v1/auth/login", json={"username": "hacker", "password": "AnyPassword"})
        assert res_unk.status_code == 401

@pytest.mark.anyio
async def test_expired_jwt():
    # Create an already expired token (negative delta)
    expired_token = create_access_token(
        {"sub": "USR-INV-001", "username": "investigator", "role": "INVESTIGATOR"},
        expires_delta=timedelta(seconds=-10)
    )
    headers = {"Authorization": f"Bearer {expired_token}"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/auth/me", headers=headers)
    assert res.status_code == 401
    assert "expired" in res.json()["detail"].lower()

@pytest.mark.anyio
async def test_malformed_jwt():
    headers = {"Authorization": "Bearer not.a.valid.jwt.token"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/auth/me", headers=headers)
    assert res.status_code == 401
    assert "invalid" in res.json()["detail"].lower()

@pytest.mark.anyio
async def test_me_endpoint_with_valid_token():
    valid_token = create_access_token(
        {"sub": "USR-INV-001", "username": "investigator", "role": "INVESTIGATOR"}
    )
    headers = {"Authorization": f"Bearer {valid_token}"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/auth/me", headers=headers)
    assert res.status_code == 200
    user = res.json()
    assert user["username"] == "investigator"
    assert user["badge_number"] == "DL-INV-301"
    assert "DL-2026-0412" in user["assigned_cases"]
