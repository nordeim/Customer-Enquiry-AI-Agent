"""
Dependency Injection Configuration

Centralized dependency management for FastAPI using dependency injection.
Includes Redis, Qdrant, and other service dependencies.
"""

from typing import Annotated, AsyncGenerator

import redis.asyncio as redis
from fastapi import Depends, Header, HTTPException, status
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.logging_config import get_logger

logger = get_logger(__name__)

# =============================================================================
# GLOBAL CLIENTS
# =============================================================================

_redis_client: redis.Redis | None = None
_qdrant_client: QdrantClient | None = None


# =============================================================================
# REDIS
# =============================================================================

async def init_redis() -> None:
    """Initialize Redis connection pool."""
    global _redis_client
    
    try:
        _redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
        )
        # Test connection
        await _redis_client.ping()
        logger.info("redis_connected", host=settings.redis_host, port=settings.redis_port)
    except Exception as e:
        logger.error("redis_connection_failed", error=str(e))
        raise


async def close_redis() -> None:
    """Close Redis connection pool."""
    global _redis_client
    
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("redis_disconnected")


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """Get Redis client dependency."""
    if _redis_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis connection not available",
        )
    yield _redis_client


# =============================================================================
# QDRANT
# =============================================================================

async def init_qdrant() -> None:
    """Initialize Qdrant client and collections."""
    global _qdrant_client
    
    try:
        # Create client
        api_key = settings.qdrant_api_key.get_secret_value()
        _qdrant_client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=api_key if api_key else None,
        )
        
        # Ensure collections exist
        await _ensure_collections()
        
        logger.info("qdrant_connected", host=settings.qdrant_host, port=settings.qdrant_port)
    except Exception as e:
        logger.error("qdrant_connection_failed", error=str(e))
        raise


async def _ensure_collections() -> None:
    """Ensure required Qdrant collections exist."""
    if _qdrant_client is None:
        return
    
    collections_to_create = [
        (settings.qdrant_collection_name, 1536),  # OpenAI text-embedding-3-small
        (settings.qdrant_collection_summaries, 1536),
    ]
    
    existing_collections = {
        col.name for col in _qdrant_client.get_collections().collections
    }
    
    for collection_name, vector_size in collections_to_create:
        if collection_name not in existing_collections:
            _qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=qdrant_models.VectorParams(
                    size=vector_size,
                    distance=qdrant_models.Distance.COSINE,
                ),
            )
            logger.info("qdrant_collection_created", collection=collection_name)
        else:
            logger.debug("qdrant_collection_exists", collection=collection_name)


def get_qdrant() -> QdrantClient:
    """Get Qdrant client dependency."""
    if _qdrant_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Qdrant connection not available",
        )
    return _qdrant_client


# =============================================================================
# AUTHENTICATION
# =============================================================================

async def verify_api_key(
    x_api_key: Annotated[str | None, Header()] = None
) -> str:
    """
    Verify API key from request header.
    
    In development mode, allows requests without API key.
    """
    if settings.is_development and not x_api_key:
        return "development"
    
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    if x_api_key != settings.api_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return x_api_key


# =============================================================================
# TYPE ALIASES FOR DEPENDENCY INJECTION
# =============================================================================

# Database session dependency
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Redis client dependency
RedisDep = Annotated[redis.Redis, Depends(get_redis)]

# Qdrant client dependency
QdrantDep = Annotated[QdrantClient, Depends(get_qdrant)]

# API key verification dependency
ApiKeyDep = Annotated[str, Depends(verify_api_key)]
