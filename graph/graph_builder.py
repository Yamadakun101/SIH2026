"""
Crime Knowledge Graph Builder
Builds, validates, and transforms multi-source crime networks into Cytoscape.js compatible structures.
"""

import json
from typing import Any, Dict, List, Optional, Set


class GraphNode:
    """Represents an entity node in the criminal network graph."""

    def __init__(
        self,
        node_id: str,
        label: str,
        node_type: str,
        sub_role: str = "ASSOCIATE_NODE",
        centrality_score: float = 0.5,
        risk_level: str = "MEDIUM",
        evidence_count: int = 1,
        status: Optional[str] = None,
        icon: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.node_id = node_id
        self.label = label
        self.node_type = node_type.upper()
        self.sub_role = sub_role
        self.centrality_score = centrality_score
        self.risk_level = risk_level.upper()
        self.evidence_count = evidence_count
        self.status = status or "ACTIVE"
        self.icon = icon or self._default_icon_for_type(self.node_type)
        self.details = details or {}

    @staticmethod
    def _default_icon_for_type(node_type: str) -> str:
        icon_map = {
            "PERSON": "user",
            "PHONE": "phone",
            "VEHICLE": "car",
            "BANK_ACCOUNT": "credit-card",
            "LOCATION": "map-pin",
            "ORGANIZATION": "briefcase",
        }
        return icon_map.get(node_type, "circle")

    def to_cytoscape_data(self) -> Dict[str, Any]:
        """Format node payload matching API_CONTRACT.md Cytoscape.js format."""
        data = {
            "id": self.node_id,
            "label": self.label,
            "type": self.node_type,
            "sub_role": self.sub_role,
            "centrality_score": round(self.centrality_score, 3),
            "risk_level": self.risk_level,
            "evidence_count": self.evidence_count,
            "status": self.status,
            "icon": self.icon,
        }
        if self.details:
            data["details"] = self.details
        return {"data": data}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "label": self.label,
            "type": self.node_type,
            "sub_role": self.sub_role,
            "centrality_score": self.centrality_score,
            "risk_level": self.risk_level,
            "evidence_count": self.evidence_count,
            "status": self.status,
            "icon": self.icon,
            "details": self.details,
        }


class GraphEdge:
    """Represents a relationship edge between two entities."""

    def __init__(
        self,
        edge_id: str,
        source: str,
        target: str,
        label: str,
        edge_type: str,
        confidence: float = 0.9,
        category: Optional[str] = None,
        interaction_count: int = 1,
        evidence_source: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.edge_id = edge_id
        self.source = source
        self.target = target
        self.label = label
        self.edge_type = edge_type
        self.confidence = confidence
        self.category = category or self._infer_category(edge_type)
        self.interaction_count = interaction_count
        self.evidence_source = evidence_source
        self.metadata = metadata or {}

    @staticmethod
    def _infer_category(edge_type: str) -> str:
        et = edge_type.upper()
        if any(x in et for x in ["CALL", "SUBSCRIBER", "SMS", "SIM", "CDR"]):
            return "TELECOM"
        if any(x in et for x in ["TRANSFER", "BANK", "UPI", "PAYMENT", "ACCOUNT"]):
            return "FINANCIAL"
        if any(x in et for x in ["SIGHTED", "TOLL", "ANPR", "CAMERA", "CCTV", "TRANSIT"]):
            return "SURVEILLANCE"
        if any(x in et for x in ["LOCATED", "TOWER", "CO_LOCATED"]):
            return "GEOLOCATION"
        return "ASSOCIATION"

    def to_cytoscape_data(self) -> Dict[str, Any]:
        """Format edge payload matching API_CONTRACT.md Cytoscape.js format."""
        data = {
            "id": self.edge_id,
            "source": self.source,
            "target": self.target,
            "label": self.label,
            "type": self.edge_type,
            "confidence": round(self.confidence, 2),
            "interaction_count": self.interaction_count,
            "category": self.category,
        }
        if self.evidence_source:
            data["evidence_source"] = self.evidence_source
        if self.metadata:
            data["metadata"] = self.metadata
        return {"data": data}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.edge_id,
            "source": self.source,
            "target": self.target,
            "label": self.label,
            "type": self.edge_type,
            "confidence": self.confidence,
            "category": self.category,
            "interaction_count": self.interaction_count,
            "evidence_source": self.evidence_source,
            "metadata": self.metadata,
        }


