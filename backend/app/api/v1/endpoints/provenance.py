from fastapi import APIRouter, HTTPException
from backend.app.models.provenance import ProvenanceResponse
from backend.app.services.case_service import case_service

router = APIRouter()

@router.get("/cases/{case_id}/provenance/verify", response_model=ProvenanceResponse, summary="BSA 2023 Sec 63 digital custody verification")
async def verify_provenance(case_id: str):
    """Returns cryptographic proof of evidence chain-of-custody, SHA-256 hashes, and Section 63 compliance status."""
    prov = case_service.get_provenance(case_id)
    if not prov:
        raise HTTPException(status_code=404, detail=f"Provenance records for case '{case_id}' not found")
    return prov

@router.post("/evidence/verify", response_model=ProvenanceResponse, summary="Direct evidence verification alias")
@router.get("/evidence/verify", response_model=ProvenanceResponse, summary="Direct evidence verification alias (GET)")
async def verify_evidence_alias(case_id: str = "DL-2026-0412"):
    """Direct alias for the evidence verification modal."""
    return await verify_provenance(case_id)
