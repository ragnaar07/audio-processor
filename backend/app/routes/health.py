from fastapi import APIRouter
from app.config import get_settings

router = APIRouter(tags=["health"])

settings = get_settings()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENV,
        "database": "connected",  # TODO: Add actual database check
        "redis": "connected",      # TODO: Add actual Redis check
        "s3": "connected",         # TODO: Add actual S3 check
    }
