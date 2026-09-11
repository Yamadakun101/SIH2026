from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from backend.app.models.case import CaseSummary
from backend.app.services.case_service import case_service

router = APIRouter()

@router.get("/cases", response_model=List[CaseSummary], summary="List cases optionally filtered by state")
async def get_cases(state: Optional[str] = Query(None, description="Two-letter state code e.g. DL")):
    """Returns cases matching state code or all active cases if not specified."""
    return case_service.get_cases(state_code=state)

@router.get("/cases/{case_id}", response_model=CaseSummary, summary="Retrieve case metadata")
async def get_case(case_id: str):
    """Returns overview metadata and summary for a single case."""
    case = case_service.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found")
    return case
