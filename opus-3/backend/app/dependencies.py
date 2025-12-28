"""
Dependency Injection Module

Provides FastAPI dependencies for database connections,
services, and other shared resources.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, Request
from qdrant_client import AsyncQdrantClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings, get_settings


# ─────────────────────────────────────────────────────────────────────────────
# Database Engine & Session Factory
# ─────────────────────────────────────────────────────────────────────────────

def create_db_engine(settings: Settings):
    """Create async database engine with connection pooling."""
    return create_async_engine(
        settings.database_url,
        echo=settings.app_debug,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )


def create_session_factory(engine) -> async_sessionmaker[AsyncSession]:
    """Create async session factory."""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Global instances (initialized at startup)
# ─────────────────────────────────────────────────────────────────────────────

_engine = None
_session_factory = None
_redis_pool = None
_qdrant_client = None


async def init_dependencies(settings: Settings) -> None:
    """Initialize all dependencies at application startup."""
    global _engine, _session_factory, _redis_pool, _qdrant_client
    
    # PostgreSQL
    _engine = create_db_engine(settings)
    _session_factory = create_session_factory(_engine)
    
    # Redis
    _redis_pool = redis.ConnectionPool.from_url(
        settings.redis_url,
        decode_responses=True,
        max_connections=20,
    )
    
    # Qdrant
    _qdrant_client = AsyncQdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        api_key=settings.qdrant_api_key.get_secret_value() if settings.qdrant_api_key else None,
    )


async def close_dependencies() -> None:
    """Cleanup all dependencies at application shutdown."""
    global _engine, _redis_pool, _qdrant_client
    
    if _engine:
        await _engine.dispose()
    
    if _redis_pool:
        await _redis_pool.disconnect()
    
    if _qdrant_client:
        await _qdrant_client.close()


# ─────────────────────────────────────────────────────────────────────────────
# FastAPI Dependencies
# ─────────────────────────────────────────────────────────────────────────────

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session dependency.
    
    Yields:
        AsyncSession: Database session that is automatically closed after use.
    """
    if _session_factory is None:
        raise RuntimeError("Database not initialized. Call init_dependencies first.")
    
    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_redis_client() -> AsyncGenerator[redis.Redis, None]:
    """
    Get Redis client dependency.
    
    Yields:
        redis.Redis: Redis client that is automatically closed after use.
    """
    if _redis_pool is None:
        raise RuntimeError("Redis not initialized. Call init_dependencies first.")
    
    client = redis.Redis(connection_pool=_redis_pool)
    try:
        yield client
    finally:
        await client.close()


async def get_qdrant_client() -> AsyncQdrantClient:
    """
    Get Qdrant client dependency.
    
    Returns:
        AsyncQdrantClient: Shared Qdrant client instance.
    """
    if _qdrant_client is None:
        raise RuntimeError("Qdrant not initialized. Call init_dependencies first.")
    
    return _qdrant_client


# ─────────────────────────────────────────────────────────────────────────────
# Type Aliases for Dependency Injection
# ─────────────────────────────────────────────────────────────────────────────

SettingsDep = Annotated[Settings, Depends(get_settings)]
DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
RedisDep = Annotated[redis.Redis, Depends(get_redis_client)]
QdrantDep = Annotated[AsyncQdrantClient, Depends(get_qdrant_client)]


# ─────────────────────────────────────────────────────────────────────────────
# Lifespan Context Manager
# ─────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app):
    """
    Application lifespan manager.
    
    Handles startup and shutdown of all dependencies.
    """
    import structlog
    
    logger = structlog.get_logger()
    settings = get_settings()
    
    # Startup
    logger.info("Starting application", app_name=settings.app_name, env=settings.app_env)
    await init_dependencies(settings)
    logger.info("Dependencies initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await close_dependencies()
    logger.info("Dependencies closed successfully")
