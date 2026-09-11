"""
KavachNet — AI-Powered Criminal Network Analysis System
Backend Entrypoint (FastAPI Application)
SIH 2026 — Problem Statement #26189
"""

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure root directory is on Python path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.api.routes import router as api_router

app = FastAPI(
    title="KavachNet Intelligence API",
    description=(
        "AI-Powered Criminal Network Analysis & Provenance Engine. "
        "Complies with Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend clients (React / Vite / Cytoscape)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router)


@app.get("/", tags=["System"])
def root():
    return {
        "system": "KavachNet Intelligence Engine",
        "version": "1.0.0",
        "status": "OPERATIONAL",
        "compliance": "Bharatiya Sakshya Adhiniyam (BSA) 2023, Section 63",
        "documentation": "/docs"
    }


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "HEALTHY",
        "active_modules": [
            "ai_entity_resolution",
            "centrality_analytics",
            "syndicate_clustering",
            "bsa_section_63_hash_chain"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
