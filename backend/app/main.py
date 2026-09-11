from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
async def health_check():
    """System health check endpoint"""
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

@app.get("/", tags=["Root"])
async def root():
    """Root info endpoint with documentation links"""
    return {
        "message": "Welcome to KavachNet Intelligence API",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR,
        "compliance": "Bharatiya Sakshya Adhiniyam (BSA) 2023, Section 63"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
