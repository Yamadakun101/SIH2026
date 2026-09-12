from fastapi import APIRouter
from backend.app.models.query import QueryRequest, QueryResponse
from backend.app.services.case_service import case_service

router = APIRouter()

@router.post("/cases/{case_id}/query", response_model=QueryResponse, summary="AI investigative assistant query")
async def query_case(case_id: str, request: QueryRequest):
    """Processes natural language query on the case graph, returning explainable findings, cited entities, and sources."""
    return case_service.query_case(case_id, request.query)
