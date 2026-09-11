from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    states,
    cases,
    graph,
    timeline,
    entities,
    query,
    provenance,
    auth,
    external,
    audit,
    forensics
)

api_router = APIRouter()

# Existing Endpoints (Untouched)
api_router.include_router(states.router, tags=["States"])
api_router.include_router(cases.router, tags=["Cases"])
api_router.include_router(graph.router, tags=["Knowledge Graph"])
api_router.include_router(timeline.router, tags=["Timeline"])
api_router.include_router(entities.router, tags=["Entities"])
api_router.include_router(query.router, tags=["AI Assistant"])
api_router.include_router(provenance.router, tags=["Evidence Provenance (BSA 2023)"])

# Security & External Data Integration Endpoints
api_router.include_router(auth.router, tags=["Authentication & Access Control"])
api_router.include_router(external.router, tags=["Secure External Data Integration"])
api_router.include_router(audit.router, tags=["Security Audit & Compliance"])

# Forensic Intelligence & Chain of Custody (BSA 2023)
api_router.include_router(forensics.router, tags=["Forensic Intelligence & Chain of Custody"])
