from typing import List
from fastapi import APIRouter
from backend.app.models.state import StateItem
from backend.app.services.case_service import case_service

router = APIRouter()

@router.get("/states", response_model=List[StateItem], summary="List states with active case statistics")
async def get_states():
    """Returns list of Indian states with active case count, high-risk alert count, and geo coordinates."""
    return case_service.get_states()
