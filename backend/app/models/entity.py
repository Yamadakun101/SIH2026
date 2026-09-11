from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class EntityMetrics(BaseModel):
    centrality_score: float
    degree: Optional[int] = None
    betweenness: Optional[float] = None
    risk_level: Optional[str] = None
    cluster_id: Optional[str] = None

class EntityDetail(BaseModel):
    id: str
    type: str
    label: str
    aliases: List[str] = []
    sub_role: Optional[str] = None
    attributes: Dict[str, Any] = {}
    metrics: EntityMetrics
    supporting_records: List[str] = []
    provenance_hash: Optional[str] = None
