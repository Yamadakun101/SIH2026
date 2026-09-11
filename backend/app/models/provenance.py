from typing import List
from pydantic import BaseModel

class AuditBlock(BaseModel):
    block_index: int
    record_id: str
    sha256: str
    timestamp: str
    officer_badge: str
    status: str

class ProvenanceResponse(BaseModel):
    case_id: str
    status: str
    bsa_section_63_compliant: bool
    total_evidence_blocks: int
    genesis_timestamp: str
    latest_block_hash: str
    merkle_root: str
    audit_trail: List[AuditBlock]
