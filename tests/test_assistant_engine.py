"""
Unit Tests for AI Investigative Assistant Engine
"""

import json
import os
import unittest
from ai.assistant_engine import InvestigativeAssistantEngine


class TestAssistantEngine(unittest.TestCase):

    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data", "dl-2026-0412.json")
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.case_data = json.load(f)

        self.engine = InvestigativeAssistantEngine(self.case_data)

    def _verify_contract_schema(self, res: dict):
        self.assertIn("query", res)
        self.assertIn("answer", res)
        self.assertIn("confidence", res)
        self.assertIn("cited_entities", res)
        self.assertIn("cited_sources", res)
        self.assertIn("suggested_actions", res)
        self.assertIsInstance(res["cited_entities"], list)
        self.assertIsInstance(res["cited_sources"], list)
        self.assertIsInstance(res["suggested_actions"], list)
        self.assertGreater(len(res["cited_entities"]), 0)
        self.assertGreater(len(res["cited_sources"]), 0)
        self.assertGreater(len(res["suggested_actions"]), 0)

        # Operational principle: Lead generation, never verdict
        ans_lower = res["answer"].lower()
        self.assertNotIn("guilty", ans_lower)
        self.assertNotIn("convicted", ans_lower)

    def test_rakesh_vehicle_connection_query(self):
        q = "What connects Rakesh Kumar to the vehicle sighted at Singhu Border?"
        res = self.engine.answer_query(q)
        self._verify_contract_schema(res)
        self.assertIn("person-rakesh", res["cited_entities"])
        self.assertIn("vehicle-dl01-9921", res["cited_entities"])

    def test_priya_contact_query(self):
        q = "Who was in contact with Priya before her device powered off?"
        res = self.engine.answer_query(q)
        self._verify_contract_schema(res)
        self.assertIn("person-priya", res["cited_entities"])
        self.assertIn("phone-burner-rakesh", res["cited_entities"])

    def test_mule_account_query(self):
        q = "Identify all suspicious mule accounts or financial transfers"
        res = self.engine.answer_query(q)
        self._verify_contract_schema(res)
        self.assertIn("bank-mule-01", res["cited_entities"])

    def test_centrality_hubs_query(self):
        q = "Which entities have the highest centrality score in the network?"
        res = self.engine.answer_query(q)
        self._verify_contract_schema(res)
        self.assertIn("person-rakesh", res["cited_entities"])

    def test_timeline_query(self):
        q = "Summarize the chronological timeline of events"
        res = self.engine.answer_query(q)
        self._verify_contract_schema(res)


if __name__ == "__main__":
    unittest.main()
