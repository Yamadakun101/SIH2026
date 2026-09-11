"""
KavachNet — AI-Powered Criminal Network Analysis System
Backend Entrypoint (FastAPI Application)
SIH 2026 — Problem Statement #26189
"""

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure root directory is on Python path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.config import settings
from backend.app.api.v1.api import api_router as v1_api_router
from backend.app.api.routes import router as core_api_router
from backend.app.security.security_headers import SecurityHeadersMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "KavachNet — AI-Powered Criminal Network Analysis & Evidence Provenance REST API. "
        "Complies with Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63."
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. Attach Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# 2. Set up CORS middleware for Vite frontend, React clients, and Cytoscape
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount Modular V1 API Routers (Cases, Forensics, Auth, External, Audit)
app.include_router(v1_api_router, prefix=settings.API_V1_STR)

# 4. Mount Core API Route Aliases (Assistant & Evidence verification shortcuts)
app.include_router(core_api_router)


@app.get("/health", tags=["System"])
async def health_check():
    """System health check endpoint"""
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "active_modules": [
            "ai_entity_resolution",
            "centrality_analytics",
            "syndicate_clustering",
            "bsa_section_63_hash_chain",
            "zero_trust_security",
            "forensics_eight_disciplines"
        ]
    }


@app.get("/", tags=["System"])
async def root():
    """Root info endpoint with documentation links"""
    return {
        "system": "KavachNet Intelligence Engine",
        "version": settings.VERSION,
        "status": "OPERATIONAL",
        "compliance": "Bharatiya Sakshya Adhiniyam (BSA) 2023, Section 63",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
