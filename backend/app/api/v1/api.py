from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    states,
    cases,
    graph,
    timeline,
    entities,
    query,
    provenance
)

api_router = APIRouter()

api_router.include_router(states.router, tags=["States"])
api_router.include_router(cases.router, tags=["Cases"])
api_router.include_router(graph.router, tags=["Knowledge Graph"])
api_router.include_router(timeline.router, tags=["Timeline"])
api_router.include_router(entities.router, tags=["Entities"])
api_router.include_router(query.router, tags=["AI Assistant"])
api_router.include_router(provenance.router, tags=["Evidence Provenance (BSA 2023)"])
