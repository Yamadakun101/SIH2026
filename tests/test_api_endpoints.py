"""
Unit & Integration Tests for KavachNet FastAPI Endpoints
Tests strict compliance with docs/API_CONTRACT.md
"""

import sys
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.main import app


class TestAPIEndpoints(unittest.TestCase):
    """Test suite for KavachNet REST API routes."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_root_and_health(self):
        """Verify root and health check endpoints."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["system"], "KavachNet Intelligence Engine")
        self.assertEqual(data["status"], "OPERATIONAL")

        res_health = self.client.get("/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json()["status"], "HEALTHY")

    def test_02_get_states(self):
        """Verify GET /api/v1/states returns expected state metrics."""
        res = self.client.get("/api/v1/states")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        dl_state = next((s for s in data if s["state_code"] == "DL"), None)
        self.assertIsNotNone(dl_state)
        self.assertEqual(dl_state["state_name"], "Delhi")
        self.assertIn("active_cases_count", dl_state)
        self.assertIn("lat", dl_state)
        self.assertIn("lng", dl_state)

    def test_03_get_cases_and_filter(self):
        """Verify GET /api/v1/cases and state filtering."""
        res_all = self.client.get("/api/v1/cases")
        self.assertEqual(res_all.status_code, 200)
        cases = res_all.json()
        self.assertIsInstance(cases, list)
        self.assertTrue(any(c["case_id"] == "DL-2026-0412" for c in cases))

        # Filter by state=DL
        res_dl = self.client.get("/api/v1/cases?state=DL")
        self.assertEqual(res_dl.status_code, 200)
        dl_cases = res_dl.json()
        self.assertTrue(all(c["state_code"] == "DL" for c in dl_cases))

    def test_04_get_case_metadata(self):
        """Verify GET /api/v1/cases/{case_id}."""
        res = self.client.get("/api/v1/cases/DL-2026-0412")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["case_id"], "DL-2026-0412")
        self.assertEqual(data["state_code"], "DL")
        self.assertTrue(data.get("bsa_section_63_verified", False))

        # 404 for invalid case
        res_404 = self.client.get("/api/v1/cases/INVALID-CASE-999")
        self.assertEqual(res_404.status_code, 404)

    def test_05_get_case_graph_cytoscape(self):
        """Verify GET /api/v1/cases/{case_id}/graph returns Cytoscape elements with centrality."""
        res = self.client.get("/api/v1/cases/DL-2026-0412/graph")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["case_id"], "DL-2026-0412")
        self.assertIn("elements", data)
        self.assertIn("nodes", data["elements"])
        self.assertIn("edges", data["elements"])

        nodes = data["elements"]["nodes"]
        edges = data["elements"]["edges"]
        self.assertGreaterEqual(len(nodes), 8)
        self.assertGreaterEqual(len(edges), 8)

        # Verify node fields
        rakesh_node = next((n["data"] for n in nodes if n["data"]["id"] == "person-rakesh"), None)
        self.assertIsNotNone(rakesh_node)
        self.assertEqual(rakesh_node["label"], "Rakesh Kumar")
        self.assertIn("centrality_score", rakesh_node)
        self.assertGreater(rakesh_node["centrality_score"], 0.5)

    def test_06_get_case_timeline(self):
        """Verify GET /api/v1/cases/{case_id}/timeline."""
        res = self.client.get("/api/v1/cases/DL-2026-0412/timeline")
        self.assertEqual(res.status_code, 200)
        timeline = res.json()
        self.assertIsInstance(timeline, list)
        self.assertGreaterEqual(len(timeline), 4)
        first_event = timeline[0]
        self.assertIn("event_id", first_event)
        self.assertIn("timestamp", first_event)
        self.assertIn("category", first_event)
        self.assertIn("involved_entities", first_event)

    def test_07_get_entity_profile(self):
        """Verify GET /api/v1/cases/{case_id}/entities/{entity_id}."""
        res = self.client.get("/api/v1/cases/DL-2026-0412/entities/person-rakesh")
        self.assertEqual(res.status_code, 200)
        profile = res.json()
        self.assertEqual(profile["entity_id"], "person-rakesh")
        self.assertEqual(profile["label"], "Rakesh Kumar")
        self.assertIn("connected_entities", profile)
        self.assertIn("provenance_hash", profile)
        self.assertGreaterEqual(len(profile["connected_entities"]), 1)

    def test_08_query_assistant(self):
        """Verify POST /api/v1/cases/{case_id}/query and /api/v1/assistant/query."""
        payload = {"query": "What phone number was used by Rakesh Kumar?"}
        res = self.client.post("/api/v1/cases/DL-2026-0412/query", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("answer", data)
        self.assertIn("confidence", data)
        self.assertIn("suggested_actions", data)
        self.assertGreater(data["confidence"], 0.5)

        # Global assistant route alias
        res_global = self.client.post("/api/v1/assistant/query", json=payload)
        self.assertEqual(res_global.status_code, 200)

    def test_09_verify_provenance(self):
        """Verify GET /api/v1/cases/{case_id}/provenance/verify under BSA 2023 Sec 63."""
        res = self.client.get("/api/v1/cases/DL-2026-0412/provenance/verify")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["case_id"], "DL-2026-0412")
        self.assertEqual(data["status"], "VERIFIED_INTACT")
        self.assertTrue(data["bsa_section_63_compliant"])
        self.assertIn("merkle_root", data)
        self.assertIn("audit_trail", data)
        self.assertGreaterEqual(len(data["audit_trail"]), 1)


if __name__ == "__main__":
    unittest.main()
