import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.auth.jwt import create_access_token
from backend.app.main import app

@pytest.mark.anyio
async def test_role_based_access_control():
    # 1. Investigator trying to access Supervisor/Admin audit route -> 403
    inv_token = create_access_token({"sub": "USR-INV-001", "username": "investigator", "role": "INVESTIGATOR"})
    inv_headers = {"Authorization": f"Bearer {inv_token}"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_inv = await ac.get("/api/v1/audit/security", headers=inv_headers)
    assert res_inv.status_code == 403
    assert "insufficient role permissions" in res_inv.json()["detail"].lower()

    # 2. Supervisor accessing audit route -> 200
    sup_token = create_access_token({"sub": "USR-SUP-001", "username": "supervisor", "role": "SUPERVISOR"})
    sup_headers = {"Authorization": f"Bearer {sup_token}"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_sup = await ac.get("/api/v1/audit/security", headers=sup_headers)
    assert res_sup.status_code == 200
    assert isinstance(res_sup.json(), list)

    # 3. Admin accessing audit route -> 200
    adm_token = create_access_token({"sub": "USR-ADM-001", "username": "admin", "role": "ADMIN"})
    adm_headers = {"Authorization": f"Bearer {adm_token}"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_adm = await ac.get("/api/v1/audit/security", headers=adm_headers)
    assert res_adm.status_code == 200

@pytest.mark.anyio
async def test_case_level_authorization():
    inv_token = create_access_token({"sub": "USR-INV-001", "username": "investigator", "role": "INVESTIGATOR"})
    inv_headers = {"Authorization": f"Bearer {inv_token}"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Investigator requesting data for an unauthorized case (MH-2026-9999) -> 403
        unauth_payload = {
            "provider_type": "VEHICLE",
            "resource_id": "VEHICLE:DL-01-AB-9921",
            "case_id": "MH-2026-9999"
        }
        res_denied = await ac.post("/api/v1/external/fetch", json=unauth_payload, headers=inv_headers)
        assert res_denied.status_code == 403
        assert "not authorized" in res_denied.json()["detail"].lower()

        # Investigator requesting data for an authorized case (DL-2026-0412) -> 200
        auth_payload = {
            "provider_type": "VEHICLE",
            "resource_id": "VEHICLE:DL-01-AB-9921",
            "case_id": "DL-2026-0412"
        }
        res_allowed = await ac.post("/api/v1/external/fetch", json=auth_payload, headers=inv_headers)
        assert res_allowed.status_code == 200
        assert res_allowed.json()["status"] == "VERIFIED_AND_INGESTED"
