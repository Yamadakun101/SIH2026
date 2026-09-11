from fastapi import APIRouter, HTTPException
from backend.app.models.graph import GraphResponse
from backend.app.services.case_service import case_service

router = APIRouter()

@router.get("/cases/{case_id}/graph", response_model=GraphResponse, summary="Cytoscape-formatted graph elements")
async def get_graph(case_id: str):
    """Returns nodes and edges structured directly for Cytoscape.js canvas with centrality scores."""
    graph = case_service.get_graph(case_id)
    if not graph:
        raise HTTPException(status_code=404, detail=f"Graph for case '{case_id}' not found")
    return graph
