from typing import Any, Dict, List
from pydantic import BaseModel

class CytoscapeNode(BaseModel):
    data: Dict[str, Any]

class CytoscapeEdge(BaseModel):
    data: Dict[str, Any]

class GraphElements(BaseModel):
    nodes: List[CytoscapeNode]
    edges: List[CytoscapeEdge]

class GraphResponse(BaseModel):
    case_id: str
    elements: GraphElements
