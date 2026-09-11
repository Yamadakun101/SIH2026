"""
FastAPI Route Controllers for KavachNet REST API
Strictly adheres to docs/API_CONTRACT.md
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.models import (
    CaseSummary,
    EntityProfileResponse,
    GraphResponse,
    ProvenanceVerificationResponse,
    QueryRequest,
    QueryResponse,
    StateSummary,
    TimelineEvent,
)
from backend.app.services.case_service import case_service

router = APIRouter(prefix="/api/v1", tags=["KavachNet Core API"])


@router.get(
    "/states",
    response_model=List[StateSummary],
    summary="List states with active case statistics",
    description="Returns high-level statistics for all states mapped in the command center."
)
def get_states() -> List[StateSummary]:
    return case_service.get_states()


@router.get(
    "/cases",
    response_model=List[CaseSummary],
    summary="List investigative cases",
    description="Retrieve cases, optionally filtered by two-letter state code (e.g., 'DL', 'MH')."
)
def get_cases(state: Optional[str] = Query(None, description="Two-letter state code")) -> List[CaseSummary]:
    return case_service.get_cases(state_code=state)


@router.get(
    "/cases/{case_id}",
    summary="Get case overview metadata",
    description="Returns detailed overview metadata, lead agency, FIR reference, and status for a single case."
)
def get_case(case_id: str) -> Dict[str, Any]:
    case = case_service.get_case_by_id(case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID '{case_id}' not found."
        )
    return case.get("case_metadata", {})


@router.get(
    "/cases/{case_id}/graph",
    response_model=GraphResponse,
    summary="Get Cytoscape-formatted knowledge graph",
    description="Returns nodes with computed centrality scores and labeled edges for Cytoscape.js canvas rendering."
)
def get_case_graph(case_id: str) -> GraphResponse:
    graph_payload = case_service.get_case_graph_cytoscape(case_id)
    if not graph_payload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Graph for Case ID '{case_id}' not found."
        )
    return graph_payload


@router.get(
    "/cases/{case_id}/timeline",
    response_model=List[TimelineEvent],
    summary="Get chronological timeline events",
    description="Returns scrubbable sequence of multi-source timeline events for chronological playback."
)
def get_case_timeline(case_id: str) -> List[TimelineEvent]:
    timeline = case_service.get_case_timeline(case_id)
    if timeline is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timeline for Case ID '{case_id}' not found."
        )
    return timeline


@router.get(
    "/cases/{case_id}/entities/{entity_id}",
    response_model=EntityProfileResponse,
    summary="Get deep profile for an entity node",
    description="Inspect extracted details, associated relationships, source evidence excerpts, and SHA-256 stamp."
)
def get_entity_profile(case_id: str, entity_id: str) -> EntityProfileResponse:
    profile = case_service.get_entity_profile(case_id=case_id, entity_id=entity_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity '{entity_id}' not found in Case '{case_id}'."
        )
    return profile


@router.post(
    "/cases/{case_id}/query",
    response_model=QueryResponse,
    summary="Query AI investigative assistant for a case",
    description="Process natural language questions about suspects, phone numbers, vehicles, or timelines."
)
def query_case_assistant(case_id: str, request: QueryRequest) -> QueryResponse:
    result = case_service.query_assistant(case_id=case_id, query=request.query)
    return result


@router.post(
    "/assistant/query",
    response_model=QueryResponse,
    summary="Global AI assistant query endpoint",
    description="Query assistant with optional case_id in the request payload."
)
def query_global_assistant(request: QueryRequest) -> QueryResponse:
    case_id = request.case_id or "DL-2026-0412"
    result = case_service.query_assistant(case_id=case_id, query=request.query)
    return result


@router.get(
    "/cases/{case_id}/provenance/verify",
    response_model=ProvenanceVerificationResponse,
    summary="Verify digital evidence chain-of-custody",
    description="Performs cryptographic verification of the SHA-256 Merkle chain under BSA 2023 Section 63."
)
def verify_provenance(case_id: str) -> ProvenanceVerificationResponse:
    verification = case_service.verify_case_provenance(case_id)
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence ledger for Case ID '{case_id}' not found."
        )
    return verification


@router.post(
    "/evidence/verify",
    response_model=ProvenanceVerificationResponse,
    summary="Verify evidence endpoint alias",
    description="Direct verification endpoint for the evidence integrity modal."
)
def verify_evidence_alias(case_id: Optional[str] = Query("DL-2026-0412")) -> ProvenanceVerificationResponse:
    verification = case_service.verify_case_provenance(case_id)
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence ledger for Case ID '{case_id}' not found."
        )
    return verification
