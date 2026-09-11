from typing import List
from fastapi import APIRouter, HTTPException
from backend.app.models.timeline import TimelineEvent
from backend.app.services.case_service import case_service

router = APIRouter()

@router.get("/cases/{case_id}/timeline", response_model=List[TimelineEvent], summary="Chronological event sequence")
async def get_timeline(case_id: str):
    """Returns chronological multi-source event sequence (CDRs, CCTV, Bank, FIR)."""
    timeline = case_service.get_timeline(case_id)
    if timeline is None:
        raise HTTPException(status_code=404, detail=f"Timeline for case '{case_id}' not found")
    return timeline
