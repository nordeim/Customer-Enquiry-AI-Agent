"""
Health Check Endpoints

Provides health and readiness endpoints for monitoring
and container orchestration systems.
"""

from datetime import datetime, timezone
from typing import Any

import redis.asyncio as redis
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from qdrant_client import QdrantClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.dependencies import get_session, get_redis, get_qdrant
from app.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter()


class HealthStatus(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    version: str
    environment: str


class ReadinessStatus(BaseModel):
    """Readiness check response model."""
    status: str
    timestamp: str
    checks: dict[str, Any]


@router.get(
    "/health",
    response_model=HealthStatus,
    summary="Health Check",
    description="Simple health check endpoint for load balancers",
)
async def health_check() -> HealthStatus:
    """
    Basic health check.
    
    Returns 200 OK if the application is running.
    Does not check dependencies.
    """
    return HealthStatus(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version="1.0.0",
        environment=settings.app_env,
    )


@router.get(
    "/ready",
    response_model=ReadinessStatus,
    summary="Readiness Check",
    description="Checks all dependencies are available",
)
async def readiness_check(
    session: AsyncSession = Depends(get_session),
    redis_client: redis.Redis = Depends(get_redis),
    qdrant_client: QdrantClient = Depends(get_qdrant),
) -> ReadinessStatus:
    """
    Comprehensive readiness check.
    
    Verifies all critical dependencies:
    - PostgreSQL database
    - Redis cache
    - Qdrant vector database
    """
    checks: dict[str, Any] = {}
    all_healthy = True
    
    # Check PostgreSQL
    try:
        await session.execute(text("SELECT 1"))
        checks["postgresql"] = {"status": "healthy"}
    except Exception as e:
        logger.error("postgresql_health_check_failed", error=str(e))
        checks["postgresql"] = {"status": "unhealthy", "error": str(e)}
        all_healthy = False
    
    # Check Redis
    try:
        await redis_client.ping()
        checks["redis"] = {"status": "healthy"}
    except Exception as e:
        logger.error("redis_health_check_failed", error=str(e))
        checks["redis"] = {"status": "unhealthy", "error": str(e)}
        all_healthy = False
    
    # Check Qdrant
    try:
        qdrant_client.get_collections()
        checks["qdrant"] = {"status": "healthy"}
    except Exception as e:
        logger.error("qdrant_health_check_failed", error=str(e))
        checks["qdrant"] = {"status": "unhealthy", "error": str(e)}
        all_healthy = False
    
    response = ReadinessStatus(
        status="ready" if all_healthy else "not_ready",
        timestamp=datetime.now(timezone.utc).isoformat(),
        checks=checks,
    )
    
    if not all_healthy:
        # Return 503 if any dependency is unhealthy
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=response.model_dump(),
        )
    
    return response


@router.get(
    "/info",
    summary="Application Info",
    description="Returns application metadata",
)
async def app_info() -> dict[str, Any]:
    """Return application information."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "environment": settings.app_env,
        "debug": settings.debug,
        "docs_url": "/docs" if settings.is_development else None,
    }
