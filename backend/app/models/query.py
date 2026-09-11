from typing import List
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    answer: str
    confidence: float
    cited_entities: List[str]
    cited_sources: List[str]
    suggested_actions: List[str]