class CrimeGraph:
    """Graph structure managing entity nodes, relational edges, and neighborhood traversals."""

    def __init__(self, case_id: str = "DL-2026-0412"):
        self.case_id = case_id
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, GraphEdge] = {}
        self.adjacency: Dict[str, Set[str]] = {}  # Undirected adjacency for centrality
        self.directed_adjacency: Dict[str, Set[str]] = {}  # Directed outgoing

    def add_node(self, node: GraphNode) -> None:
        """Add or update an entity node."""
        self.nodes[node.node_id] = node
        if node.node_id not in self.adjacency:
            self.adjacency[node.node_id] = set()
            self.directed_adjacency[node.node_id] = set()

    def add_edge(self, edge: GraphEdge) -> None:
        """Add a relationship edge between two existing or auto-created nodes."""
        if edge.source not in self.nodes:
            self.add_node(GraphNode(node_id=edge.source, label=edge.source, node_type="UNKNOWN"))
        if edge.target not in self.nodes:
            self.add_node(GraphNode(node_id=edge.target, label=edge.target, node_type="UNKNOWN"))

        self.edges[edge.edge_id] = edge
        self.adjacency[edge.source].add(edge.target)
        self.adjacency[edge.target].add(edge.source)
        self.directed_adjacency[edge.source].add(edge.target)

    def get_neighbors(self, node_id: str) -> List[str]:
        """Get connected neighbor node IDs."""
        return list(self.adjacency.get(node_id, set()))

    def get_incident_edges(self, node_id: str) -> List[GraphEdge]:
        """Get all edges connected to a node."""
        return [
            e for e in self.edges.values()
            if e.source == node_id or e.target == node_id
        ]

    def to_cytoscape_json(self) -> Dict[str, Any]:
        """Format full graph for GET /api/v1/cases/{case_id}/graph."""
        return {
            "case_id": self.case_id,
            "elements": {
                "nodes": [n.to_cytoscape_data() for n in self.nodes.values()],
                "edges": [e.to_cytoscape_data() for e in self.edges.values()],
            }
        }

    @classmethod
    def from_case_json(cls, data_or_path: Any) -> "CrimeGraph":
        """Load graph from JSON dictionary or filepath, supporting both flat and Cytoscape elements formats."""
        if hasattr(data_or_path, "exists") or isinstance(data_or_path, str):
            with open(str(data_or_path), "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = data_or_path

        case_id = data.get("case_metadata", {}).get("case_id", "CASE-UNKNOWN")
        graph = cls(case_id=case_id)

        raw_graph = data.get("graph", {})
        elements = raw_graph.get("elements", {})
        raw_nodes = elements.get("nodes") if "nodes" in elements else raw_graph.get("nodes", [])
        raw_edges = elements.get("edges") if "edges" in elements else raw_graph.get("edges", [])

        for n_item in raw_nodes:
            n_data = n_item.get("data", n_item)
            node_id = n_data.get("id")
            if not node_id:
                continue
            node = GraphNode(
                node_id=node_id,
                label=n_data.get("label", node_id),
                node_type=n_data.get("type", "UNKNOWN"),
                sub_role=n_data.get("sub_role", "ASSOCIATE_NODE"),
                centrality_score=n_data.get("centrality_score", 0.5),
                risk_level=n_data.get("risk_level", "MEDIUM"),
                evidence_count=n_data.get("evidence_count", 1),
                details=n_data.get("details", {}),
            )
            graph.add_node(node)

        for e_item in raw_edges:
            e_data = e_item.get("data", e_item)
            edge_id = e_data.get("id")
            source = e_data.get("source")
            target = e_data.get("target")
            if not source or not target:
                continue
            edge = GraphEdge(
                edge_id=edge_id or f"edge-{source}-{target}",
                source=source,
                target=target,
                label=e_data.get("label", ""),
                edge_type=e_data.get("type", "ASSOCIATED_WITH"),
                confidence=e_data.get("confidence", 0.9),
                evidence_source=e_data.get("evidence_source"),
                metadata=e_data.get("metadata", {}),
            )
            graph.add_edge(edge)

        return graph
