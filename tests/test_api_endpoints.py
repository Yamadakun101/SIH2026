import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.main import app

@pytest.mark.anyio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["service"] == "KavachNet"

@pytest.mark.anyio
async def test_get_states():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/states")
    assert response.status_code == 200
    states = response.json()
    assert isinstance(states, list)
    assert len(states) >= 1
    dl_state = next((s for s in states if s["state_code"] == "DL"), None)
    assert dl_state is not None
    assert dl_state["state_name"] == "Delhi"
    assert dl_state["active_cases_count"] >= 1

@pytest.mark.anyio
async def test_get_cases_and_filter():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # All cases
        res_all = await ac.get("/api/v1/cases")
        assert res_all.status_code == 200
        cases = res_all.json()
        assert len(cases) >= 1
        assert cases[0]["case_id"] == "DL-2026-0412"

        # Filter by state=DL
        res_dl = await ac.get("/api/v1/cases?state=DL")
        assert res_dl.status_code == 200
        assert len(res_dl.json()) >= 1

        # Filter by non-existent state
        res_none = await ac.get("/api/v1/cases?state=ZZ")
        assert res_none.status_code == 200
        assert len(res_none.json()) == 0

@pytest.mark.anyio
async def test_get_single_case():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/cases/DL-2026-0412")
        assert res.status_code == 200
        case = res.json()
        assert case["case_id"] == "DL-2026-0412"
        assert "fir_number" in case
        assert case["priority"] == "CRITICAL"

        # Not found
        res_404 = await ac.get("/api/v1/cases/NON-EXISTENT")
        assert res_404.status_code == 404

@pytest.mark.anyio
async def test_get_case_graph():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/cases/DL-2026-0412/graph")
        assert res.status_code == 200
        graph = res.json()
        assert graph["case_id"] == "DL-2026-0412"
        assert "elements" in graph
        nodes = graph["elements"]["nodes"]
        edges = graph["elements"]["edges"]
        
        # Verify Cytoscape format: nodes and edges have nested 'data'
        assert len(nodes) >= 10
        assert len(edges) >= 9
        assert "data" in nodes[0]
        assert "id" in nodes[0]["data"]
        assert "label" in nodes[0]["data"]
        assert "data" in edges[0]
        assert "source" in edges[0]["data"]
        assert "target" in edges[0]["data"]

@pytest.mark.anyio
async def test_get_case_timeline():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/cases/DL-2026-0412/timeline")
        assert res.status_code == 200
        events = res.json()
        assert len(events) >= 4
        assert events[0]["event_id"] == "evt-001"
        assert "timestamp" in events[0]
        assert "category" in events[0]
        assert "involved_entities" in events[0]

@pytest.mark.anyio
async def test_get_case_entity_detail():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Priya
        res_p = await ac.get("/api/v1/cases/DL-2026-0412/entities/person-priya")
        assert res_p.status_code == 200
        priya = res_p.json()
        assert priya["id"] == "person-priya"
        assert priya["type"] == "PERSON"
        assert priya["sub_role"] == "SUBJECT_OF_SEARCH"
        assert len(priya["supporting_records"]) >= 1

        # Rakesh
        res_r = await ac.get("/api/v1/cases/DL-2026-0412/entities/person-rakesh")
        assert res_r.status_code == 200
        rakesh = res_r.json()
        assert rakesh["metrics"]["centrality_score"] == 0.94
        assert rakesh["metrics"]["risk_level"] == "CRITICAL"

        # Not found
        res_nf = await ac.get("/api/v1/cases/DL-2026-0412/entities/unknown-node")
        assert res_nf.status_code == 404

@pytest.mark.anyio
async def test_post_case_query():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {"query": "What connects Rakesh Kumar to the vehicle sighted at Singhu Border?"}
        res = await ac.post("/api/v1/cases/DL-2026-0412/query", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert "answer" in data
        assert data["confidence"] > 0.8
        assert "person-rakesh" in data["cited_entities"]
        assert len(data["suggested_actions"]) >= 1

@pytest.mark.anyio
async def test_get_case_provenance():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/cases/DL-2026-0412/provenance/verify")
        assert res.status_code == 200
        prov = res.json()
        assert prov["case_id"] == "DL-2026-0412"
        assert prov["status"] == "VERIFIED_INTACT"
        assert prov["bsa_section_63_compliant"] is True
        assert len(prov["audit_trail"]) >= 4
