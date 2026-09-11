import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "dl-2026-0412.json"

@pytest.fixture
def canonical_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def test_baseline_entities_preserved(canonical_data):
    """Verifies that all 10 baseline nodes and 9 baseline edges remain untouched."""
    baseline_nodes = {
        "person-priya", "person-rakesh", "person-vikram",
        "phone-priya", "phone-burner-rakesh", "phone-vikram",
        "vehicle-dl01-9921", "loc-kashmere-gate", "loc-singhu-border", "bank-mule-01"
    }
    baseline_edges = {
        "edge-call-01", "edge-call-02", "edge-call-03",
        "edge-loc-01", "edge-loc-02", "edge-assoc-01",
        "edge-veh-01", "edge-toll-01", "edge-fin-01"
    }
    
    current_nodes = {n["data"]["id"] for n in canonical_data["graph"]["elements"]["nodes"]}
    current_edges = {e["data"]["id"] for e in canonical_data["graph"]["elements"]["edges"]}
    
    for b_node in baseline_nodes:
        assert b_node in current_nodes, f"Baseline node '{b_node}' missing!"
        
    for b_edge in baseline_edges:
        assert b_edge in current_edges, f"Baseline edge '{b_edge}' missing!"

def test_all_eight_forensic_categories_present(canonical_data):
    """Verifies that all 8 forensic categories exist with non-empty record sets."""
    assert "forensics" in canonical_data
    forensics = canonical_data["forensics"]
    
    expected_categories = [
        "DNA_BIOLOGICAL",
        "FINGERPRINT_LATENT",
        "DIGITAL_FORENSICS",
        "CCTV_VIDEO_FORENSICS",
        "TRACE_EVIDENCE",
        "FOOTWEAR_TIRE_IMPRESSIONS",
        "BALLISTICS_TOOLMARKS",
        "CHAIN_OF_CUSTODY"
    ]
    for cat in expected_categories:
        assert cat in forensics["categories_present"]

    assert len(forensics["dna_evidence"]) >= 3
    assert len(forensics["fingerprint_evidence"]) >= 3
    assert len(forensics["digital_forensics"]) >= 2
    assert len(forensics["cctv_video_forensics"]) >= 2
    assert len(forensics["trace_evidence"]) >= 3
    assert len(forensics["impression_evidence"]) >= 2
    assert len(forensics["ballistics_toolmarks"]) >= 2
    assert len(forensics["chain_of_custody"]) >= 2

def test_forensic_ids_are_unique(canonical_data):
    """Ensures no duplicate evidence_id or record_id exists across categories."""
    forensics = canonical_data["forensics"]
    seen_ids = set()
    
    for list_name in [
        "dna_evidence", "fingerprint_evidence", "digital_forensics",
        "cctv_video_forensics", "trace_evidence", "impression_evidence",
        "ballistics_toolmarks"
    ]:
        for item in forensics[list_name]:
            eid = item["evidence_id"]
            assert eid not in seen_ids, f"Duplicate evidence_id: {eid}"
            seen_ids.add(eid)

def test_investigative_non_guilt_terminology(canonical_data):
    """Ensures investigative terminology is strictly followed (no guilt hardcoding)."""
    raw_str = json.dumps(canonical_data["forensics"]).lower()
    assert '"guilty": true' not in raw_str
    assert '"criminal": true' not in raw_str
    assert '"confirmed perpetrator": true' not in raw_str

    # Must contain investigative terminology
    assert any(term in raw_str for term in ["strong association", "potential match", "investigative lead", "inconclusive", "verified"])

def test_confidence_variation_and_exclusionary_controls(canonical_data):
    """Verifies that confidence scores vary realistically and exclusionary findings exist."""
    forensics = canonical_data["forensics"]
    all_confidences = []

    for item in forensics["dna_evidence"]:
        all_confidences.append(item["match_confidence"])
    for item in forensics["fingerprint_evidence"]:
        all_confidences.append(item["similarity_score"])
    for item in forensics["trace_evidence"]:
        all_confidences.append(item["similarity_confidence"])

    # Verify score variation (not all 0.99)
    assert min(all_confidences) <= 0.55, "Should contain lower/inconclusive scores for realism"
    assert max(all_confidences) >= 0.90, "Should contain high-confidence verified scores"
    assert len(set(all_confidences)) >= 4, "Should exhibit granular confidence variance"

