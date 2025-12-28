"""
Health Check Routes

Provides endpoints for monitoring application health and readiness.
"""

from datetime import datetime, timezone
from typing import Any

import structlog
from fastapi import APIRouter, status
from pydantic import BaseModel, Field
from qdrant_client import AsyncQdrantClient

from app.config import get_settings
from app.dependencies import get_db_session, get_qdrant_client, get_redis_client

router = APIRouter()
logger = structlog.get_logger()


class HealthStatus(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Overall health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Environment name")
    checks: dict[str, Any] = Field(default_factory=dict, description="Individual component checks")


class ComponentHealth(BaseModel):
    """Individual component health status."""
    
    status: str
    latency_ms: float | None = None
    error: str | None = None


@router.get(
    "/health",
    response_model=HealthStatus,
    summary="Health Check",
    description="Basic health check endpoint for load balancers and monitoring.",
)
async def health_check() -> HealthStatus:
    """
    Basic health check endpoint.
    
    Returns a simple health status without checking dependencies.
    Suitable for load balancer health probes.
    """
    settings = get_settings()
    
    return HealthStatus(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        version="0.1.0",
        environment=settings.app_env,
        checks={},
    )


@router.get(
    "/health/ready",
    response_model=HealthStatus,
    summary="Readiness Check",
    description="Comprehensive readiness check including all dependencies.",
    responses={
        503: {"description": "Service not ready"},
    },
)
async def readiness_check() -> HealthStatus:
    """
    Comprehensive readiness check.
    
    Checks all critical dependencies:
    - PostgreSQL database
    - Redis cache
    - Qdrant vector database
    
    Returns 503 if any dependency is unhealthy.
    """
    import time
    
    settings = get_settings()
    checks: dict[str, Any] = {}
    all_healthy = True
    
    # Check PostgreSQL
    try:
        start = time.perf_counter()
        async for session in get_db_session():
            await session.execute("SELECT 1")
        latency = (time.perf_counter() - start) * 1000
        checks["postgresql"] = ComponentHealth(status="healthy", latency_ms=round(latency, 2))
    except Exception as e:
        logger.error("PostgreSQL health check failed", error=str(e))
        checks["postgresql"] = ComponentHealth(status="unhealthy", error=str(e))
        all_healthy = False
    
    # Check Redis
    try:
        start = time.perf_counter()
        async for client in get_redis_client():
            await client.ping()
        latency = (time.perf_counter() - start) * 1000
        checks["redis"] = ComponentHealth(status="healthy", latency_ms=round(latency, 2))
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))
        checks["redis"] = ComponentHealth(status="unhealthy", error=str(e))
        all_healthy = False
    
    # Check Qdrant
    try:
        start = time.perf_counter()
        qdrant = await get_qdrant_client()
        await qdrant.get_collections()
        latency = (time.perf_counter() - start) * 1000
        checks["qdrant"] = ComponentHealth(status="healthy", latency_ms=round(latency, 2))
    except Exception as e:
        logger.error("Qdrant health check failed", error=str(e))
        checks["qdrant"] = ComponentHealth(status="unhealthy", error=str(e))
        all_healthy = False
    
    status_value = "healthy" if all_healthy else "unhealthy"
    
    health_status = HealthStatus(
        status=status_value,
        timestamp=datetime.now(timezone.utc),
        version="0.1.0",
        environment=settings.app_env,
        checks={k: v.model_dump() for k, v in checks.items()},
    )
    
    if not all_healthy:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_status.model_dump(),
        )
    
    return health_status


@router.get(
    "/health/live",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Liveness Check",
    description="Simple liveness probe for Kubernetes.",
)
async def liveness_check() -> None:
    """
    Simple liveness check.
    
    Returns 204 No Content if the application is running.
    Used by Kubernetes liveness probes.
    """
    pass
