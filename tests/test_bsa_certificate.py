"""
Unit Tests for Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63 Certificate Generation
"""

import json
import os
import unittest
from blockchain.custody_ledger import EvidenceCustodyLedger
from blockchain.bsa_certificate import BSACertificateGenerator


class TestBSACertificate(unittest.TestCase):

    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data", "dl-2026-0412.json")
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.case_data = json.load(f)

        self.ledger = EvidenceCustodyLedger("DL-2026-0412")
        self.ledger.populate_from_case_dataset(self.case_data, officer_badge="DP-SI-4921")
        self.cert_gen = BSACertificateGenerator(self.ledger)

    def test_generate_valid_certificate(self):
        cert = self.cert_gen.generate_certificate(
            certifying_officer_name="Inspector Ramesh Chander",
            certifying_officer_rank="Sub-Inspector / Cyber Cell",
            certifying_officer_badge="DP-SI-4921",
        )

        self.assertEqual(cert["status"], "VALID")
        self.assertIn("BSA-63-DL-2026-0412-", cert["certificate_id"])
        self.assertEqual(cert["statutory_provision"], "Section 63, Bharatiya Sakshya Adhiniyam (BSA), 2023")
        self.assertTrue(cert["evidence_integrity_metrics"]["chain_is_unbroken"])
        self.assertGreater(cert["evidence_integrity_metrics"]["total_blocks_verified"], 5)

        # Check legal text contents
        legal_text = cert["legal_declaration_text"]
        self.assertIn("BHARATIYA SAKSHYA ADHINIYAM, 2023", legal_text)
        self.assertIn("SECTION 63", legal_text)
        self.assertIn("DP-SI-4921", legal_text)
        self.assertIn("Inspector Ramesh Chander", legal_text)
        self.assertIn(cert["evidence_integrity_metrics"]["merkle_root"], legal_text)

    def test_tampered_certificate_status(self):
        # Tamper with an evidence block
        self.ledger.chain.blocks[2].data_payload["tampered_key"] = "malicious_injection"

        cert = self.cert_gen.generate_certificate()
        self.assertEqual(cert["status"], "INVALID_TAMPERED")
        self.assertFalse(cert["evidence_integrity_metrics"]["chain_is_unbroken"])
        self.assertIn("INTEGRITY MISMATCH", cert["legal_declaration_text"])


if __name__ == "__main__":
    unittest.main()
