from fastapi import APIRouter, HTTPException
from backend.app.models.entity import EntityDetail
from backend.app.services.case_service import case_service

router = APIRouter()

@router.get("/cases/{case_id}/entities/{entity_id}", response_model=EntityDetail, summary="Detailed entity profile and dossier")
async def get_entity(case_id: str, entity_id: str):
    """Returns detailed profile, attributes, centrality metrics, and supporting records for a specific node."""
    entity = case_service.get_entity(case_id, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity '{entity_id}' not found in case '{case_id}'")
    return entity
