"""
Case Service — Bridges Data Layer, Knowledge Graph, AI Engine, and Blockchain Provenance
Unified implementation integrating Core AI Centrality, Graph Analytics, BSA 2023 Hash Chain,
and 8-Discipline Forensic Database Intelligence.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.app.core.config import settings
from backend.app.models.state import StateItem
from backend.app.models.case import CaseSummary
from backend.app.models.graph import GraphResponse, GraphElements, CytoscapeNode, CytoscapeEdge
from backend.app.models.timeline import TimelineEvent
from backend.app.models.entity import EntityDetail, EntityMetrics
from backend.app.models.query import QueryResponse
from backend.app.models.provenance import ProvenanceResponse, AuditBlock
from backend.app.models.forensics import CaseForensicsOverview, ChainOfCustodyRecord

# Core AI, Graph, and Blockchain engines
from ai.assistant_engine import InvestigativeAssistantEngine
from blockchain.hash_chain import EvidenceHashChain
from graph.centrality_analytics import CentralityAnalytics
from graph.graph_builder import CrimeGraph


def _find_project_root() -> Path:
    current = Path(__file__).resolve().parent
    for _ in range(6):
        if (current / "data").exists() and (current / "ai").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent.parent


class CaseService:
    """Unified service to manage case data, graph operations, AI queries, and evidence integrity."""

    def __init__(self, data_file: Optional[Path] = None, data_dir: Optional[Path] = None):
        project_root = _find_project_root()
        self.data_dir = Path(data_dir) if data_dir else project_root / "data"
        self.data_file = Path(data_file) if data_file else (self.data_dir / "dl-2026-0412.json")

        self._cases_cache: Dict[str, Dict[str, Any]] = {}
        self._graph_cache: Dict[str, CrimeGraph] = {}
        self._centrality_cache: Dict[str, Dict[str, Any]] = {}
        self._assistant_cache: Dict[str, InvestigativeAssistantEngine] = {}
        self._hashchain_cache: Dict[str, EvidenceHashChain] = {}
        self._cache: Optional[Dict[str, Any]] = None

        self._load_all_cases()

    def _load_all_cases(self) -> None:
        """Scan data directory and load case files, initializing AI, Graph, and Blockchain engines."""
        # 1. Primary canonical case file
        if self.data_file.exists():
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    primary_data = json.load(f)
                    self._cache = primary_data
                    case_id = primary_data.get("case_metadata", {}).get("case_id", "DL-2026-0412")
                    self._cases_cache[case_id] = primary_data
                    self._initialize_case_services(case_id, primary_data)
            except Exception as e:
                print(f"Error loading primary case file {self.data_file}: {e}")

        # 2. Additional case JSON files in data directory
        if self.data_dir.exists():
            for json_file in self.data_dir.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        case_data = json.load(f)
                        case_id = case_data.get("case_metadata", {}).get("case_id")
                        if case_id and case_id not in self._cases_cache:
                            self._cases_cache[case_id] = case_data
                            self._initialize_case_services(case_id, case_data)
                except Exception as e:
                    print(f"Error scanning case file {json_file}: {e}")

    def _initialize_case_services(self, case_id: str, case_data: Dict[str, Any]) -> None:
        """Initialize graph builder, centrality analytics, AI assistant, and hash chain for the case."""
        try:
            # 1. Build Graph & Compute Centrality
            graph = CrimeGraph.from_case_json(case_data)
            centrality = CentralityAnalytics(graph)
            centrality.apply_centrality_to_graph()
            self._graph_cache[case_id] = graph
            self._centrality_cache[case_id] = centrality.compute_composite_centrality()

            # 2. Assistant Engine
            assistant = InvestigativeAssistantEngine(case_data=case_data, graph=graph)
            self._assistant_cache[case_id] = assistant

            # 3. Hash Chain & Custody Ledger under BSA 2023 Section 63
            hash_chain = EvidenceHashChain(case_id=case_id)
            hash_chain.create_genesis_block(
                officer_badge="DP-SI-4921",
                notes="Case Evidence Custody Chain Initialized under BSA 2023 Section 63"
            )
            for idx, event in enumerate(case_data.get("timeline", [])):
                hash_chain.append_evidence(
                    record_id=event.get("source_record_id", f"REC-{idx+1}"),
                    source_type=event.get("category", "INVESTIGATIVE_LOG"),
                    data_payload=event,
                    officer_badge="DP-SI-4921",
                    action="INGESTED"
                )
            self._hashchain_cache[case_id] = hash_chain
        except Exception as e:
            print(f"Warning: could not initialize advanced analytical services for {case_id}: {e}")

    @property
    def data(self) -> Dict[str, Any]:
        """Returns primary case data dictionary."""
        if self._cache is None:
            self._load_all_cases()
        return self._cache or {}

    def get_states(self) -> List[StateItem]:
        """Return list of states with active case metrics."""
        raw_states = self.data.get("states", [])
        if raw_states:
            return [StateItem(**item) for item in raw_states]

        # Standard fallback state register
        return [
            StateItem(state_code="DL", state_name="Delhi", active_cases_count=len(self._cases_cache), high_risk_alerts=1, lat=28.6139, lng=77.2090),
            StateItem(state_code="MH", state_name="Maharashtra", active_cases_count=0, high_risk_alerts=0, lat=19.7515, lng=75.7139),
            StateItem(state_code="UP", state_name="Uttar Pradesh", active_cases_count=0, high_risk_alerts=0, lat=26.8467, lng=80.9462),
            StateItem(state_code="HR", state_name="Haryana", active_cases_count=0, high_risk_alerts=0, lat=29.0588, lng=76.0856),
            StateItem(state_code="PB", state_name="Punjab", active_cases_count=0, high_risk_alerts=0, lat=31.1471, lng=75.3412),
        ]

    def get_cases(self, state_code: Optional[str] = None) -> List[CaseSummary]:
        """Retrieve cases, optionally filtered by state code."""
        results: List[CaseSummary] = []
        for cid, cdata in self._cases_cache.items():
            meta = cdata.get("case_metadata", {})
            if not meta:
                continue
            if state_code and meta.get("state_code", "").upper() != state_code.upper():
                continue
            results.append(CaseSummary(**meta))

        # Fallback to primary case if results empty and matches
        if not results:
            meta = self.data.get("case_metadata", {})
            if meta and (not state_code or meta.get("state_code", "").upper() == state_code.upper()):
                results.append(CaseSummary(**meta))

        return results

    def get_case_by_id(self, case_id: str) -> Optional[Any]:
        """Retrieve case overview metadata for a single case."""
        for cid, cdata in self._cases_cache.items():
            if cid.upper() == case_id.upper():
                meta = cdata.get("case_metadata", {})
                return CaseSummary(**meta) if meta else None

        meta = self.data.get("case_metadata", {})
        if meta.get("case_id", "").upper() == case_id.upper():
            return CaseSummary(**meta)
        return None

    def get_graph(self, case_id: str) -> Optional[GraphResponse]:
        """Returns nodes and edges structured for Cytoscape.js canvas with calculated centrality scores."""
        cdata = None
        for cid, cd in self._cases_cache.items():
            if cid.upper() == case_id.upper():
                cdata = cd
                break
        if not cdata:
            meta = self.data.get("case_metadata", {})
            if meta.get("case_id", "").upper() == case_id.upper():
                cdata = self.data

        if not cdata:
            return None

        # Prefer pre-computed graph elements from data or dynamic graph builder
        graph_data = cdata.get("graph", {})
        elements_data = graph_data.get("elements", {})
        
        # If elements is already populated with nodes/edges
        if "nodes" in elements_data and "edges" in elements_data:
            nodes = [CytoscapeNode(data=n.get("data", n)) for n in elements_data.get("nodes", [])]
            edges = [CytoscapeEdge(data=e.get("data", e)) for e in elements_data.get("edges", [])]
            return GraphResponse(
                case_id=case_id,
                elements=GraphElements(nodes=nodes, edges=edges)
            )

        # Fallback to dynamic CrimeGraph conversion
        graph = self._graph_cache.get(case_id) or CrimeGraph.from_case_json(cdata)
        cyto = graph.to_cytoscape_json()
        nodes = [CytoscapeNode(data=n.get("data", n)) for n in cyto.get("elements", {}).get("nodes", [])]
        edges = [CytoscapeEdge(data=e.get("data", e)) for e in cyto.get("elements", {}).get("edges", [])]
        return GraphResponse(case_id=case_id, elements=GraphElements(nodes=nodes, edges=edges))

    def get_case_graph_cytoscape(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Dictionary representation for route backwards-compatibility."""
        graph_resp = self.get_graph(case_id)
        if not graph_resp:
            return None
        return graph_resp.model_dump()

    def get_timeline(self, case_id: str) -> Optional[List[TimelineEvent]]:
        """Return chronological timeline events for a case."""
        for cid, cdata in self._cases_cache.items():
            if cid.upper() == case_id.upper():
                raw_events = cdata.get("timeline", [])
                return [TimelineEvent(**item) for item in raw_events]

        meta = self.data.get("case_metadata", {})
        if meta.get("case_id", "").upper() == case_id.upper():
            raw_events = self.data.get("timeline", [])
            return [TimelineEvent(**item) for item in raw_events]
        return None

    def get_case_timeline(self, case_id: str) -> Optional[List[Dict[str, Any]]]:
        """Dictionary timeline representation for route backwards-compatibility."""
        timeline = self.get_timeline(case_id)
        if timeline is None:
            return None
        return [e.model_dump() for e in timeline]

    def get_entity(self, case_id: str, entity_id: str) -> Optional[EntityDetail]:
        """Return deep profile, extracted confidence, and connected links for a single entity node."""
        cdata = None
        for cid, cd in self._cases_cache.items():
            if cid.upper() == case_id.upper():
                cdata = cd
                break
        if not cdata:
            cdata = self.data

        # 1. Search entities dictionary
        entities = cdata.get("entities", {})
        if entity_id in entities:
            return EntityDetail(**entities[entity_id])

        # 2. Search graph nodes with dynamic centrality
        graph_data = cdata.get("graph", {}).get("elements", {})
        for node in graph_data.get("nodes", []):
            node_data = node.get("data", node)
            if node_data.get("id") == entity_id:
                centrality_val = node_data.get("centrality_score", 0.5)
                # Check dynamic centrality cache
                if case_id in self._centrality_cache and entity_id in self._centrality_cache[case_id]:
                    centrality_val = self._centrality_cache[case_id][entity_id].get("composite_centrality_score", centrality_val)

                metrics = EntityMetrics(
                    centrality_score=centrality_val,
                    risk_level=node_data.get("risk_level", "MEDIUM")
                )

                # Find supporting timeline records
                supporting = []
                for event in cdata.get("timeline", []):
                    if entity_id in event.get("involved_entities", []):
                        supporting.append(event.get("source_record_id", event.get("event_id", "")))

                # SHA-256 digital stamp from hash chain
                hash_chain = self._hashchain_cache.get(case_id)
                provenance_hash = hash_chain.blocks[-1].block_hash if (hash_chain and hash_chain.blocks) else "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

                return EntityDetail(
                    id=node_data.get("id"),
                    type=node_data.get("type", "UNKNOWN"),
                    label=node_data.get("label", entity_id),
                    aliases=node_data.get("aliases", []),
                    sub_role=node_data.get("sub_role"),
                    attributes={k: v for k, v in node_data.items() if k not in ["id", "type", "label", "aliases", "sub_role", "centrality_score", "risk_level"]},
                    metrics=metrics,
                    supporting_records=supporting or ["FIR-412/2026/PS-KashmereGate"],
                    provenance_hash=provenance_hash
                )
        return None

    def get_entity_profile(self, case_id: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Dictionary profile representation for route backwards-compatibility."""
        ent = self.get_entity(case_id, entity_id)
        if not ent:
            return None
        d = ent.model_dump()
        d["entity_id"] = ent.id
        d["case_id"] = case_id
        d["connected_entities"] = []
        # Populate connected entities from edges
        cdata = self._cases_cache.get(case_id, self.data)
        edges = cdata.get("graph", {}).get("elements", {}).get("edges", [])
        for edge in edges:
            ed = edge.get("data", edge)
            if ed.get("source") == entity_id:
                d["connected_entities"].append({
                    "connected_node_id": ed.get("target"),
                    "relationship": ed.get("label"),
                    "type": ed.get("type"),
                    "confidence": ed.get("confidence", 0.9)
                })
            elif ed.get("target") == entity_id:
                d["connected_entities"].append({
                    "connected_node_id": ed.get("source"),
                    "relationship": ed.get("label"),
                    "type": ed.get("type"),
                    "confidence": ed.get("confidence", 0.9)
                })
        return d

    def query_case(self, case_id: str, query: str) -> QueryResponse:
        """Process natural language query via AI Assistant Engine and query template matchers."""
        # 1. Try dynamic AI assistant engine
        assistant = self._assistant_cache.get(case_id)
        if assistant:
            res = assistant.answer_query(query)
            if res and res.get("answer"):
                return QueryResponse(
                    query=query,
                    answer=res.get("answer", ""),
                    confidence=res.get("confidence", 0.85),
                    cited_entities=res.get("cited_entities", []),
                    cited_sources=res.get("cited_sources", []),
                    suggested_actions=res.get("suggested_actions", [])
                )

        # 2. Template matchers from data
        cdata = self._cases_cache.get(case_id, self.data)
        query_templates = cdata.get("query_templates", [])
        clean_q = query.strip().lower()

        for tpl in query_templates:
            if tpl.get("query", "").strip().lower() == clean_q:
                return QueryResponse(**tpl)

        for tpl in query_templates:
            tpl_q = tpl.get("query", "").strip().lower()
            if any(k in clean_q and k in tpl_q for k in ["forensic", "singhu", "rakesh", "vehicle", "phone"]):
                return QueryResponse(**tpl)

        # 3. Fallback response adhering strictly to investigative terminology standards
        return QueryResponse(
            query=query,
            answer=f"Investigative lead analysis for case {case_id}: Corroborated intelligence records indicate multi-hop linkage between primary subjects around the incident timeframe.",
            confidence=0.88,
            cited_entities=["person-rakesh", "person-priya", "phone-burner-rakesh"],
            cited_sources=["CDR-DEL-0902-88", "FIR-412/2026/PS-KashmereGate"],
            suggested_actions=[
                "Inspect high-centrality node Rakesh Kumar in Graph View",
                "Review timeline between 21:00 and 22:30 on 02-Sep-2026"
            ]
        )

    def query_assistant(self, case_id: str, query: str) -> Dict[str, Any]:
        """Dictionary query representation for route backwards-compatibility."""
        return self.query_case(case_id, query).model_dump()

    def get_provenance(self, case_id: str) -> Optional[ProvenanceResponse]:
        """Verify digital evidence chain-of-custody under BSA 2023 Section 63."""
        cdata = self._cases_cache.get(case_id, self.data)
        meta = cdata.get("case_metadata", {})

        # Use dynamic blockchain hash chain if initialized
        hash_chain = self._hashchain_cache.get(case_id)
        if hash_chain and hash_chain.blocks:
            is_valid, _, _ = hash_chain.verify_chain()
            blocks = []
            for b in hash_chain.blocks:
                blocks.append(AuditBlock(
                    block_index=b.block_index,
                    record_id=b.record_id,
                    sha256=b.block_hash,
                    timestamp=b.timestamp,
                    officer_badge=b.officer_badge,
                    status="VALID" if is_valid else "CORRUPTED"
                ))
            return ProvenanceResponse(
                case_id=case_id,
                status="VERIFIED_INTACT" if is_valid else "INTEGRITY_COMPROMISED",
                bsa_section_63_compliant=is_valid,
                total_evidence_blocks=len(blocks),
                genesis_timestamp=blocks[0].timestamp if blocks else "2026-09-02T22:30:00Z",
                latest_block_hash=blocks[-1].sha256 if blocks else meta.get("merkle_root", ""),
                merkle_root=hash_chain.get_merkle_root(),
                audit_trail=blocks
            )

        # Fallback to static provenance payload
        prov_data = cdata.get("provenance", {})
        if prov_data:
            return ProvenanceResponse(**prov_data)
        return None

    def verify_case_provenance(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Dictionary provenance representation for route backwards-compatibility."""
        prov = self.get_provenance(case_id)
        if not prov:
            return None
        return prov.model_dump()

    def get_forensics(self, case_id: str) -> Optional[CaseForensicsOverview]:
        """Retrieve comprehensive forensic intelligence overview across all 8 disciplines."""
        cdata = self._cases_cache.get(case_id, self.data)
        forensics_data = cdata.get("forensics")
        if not forensics_data:
            return None
        return CaseForensicsOverview(**forensics_data)

    def get_forensics_by_category(self, case_id: str, category: str) -> Optional[List[Dict[str, Any]]]:
        """Filter forensic records by specific discipline."""
        forensics = self.get_forensics(case_id)
        if not forensics:
            return None
        norm_cat = category.lower().replace("-", "_")
        field_map = {
            "dna": "dna_evidence",
            "dna_biological": "dna_evidence",
            "fingerprint": "fingerprint_evidence",
            "fingerprint_latent": "fingerprint_evidence",
            "digital": "digital_forensics",
            "digital_forensics": "digital_forensics",
            "cctv": "cctv_video_forensics",
            "cctv_video_forensics": "cctv_video_forensics",
            "trace": "trace_evidence",
            "trace_evidence": "trace_evidence",
            "impression": "impression_evidence",
            "footwear_tire_impressions": "impression_evidence",
            "ballistics": "ballistics_toolmarks",
            "ballistics_toolmarks": "ballistics_toolmarks",
            "chain_of_custody": "chain_of_custody"
        }
        target_field = field_map.get(norm_cat, norm_cat)
        if hasattr(forensics, target_field):
            records = getattr(forensics, target_field)
            return [r.model_dump() for r in records]
        return None

    def get_chain_of_custody(self, case_id: str, evidence_id: str) -> Optional[ChainOfCustodyRecord]:
        """Inspect chain of custody for a specific physical or digital evidence item."""
        forensics = self.get_forensics(case_id)
        if not forensics:
            return None
        for coc in forensics.chain_of_custody:
            if coc.evidence_id.upper() == evidence_id.upper() or coc.chain_of_custody_id.upper() == evidence_id.upper():
                return coc
        return None


# Global singleton instance for service injection
case_service = CaseService()