def test_cross_source_corroboration_graph_connectivity(canonical_data):
    """Verifies multiple independent evidence paths connect person, vehicle, and locations."""
    nodes = {n["data"]["id"]: n["data"] for n in canonical_data["graph"]["elements"]["nodes"]}
    edges = canonical_data["graph"]["elements"]["edges"]

    # Touch DNA & Latent Print both connect to Rakesh & Vehicle DL 01 AB 9921
    rakesh_edges = [e["data"] for e in edges if e["data"]["target"] == "person-rakesh"]
    vehicle_edges = [e["data"] for e in edges if e["data"]["target"] == "vehicle-dl01-9921" or e["data"]["source"] == "vehicle-dl01-9921"]

    rakesh_sources = {e["source"] for e in rakesh_edges}
    assert "evidence-dna-touch-01" in rakesh_sources
    assert "evidence-fp-door-01" in rakesh_sources

    vehicle_connected = {e["source"] for e in vehicle_edges} | {e["target"] for e in vehicle_edges}
    assert "evidence-dna-touch-01" in vehicle_connected
    assert "evidence-fp-door-01" in vehicle_connected
    assert "evidence-trace-soil-01" in vehicle_connected
    assert "evidence-tire-isbt-01" in vehicle_connected

def test_timeline_chronological_consistency(canonical_data):
    """Verifies timeline events maintain chronological progression without contradictions."""
    timeline = canonical_data["timeline"]
    timestamps = [e["timestamp"] for e in timeline]
    assert timestamps == sorted(timestamps), "Timeline events must be chronologically ordered"

def test_chain_of_custody_and_integrity_hashes(canonical_data):
    """Verifies that chain of custody records have valid sequential transfers and matching SHA-256 hashes."""
    coc_list = canonical_data["forensics"]["chain_of_custody"]
    for coc in coc_list:
        assert coc["original_hash"] == coc["current_hash"]
        assert len(coc["original_hash"]) == 64
        assert len(coc["transfer_events"]) >= 2
        # Verify transfer index ordering
        indices = [t["transfer_index"] for t in coc["transfer_events"]]
        assert indices == sorted(indices)
        assert coc["bsa_section_63_compliant"] is True

def test_forensic_rest_api_overview():
    """Tests GET /api/v1/cases/{case_id}/forensics endpoint."""
    res = client.get("/api/v1/cases/DL-2026-0412/forensics")
    assert res.status_code == 200
    data = res.json()
    assert data["case_id"] == "DL-2026-0412"
    assert data["total_forensic_records"] >= 19
    assert len(data["categories_present"]) == 8

def test_forensic_rest_api_by_category():
    """Tests GET /api/v1/cases/{case_id}/forensics/categories/{category} endpoint."""
    res = client.get("/api/v1/cases/DL-2026-0412/forensics/categories/dna")
    assert res.status_code == 200
    dna_list = res.json()
    assert len(dna_list) >= 3
    assert any(item["evidence_id"] == "EVID-DNA-001" for item in dna_list)

    res_fp = client.get("/api/v1/cases/DL-2026-0412/forensics/categories/fingerprint")
    assert res_fp.status_code == 200
    assert len(res_fp.json()) >= 3

def test_forensic_rest_api_chain_of_custody():
    """Tests GET /api/v1/cases/{case_id}/forensics/chain-of-custody/{evidence_id} endpoint."""
    res = client.get("/api/v1/cases/DL-2026-0412/forensics/chain-of-custody/EVID-DNA-001")
    assert res.status_code == 200
    coc = res.json()
    assert coc["evidence_id"] == "EVID-DNA-001"
    assert coc["integrity_status"] == "INTACT_VERIFIED"
    assert len(coc["transfer_events"]) == 4

def test_forensic_query_reasoning():
    """Tests that the AI Assistant can answer forensic correlation queries."""
    res = client.post(
        "/api/v1/cases/DL-2026-0412/query",
        json={"query": "What forensic evidence connects Rakesh Kumar to vehicle DL 01 AB 9921?"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "Touch DNA" in data["answer"] or "DNA-FSL-DEL-2026-401" in data["answer"]
    assert "person-rakesh" in data["cited_entities"]
    assert "vehicle-dl01-9921" in data["cited_entities"]
