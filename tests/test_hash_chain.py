"""
Unit Tests for SHA-256 Merkle Hash-Chain and Custody Ledger
"""

import unittest
from blockchain.hash_chain import EvidenceHashChain, MerkleTree, sha256_hex
from blockchain.custody_ledger import EvidenceCustodyLedger


class TestHashChain(unittest.TestCase):

    def setUp(self):
        self.case_id = "DL-2026-0412"
        self.chain = EvidenceHashChain(self.case_id)

    def test_genesis_block(self):
        genesis = self.chain.create_genesis_block(officer_badge="TEST-BADGE-01")
        self.assertEqual(genesis.block_index, 0)
        self.assertEqual(genesis.prev_block_hash, "0" * 64)
        self.assertEqual(len(self.chain.blocks), 1)

        is_valid, corrupt_idx, msg = self.chain.verify_chain()
        self.assertTrue(is_valid)
        self.assertIsNone(corrupt_idx)

    def test_append_evidence_blocks(self):
        self.chain.append_evidence(
            record_id="FIR-412/2026",
            source_type="FIR",
            data_payload={"incident": "Missing person report", "victim": "Priya Sharma"},
            officer_badge="DP-SI-4921",
        )
        self.chain.append_evidence(
            record_id="CDR-DEL-0902-1",
            source_type="CDR",
            data_payload={"caller": "+919871044219", "receiver": "+919811200341"},
            officer_badge="DP-SI-4921",
        )
        self.assertEqual(len(self.chain.blocks), 3)  # Genesis + 2 evidence blocks

        is_valid, corrupt_idx, msg = self.chain.verify_chain()
        self.assertTrue(is_valid)
        self.assertIsNone(corrupt_idx)

    def test_merkle_tree_proofs(self):
        leaf_hashes = [
            sha256_hex(b"record_1"),
            sha256_hex(b"record_2"),
            sha256_hex(b"record_3"),
            sha256_hex(b"record_4"),
        ]
        tree = MerkleTree(leaf_hashes)
        root = tree.get_merkle_root()
        self.assertIsNotNone(root)
        self.assertEqual(len(root), 64)

        # Test inclusion proof for each leaf
        for idx, leaf in enumerate(leaf_hashes):
            proof = tree.get_inclusion_proof(idx)
            is_valid_proof = MerkleTree.verify_proof(leaf, proof, root)
            self.assertTrue(is_valid_proof, f"Merkle proof failed for leaf {idx}")

    def test_tamper_detection_payload_alteration(self):
        self.chain.append_evidence(
            record_id="ANPR-TOLL-01",
            source_type="ANPR",
            data_payload={"vehicle": "DL 01 AB 9921", "speed": 82},
            officer_badge="DP-SI-4921",
        )
        self.chain.append_evidence(
            record_id="BANK-TX-01",
            source_type="BANKING",
            data_payload={"amount": 45000, "vpa": "rkenterprises@okhdfc"},
            officer_badge="DP-SI-4921",
        )

        # Confirm valid before tamper
        is_valid, _, _ = self.chain.verify_chain()
        self.assertTrue(is_valid)

        # Tamper with block 1 data payload
        self.chain.blocks[1].data_payload["amount"] = 999999

        is_valid, corrupt_idx, msg = self.chain.verify_chain()
        self.assertFalse(is_valid)
        self.assertEqual(corrupt_idx, 1)
        self.assertIn("altered", msg.lower())

    def test_custody_ledger_lifecycle(self):
        ledger = EvidenceCustodyLedger("DL-2026-0412")
        ledger.initialize(officer_badge="DP-SI-4921")
        ledger.log_ingestion(
            record_id="CCTV-SINGHU-04",
            source_type="CCTV",
            data_payload={"camera_id": "SINGHU-LANE-04", "vehicle": "DL 01 AB 9921"},
            officer_badge="DP-SI-4921",
        )
        ledger.log_custody_action(
            record_id="CCTV-SINGHU-04",
            action="FORENSIC_EXTRACTION_COMPLETED",
            officer_badge="DP-INSP-1092",
            action_details={"extracted_frames_count": 48},
        )

        payload = ledger.get_verification_payload()
        self.assertEqual(payload["status"], "VERIFIED_INTACT")
        self.assertTrue(payload["bsa_section_63_compliant"])
        self.assertEqual(payload["total_evidence_blocks"], 3)
        self.assertEqual(len(payload["audit_trail"]), 3)


if __name__ == "__main__":
    unittest.main()
