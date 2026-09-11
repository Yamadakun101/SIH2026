import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Ensure root directory is on Python path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.config import settings
from backend.app.api.v1.api import api_router
from backend.app.security.security_headers import SecurityHeadersMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="KavachNet — AI-Powered Criminal Network Analysis & Evidence Provenance REST API (SIH 2026, PS #26189)",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Attach Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# Set up CORS middleware for Vite frontend and local tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router under /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
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
            "forensic_intelligence_engine"
        ]
    }


@app.get("/api", tags=["Root"])
async def api_root():
    """Root API info endpoint with documentation links"""
    return {
        "message": "Welcome to KavachNet Intelligence API",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR,
        "compliance": "Bharatiya Sakshya Adhiniyam (BSA) 2023, Section 63"
    }


# Mount Static Frontend
frontend_dir = ROOT_DIR / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
