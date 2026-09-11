"""
Unit Tests for Named Entity Recognition (NER) and Entity Disambiguation
"""

import unittest
from ai.ner_extractor import MultiSourceNERExtractor
from ai.entity_resolution import EntityResolver


class TestEntityResolution(unittest.TestCase):

    def setUp(self):
        self.extractor = MultiSourceNERExtractor()
        self.resolver = EntityResolver()

    def test_ner_extraction_multi_type(self):
        raw_text = (
            "Complainant reported that victim Priya was last sighted near ISBT Kashmere Gate. "
            "Suspect Raka was observed operating vehicle DL 01 AB 9921 and communicating via "
            "+91 98710 44219. Transactions were traced to UPI ID rkenterprises@okhdfc."
        )
        entities = self.extractor.extract_all(raw_text, source_context="POLICE_DIARY_EXCERPT")

        extracted_types = {e.entity_type for e in entities}
        self.assertIn("PERSON", extracted_types)
        self.assertIn("LOCATION", extracted_types)
        self.assertIn("VEHICLE", extracted_types)
        self.assertIn("PHONE", extracted_types)
        self.assertIn("BANK_ACCOUNT", extracted_types)

        # Check vehicle plate normalization
        vehicle_ent = next(e for e in entities if e.entity_type == "VEHICLE")
        self.assertEqual(vehicle_ent.normalized_value, "DL 01 AB 9921")

        # Check phone normalization
        phone_ent = next(e for e in entities if e.entity_type == "PHONE")
        self.assertEqual(phone_ent.normalized_value, "+91 98710 44219")

    def test_alias_and_entity_resolution(self):
        raw_text = "Raka met with Vicky near Singhu Border Toll Plaza before driving DL01AB9921."
        entities = self.extractor.extract_all(raw_text)
        resolved_links = self.resolver.resolve_batch(entities)

        canonical_ids = {r.canonical_node_id for r in resolved_links}
        self.assertIn("person-rakesh", canonical_ids)  # 'Raka' -> 'person-rakesh'
        self.assertIn("person-vikram", canonical_ids)  # 'Vicky' -> 'person-vikram'
        self.assertIn("vehicle-dl01-9921", canonical_ids)  # 'DL01AB9921' -> 'vehicle-dl01-9921'
        self.assertIn("loc-singhu-border", canonical_ids)

    def test_confidence_scores_present(self):
        raw_text = "Call logged from +919811200341 to 9871044219."
        entities = self.extractor.extract_all(raw_text)
        for ent in entities:
            self.assertGreaterEqual(ent.confidence, 0.80)
            self.assertLessEqual(ent.confidence, 1.0)


if __name__ == "__main__":
    unittest.main()
