"""
Health Check Endpoints
═══════════════════════════════════════════════════════════════════════════════════

Provides health monitoring endpoints for the application.
Used by load balancers, Kubernetes probes, and monitoring systems.
"""

import time
from datetime import datetime
from typing import Optional

import structlog
from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.models.schemas import ComponentHealth, HealthCheckResponse, HealthStatus

logger = structlog.get_logger(__name__)

router = APIRouter()


async def check_database_health() -> ComponentHealth:
    """Check PostgreSQL database connectivity."""
    start = time.perf_counter()
    try:
        # TODO: Implement actual database check
        # async with get_db_session() as session:
        #     await session.execute(text("SELECT 1"))
        latency = (time.perf_counter() - start) * 1000
        return ComponentHealth(
            name="postgresql",
            status=HealthStatus.HEALTHY,
            latency_ms=latency,
        )
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return ComponentHealth(
            name="postgresql",
            status=HealthStatus.UNHEALTHY,
            message=str(e),
        )


async def check_redis_health() -> ComponentHealth:
    """Check Redis connectivity."""
    start = time.perf_counter()
    try:
        # TODO: Implement actual Redis check
        # redis = await get_redis()
        # await redis.ping()
        latency = (time.perf_counter() - start) * 1000
        return ComponentHealth(
            name="redis",
            status=HealthStatus.HEALTHY,
            latency_ms=latency,
        )
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))
        return ComponentHealth(
            name="redis",
            status=HealthStatus.UNHEALTHY,
            message=str(e),
        )


async def check_qdrant_health() -> ComponentHealth:
    """Check Qdrant vector database connectivity."""
    start = time.perf_counter()
    try:
        # TODO: Implement actual Qdrant check
        # client = get_qdrant_client()
        # await client.get_collections()
        latency = (time.perf_counter() - start) * 1000
        return ComponentHealth(
            name="qdrant",
            status=HealthStatus.HEALTHY,
            latency_ms=latency,
        )
    except Exception as e:
        logger.error("Qdrant health check failed", error=str(e))
        return ComponentHealth(
            name="qdrant",
            status=HealthStatus.UNHEALTHY,
            message=str(e),
        )


async def check_openai_health() -> ComponentHealth:
    """Check OpenAI API connectivity."""
    start = time.perf_counter()
    try:
        # TODO: Implement actual OpenAI check
        # client = get_openai_client()
        # await client.models.list()
        latency = (time.perf_counter() - start) * 1000
        return ComponentHealth(
            name="openai",
            status=HealthStatus.HEALTHY,
            latency_ms=latency,
        )
    except Exception as e:
        logger.error("OpenAI health check failed", error=str(e))
        return ComponentHealth(
            name="openai",
            status=HealthStatus.DEGRADED,
            message=str(e),
        )


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Basic health check",
    description="Returns basic application health status",
)
async def health_check(
    settings: Settings = Depends(get_settings),
) -> HealthCheckResponse:
    """
    Basic health check endpoint.
    
    Returns 200 if the application is running.
    Does not check external dependencies.
    """
    return HealthCheckResponse(
        status=HealthStatus.HEALTHY,
        version=settings.app.app_version,
        timestamp=datetime.utcnow(),
        components=[],
    )


@router.get(
    "/health/detailed",
    response_model=HealthCheckResponse,
    summary="Detailed health check",
    description="Returns detailed health status including all dependencies",
)
async def detailed_health_check(
    settings: Settings = Depends(get_settings),
) -> HealthCheckResponse:
    """
    Detailed health check endpoint.
    
    Checks connectivity to all external dependencies:
    - PostgreSQL database
    - Redis cache
    - Qdrant vector database
    - OpenAI API
    """
    components = [
        await check_database_health(),
        await check_redis_health(),
        await check_qdrant_health(),
        await check_openai_health(),
    ]
    
    # Determine overall status
    statuses = [c.status for c in components]
    if all(s == HealthStatus.HEALTHY for s in statuses):
        overall_status = HealthStatus.HEALTHY
    elif any(s == HealthStatus.UNHEALTHY for s in statuses):
        overall_status = HealthStatus.UNHEALTHY
    else:
        overall_status = HealthStatus.DEGRADED
    
    return HealthCheckResponse(
        status=overall_status,
        version=settings.app.app_version,
        timestamp=datetime.utcnow(),
        components=components,
    )


@router.get(
    "/health/ready",
    summary="Readiness probe",
    description="Kubernetes readiness probe endpoint",
)
async def readiness_probe() -> dict:
    """
    Readiness probe for Kubernetes.
    
    Returns 200 when the application is ready to receive traffic.
    """
    # Check critical dependencies
    db_health = await check_database_health()
    redis_health = await check_redis_health()
    
    if db_health.status == HealthStatus.UNHEALTHY:
        return {"ready": False, "reason": "Database unavailable"}
    
    if redis_health.status == HealthStatus.UNHEALTHY:
        return {"ready": False, "reason": "Redis unavailable"}
    
    return {"ready": True}


@router.get(
    "/health/live",
    summary="Liveness probe",
    description="Kubernetes liveness probe endpoint",
)
async def liveness_probe() -> dict:
    """
    Liveness probe for Kubernetes.
    
    Returns 200 if the application is alive.
    A failure would trigger a container restart.
    """
    return {"alive": True}
