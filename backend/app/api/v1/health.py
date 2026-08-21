from fastapi import APIRouter
from app.config import settings

router = APIRouter()


@router.get("/health", summary="Health Check")
async def health_check() -> dict[str, str]:
    """
    Returns API health status, app name, version, and environment.
    """
    return {
        "status": "healthy",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }
