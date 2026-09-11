import json
from pathlib import Path
from typing import Any, Dict, List
from backend.app.ingestion.envelope import verify_envelope
from backend.app.ingestion.parsers import parse_fir, parse_cdr, parse_banking, parse_cctv

class IngestionEngine:
    """
    KavachNet Ingestion & Normalization Engine.
    Processes multi-source evidentiary feeds, verifies SHA-256 custody seals,
    and extracts deduplicated graph elements.
    """
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: Dict[str, Dict[str, Any]] = {}
        self.records_processed = 0
        self.tamper_check_failures = 0

    def ingest_envelope(self, envelope: Dict[str, Any]) -> bool:
        """Processes a single raw envelope, verifying provenance before extraction."""
        if not verify_envelope(envelope):
            self.tamper_check_failures += 1
            return False

        source_type = envelope.get("source_type", "")
        extracted_nodes: List[Dict[str, Any]] = []
        extracted_edges: List[Dict[str, Any]] = []

        if source_type == "FIR":
            extracted_nodes, extracted_edges = parse_fir(envelope)
        elif source_type == "CDR":
            extracted_nodes, extracted_edges = parse_cdr(envelope)
        elif source_type == "BANK":
            extracted_nodes, extracted_edges = parse_banking(envelope)
        elif source_type == "CCTV_ANPR":
            extracted_nodes, extracted_edges = parse_cctv(envelope)
        else:
            # Pass through generic
            pass

        # Deduplicate and merge nodes
        for node in extracted_nodes:
            n_id = node["id"]
            if n_id not in self.nodes:
                self.nodes[n_id] = node
            else:
                existing_records = set(self.nodes[n_id].get("supporting_records", []))
                existing_records.update(node.get("supporting_records", []))
                self.nodes[n_id]["supporting_records"] = sorted(list(existing_records))

        # Deduplicate edges
        for edge in extracted_edges:
            e_id = edge["id"]
            self.edges[e_id] = edge

        self.records_processed += 1
        return True

    def ingest_directory(self, raw_dir: Path) -> Dict[str, Any]:
        """Scans a directory recursively for JSON envelopes and ingests all valid files."""
        for json_file in raw_dir.glob("**/*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        for env in content:
                            if isinstance(env, dict) and "provenance" in env:
                                self.ingest_envelope(env)
                    elif isinstance(content, dict) and "provenance" in content:
                        self.ingest_envelope(content)
            except Exception as e:
                print(f"[-] Error reading {json_file}: {e}")

        return {
            "records_processed": self.records_processed,
            "tamper_check_failures": self.tamper_check_failures,
            "unique_nodes_extracted": len(self.nodes),
            "unique_edges_extracted": len(self.edges)
        }

ingestion_engine = IngestionEngine()
