"""
FastAPI application entrypoint for the AI Resume Analyzer backend.
Configures CORS middleware and registers sub-routers for health, parsing, skills, and scoring.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.health import router as health_router
from app.api.v1.parser import router as parser_router
from app.api.v1.skills import router as skills_router
from app.api.v1.scoring import router as scoring_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Router Modules
app.include_router(health_router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(parser_router, prefix=settings.API_V1_STR, tags=["Resume Parser"])
app.include_router(skills_router, prefix=settings.API_V1_STR, tags=["Skill Analytics"])
app.include_router(scoring_router, prefix=settings.API_V1_STR, tags=["ATS Scoring Engine"])


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
    }
