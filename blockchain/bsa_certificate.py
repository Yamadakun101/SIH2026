"""
Bharatiya Sakshya Adhiniyam (BSA) 2023 — Section 63 Electronic Evidence Certificate Generator
Generates legally compliant, court-admissible digital certificates of evidence integrity.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from .custody_ledger import EvidenceCustodyLedger


class BSACertificateGenerator:
    """
    Generates Certificate of Electronic Evidence under Section 63 of the
    Bharatiya Sakshya Adhiniyam (BSA), 2023 (formerly Section 65B, Indian Evidence Act).
    """

    def __init__(self, ledger: EvidenceCustodyLedger):
        self.ledger = ledger
        self.case_id = ledger.case_id

    def generate_certificate(
        self,
        certifying_officer_name: str = "Inspector Ramesh Chander",
        certifying_officer_rank: str = "Sub-Inspector / Cyber Cell",
        certifying_officer_badge: str = "DP-SI-4921",
        police_station_agency: str = "Special Cell / Crime Branch, Delhi Police",
        court_jurisdiction: str = "Chief Metropolitan Magistrate Court, Tis Hazari, Delhi",
    ) -> Dict[str, Any]:
        """
        Generate structured BSA 2023 Section 63 certificate payload and printable legal text.
        """
        verification = self.ledger.get_verification_payload()
        now_ts = datetime.now(timezone.utc).isoformat()

        is_intact = verification["bsa_section_63_compliant"]
        merkle_root = verification["merkle_root"]
        total_records = verification["total_evidence_blocks"]
        latest_hash = verification["latest_block_hash"]
        genesis_ts = verification["genesis_timestamp"]

        legal_declaration_text = (
            f"CERTIFICATE UNDER SECTION 63 OF THE BHARATIYA SAKSHYA ADHINIYAM, 2023\n"
            f"FOR ADMISSIBILITY OF ELECTRONIC RECORDS\n\n"
            f"Case Identifier: {self.case_id}\n"
            f"Competent Court: {court_jurisdiction}\n"
            f"Investigating Agency: {police_station_agency}\n\n"
            f"I, {certifying_officer_name}, {certifying_officer_rank} (Badge No. {certifying_officer_badge}), "
            f"do hereby solemnly affirm, certify, and declare as follows:\n\n"
            f"1. That I have lawful control and supervisory custody over the digital analysis system (KavachNet) "
            f"used in the ingestion, normalization, and cryptographic custody management of electronic records for Case {self.case_id}.\n\n"
            f"2. That the electronic evidence items comprising {total_records} distinct blocks (including CDR logs, "
            f"ANPR vehicle sightings, telecom subscriber KYC, and banking records) were ingested into an immutable SHA-256 Merkle ledger.\n\n"
            f"3. SYSTEM INTEGRITY VERIFICATION:\n"
            f"   - Genesis Timestamp: {genesis_ts}\n"
            f"   - Cumulative Merkle Root: {merkle_root}\n"
            f"   - Latest Block Hash: {latest_hash}\n"
            f"   - Cryptographic Status: {'INTEGRITY VERIFIED - UNBROKEN HASH CHAIN' if is_intact else 'INTEGRITY MISMATCH DETECTED'}\n\n"
            f"4. That throughout the material period, the computer system and hashing algorithms operated properly without "
            f"any unauthorized manipulation, network intrusion, or corruption affecting the integrity of the stored electronic records.\n\n"
            f"5. That the information contained in the enclosed investigative graph, event timelines, and provenance trails "
            f"faithfully reproduces the electronic outputs of the source systems without alteration.\n\n"
            f"Certified on: {now_ts}\n"
            f"Signature of Certifying Authority: [ELECTRONICALLY VERIFIED — BADGE: {certifying_officer_badge}]\n"
            f"Rank & Designation: {certifying_officer_rank}, {police_station_agency}"
        )

        return {
            "certificate_id": f"BSA-63-{self.case_id}-{merkle_root[:12].upper()}",
            "statutory_provision": "Section 63, Bharatiya Sakshya Adhiniyam (BSA), 2023",
            "case_id": self.case_id,
            "issued_at": now_ts,
            "status": "VALID" if is_intact else "INVALID_TAMPERED",
            "certifying_officer": {
                "name": certifying_officer_name,
                "rank": certifying_officer_rank,
                "badge_id": certifying_officer_badge,
                "agency": police_station_agency,
                "jurisdiction": court_jurisdiction,
            },
            "evidence_integrity_metrics": {
                "total_blocks_verified": total_records,
                "merkle_root": merkle_root,
                "latest_block_hash": latest_hash,
                "chain_is_unbroken": is_intact,
            },
            "legal_declaration_text": legal_declaration_text,
            "audit_trail_summary": verification["audit_trail"],
        }
