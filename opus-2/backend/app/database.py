"""
Database Configuration

Async SQLAlchemy setup for PostgreSQL with connection pooling
and session management.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings
from app.logging_config import get_logger

logger = get_logger(__name__)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# Create async engine with connection pooling
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Create session factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def init_db() -> None:
    """
    Initialize database connection and create tables.
    
    Should be called during application startup.
    """
    try:
        # Import all models to ensure they're registered
        from app.models import database  # noqa: F401
        
        async with engine.begin() as conn:
            # Create tables if they don't exist
            # In production, use Alembic migrations instead
            if settings.is_development:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("database_tables_created")
    except Exception as e:
        logger.error("database_init_failed", error=str(e))
        raise


async def close_db() -> None:
    """
    Close database connections.
    
    Should be called during application shutdown.
    """
    await engine.dispose()
    logger.info("database_connections_closed")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection for database sessions.
    
    Usage:
        @router.get("/items")
        async def get_items(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
