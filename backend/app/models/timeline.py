from typing import List, Optional
from pydantic import BaseModel

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
