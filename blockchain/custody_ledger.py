"""
Digital Evidence Custody Ledger
Manages append-only immutable custody logs and audit trails for criminal network analysis.
"""

from typing import Any, Dict, List, Optional
from .hash_chain import EvidenceHashChain


class EvidenceCustodyLedger:
    """Manages the full evidence custody lifecycle for an investigation."""

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.chain = EvidenceHashChain(case_id=case_id)

    def initialize(self, officer_badge: str, timestamp: Optional[str] = None) -> None:
        """Initialize genesis block if not already initialized."""
        if not self.chain.blocks:
            self.chain.create_genesis_block(officer_badge=officer_badge, timestamp=timestamp)

    def log_ingestion(
        self,
        record_id: str,
        source_type: str,
        data_payload: Dict[str, Any],
        officer_badge: str,
        timestamp: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record an evidence ingestion event."""
        if not self.chain.blocks:
            self.initialize(officer_badge=officer_badge, timestamp=timestamp)

        metadata = {"notes": notes} if notes else {}
        block = self.chain.append_evidence(
            record_id=record_id,
            source_type=source_type,
            data_payload=data_payload,
            officer_badge=officer_badge,
            action="EVIDENCE_INGESTED",
            timestamp=timestamp,
            metadata=metadata,
        )
        return block.to_dict()

    def log_custody_action(
        self,
        record_id: str,
        action: str,
        officer_badge: str,
        action_details: Dict[str, Any],
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record an analysis, transfer, or verification step on existing evidence."""
        if not self.chain.blocks:
            self.initialize(officer_badge=officer_badge, timestamp=timestamp)

        block = self.chain.append_evidence(
            record_id=record_id,
            source_type="CUSTODY_EVENT",
            data_payload=action_details,
            officer_badge=officer_badge,
            action=action,
            timestamp=timestamp,
        )
        return block.to_dict()

    def populate_from_case_dataset(self, case_data: Dict[str, Any], officer_badge: str = "DP-SI-4921") -> None:
        """Populate the chain of custody from a canonical case dataset (e.g. DL-2026-0412)."""
        meta = case_data.get("case_metadata", {})
        incident_date = meta.get("incident_date", "2026-09-02T22:30:00Z")
        self.initialize(officer_badge=officer_badge, timestamp=incident_date)

        # Ingest FIR / Primary case metadata
        self.log_ingestion(
            record_id=meta.get("fir_number", f"FIR-{self.case_id}"),
            source_type="FIR_PRIMARY",
            data_payload={
                "case_id": self.case_id,
                "title": meta.get("title"),
                "summary": meta.get("summary"),
                "lead_agency": meta.get("lead_agency"),
            },
            officer_badge=officer_badge,
            timestamp=incident_date,
        )

        # Ingest timeline events
        timeline_events = case_data.get("timeline", [])
        for evt in timeline_events:
            self.log_ingestion(
                record_id=evt.get("source_record_id", evt.get("event_id")),
                source_type=evt.get("category", "INVESTIGATIVE_RECORD"),
                data_payload={
                    "title": evt.get("title"),
                    "description": evt.get("description"),
                    "location": evt.get("location"),
                    "involved_entities": evt.get("involved_entities", []),
                    "confidence": evt.get("confidence", 0.9),
                },
                officer_badge=officer_badge,
                timestamp=evt.get("timestamp"),
            )

        # Ingest graph edges / relational links
        edges = case_data.get("graph", {}).get("edges", [])
        for edge in edges:
            self.log_ingestion(
                record_id=f"REL-{edge.get('id')}",
                source_type=edge.get("evidence_source", "RELATIONAL_LINK"),
                data_payload={
                    "source": edge.get("source"),
                    "target": edge.get("target"),
                    "label": edge.get("label"),
                    "type": edge.get("type"),
                    "confidence": edge.get("confidence"),
                },
                officer_badge=officer_badge,
                timestamp=incident_date,
            )

    def get_audit_trail(self, record_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return formatted audit trail entries matching API_CONTRACT.md format."""
        trail = []
        for block in self.chain.blocks:
            if record_id and block.record_id != record_id:
                continue
            trail.append({
                "block_index": block.block_index,
                "record_id": block.record_id,
                "source_type": block.source_type,
                "sha256": block.block_hash,
                "data_sha256": block.data_hash,
                "timestamp": block.timestamp,
                "officer_badge": block.officer_badge,
                "action": block.action,
                "status": "VALID",
            })
        return trail

    def get_verification_payload(self) -> Dict[str, Any]:
        """Generate verification payload matching GET /api/v1/cases/{case_id}/provenance/verify."""
        is_valid, corrupted_idx, reason = self.chain.verify_chain()
        latest_hash = self.chain.blocks[-1].block_hash if self.chain.blocks else None
        genesis_ts = self.chain.blocks[0].timestamp if self.chain.blocks else None

        return {
            "case_id": self.case_id,
            "status": "VERIFIED_INTACT" if is_valid else "INTEGRITY_COMPROMISED",
            "bsa_section_63_compliant": is_valid,
            "total_evidence_blocks": len(self.chain.blocks),
            "genesis_timestamp": genesis_ts,
            "latest_block_hash": latest_hash,
            "merkle_root": self.chain.get_merkle_root(),
            "verification_message": reason,
            "corrupted_block_index": corrupted_idx,
            "audit_trail": self.get_audit_trail(),
        }
