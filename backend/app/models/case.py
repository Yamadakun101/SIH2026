from typing import Optional
from pydantic import BaseModel

class CaseSummary(BaseModel):
    case_id: str
    title: str
    state_code: str
    state_name: Optional[str] = None
    status: str
    priority: str
    incident_date: str
    lead_agency: str
    fir_number: str
    total_entities_identified: int
    total_evidence_records: int
    summary: str
    bsa_section_63_verified: Optional[bool] = None
    merkle_root: Optional[str] = None
