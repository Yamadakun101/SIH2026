"""
Pydantic Models for KavachNet REST API
Complies strictly with docs/API_CONTRACT.md and docs/DATA_SCHEMA.md
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class StateSummary(BaseModel):
    state_code: str
    state_name: str
    active_cases_count: int
    high_risk_alerts: int
    lat: float
    lng: float


class CaseSummary(BaseModel):
    case_id: str
    title: str
    state_code: str
    status: str
    priority: str
    incident_date: str
    lead_agency: str
    fir_number: str
    total_entities_identified: int
    total_evidence_records: int
    summary: str


class CaseMetadata(BaseModel):
    case_id: str
    title: str
    state_code: str
    state_name: str
    incident_date: str
    lead_agency: str
    fir_number: str
    status: str
    priority: str
    summary: str
    bsa_section_63_verified: bool
    merkle_root: str


class NodeData(BaseModel):
    id: str
    label: str
    type: str
    sub_role: Optional[str] = None
    centrality_score: float = 0.0
    risk_level: Optional[str] = None
    evidence_count: int = 0
    status: Optional[str] = None
    icon: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class NodeElement(BaseModel):
    data: NodeData


class EdgeData(BaseModel):
    id: str
    source: str
    target: str
    label: str
    type: Optional[str] = None
    confidence: float
    interaction_count: Optional[int] = 1
    category: Optional[str] = None
    evidence_source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class EdgeElement(BaseModel):
    data: EdgeData


class GraphElements(BaseModel):
    nodes: List[NodeElement]
    edges: List[EdgeElement]


class GraphResponse(BaseModel):
    case_id: str
    elements: GraphElements


class TimelineEvent(BaseModel):
    event_id: str
    timestamp: str
    title: str
    category: str
    source_record_id: str
    location: str
    involved_entities: List[str]
    description: str
    confidence: float


class EntityProfileResponse(BaseModel):
    entity_id: str
    case_id: str
    label: str
    type: str
    sub_role: Optional[str] = None
    centrality_score: float
    risk_level: Optional[str] = None
    evidence_count: int
    details: Dict[str, Any] = Field(default_factory=dict)
    connected_entities: List[Dict[str, Any]] = Field(default_factory=list)
    source_records: List[Dict[str, Any]] = Field(default_factory=list)
    provenance_hash: str


class QueryRequest(BaseModel):
    query: str
    case_id: Optional[str] = None


class QueryResponse(BaseModel):
    query: str
    answer: str
    confidence: float
    cited_entities: List[str]
    cited_sources: List[str]
    suggested_actions: List[str]


class AuditBlock(BaseModel):
    block_index: int
    record_id: str
    sha256: str
    timestamp: str
    officer_badge: str
    status: str


class ProvenanceVerificationResponse(BaseModel):
    case_id: str
    status: str
    bsa_section_63_compliant: bool
    total_evidence_blocks: int
    genesis_timestamp: str
    latest_block_hash: str
    merkle_root: str
    audit_trail: List[AuditBlock]
