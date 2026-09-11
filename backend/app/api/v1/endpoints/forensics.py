from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from backend.app.models.forensics import CaseForensicsOverview, ChainOfCustodyRecord
from backend.app.services.case_service import case_service

router = APIRouter()

@router.get(
    "/cases/{case_id}/forensics",
    response_model=CaseForensicsOverview,
    summary="Retrieve complete multi-category forensic intelligence overview"
)
@router.get(
    "/cases/{case_id}/forensics/overview",
    response_model=CaseForensicsOverview,
    summary="Retrieve complete multi-category forensic intelligence overview (alias)"
)
async def get_case_forensics(case_id: str):
    """
    Returns full multi-source forensic evidence profiles across all 8 disciplines:
    DNA/Biological, Fingerprint, Digital/Mobile, CCTV/Video, Trace, Impressions,
    Ballistics/Toolmarks, and Chain of Custody.
    """
    forensics = case_service.get_forensics(case_id)
    if not forensics:
        raise HTTPException(
            status_code=404,
            detail=f"Forensic records for case '{case_id}' not found"
        )
    return forensics

@router.get(
    "/cases/{case_id}/forensics/categories/{category}",
    response_model=List[Dict[str, Any]],
    summary="Retrieve forensic records filtered by specific discipline category"
)
async def get_forensic_category(case_id: str, category: str):
    """
    Filters forensic records by discipline:
    - 'dna' or 'dna_biological'
    - 'fingerprint' or 'fingerprint_latent'
    - 'digital' or 'digital_forensics'
    - 'cctv' or 'cctv_video_forensics'
    - 'trace' or 'trace_evidence'
    - 'impression' or 'footwear_tire_impressions'
    - 'ballistics' or 'ballistics_toolmarks'
    - 'chain_of_custody'
    """
    records = case_service.get_forensics_by_category(case_id, category)
    if records is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category}' not found for case '{case_id}'"
        )
    return records

@router.get(
    "/cases/{case_id}/forensics/chain-of-custody/{evidence_id}",
    response_model=ChainOfCustodyRecord,
    summary="Retrieve sequential chain of custody ledger and BSA 2023 Sec 63 status"
)
async def get_evidence_chain_of_custody(case_id: str, evidence_id: str):
    """
    Returns verified chain of custody transfer events, original and current SHA-256 hashes,
    officer badge identifiers, and storage vaults under BSA 2023 Section 63.
    """
    record = case_service.get_chain_of_custody(case_id, evidence_id)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Chain of custody record for evidence '{evidence_id}' in case '{case_id}' not found"
        )
    return record
