"""
FastAPI Application Entry Point

Main application factory and configuration for the Singapore SMB
Customer Support AI Agent.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.logging_config import setup_logging, get_logger

# Initialize logging first
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for initializing
    and cleaning up resources.
    """
    # Startup
    logger.info(
        "application_starting",
        app_name=settings.app_name,
        environment=settings.app_env,
        debug=settings.debug,
    )
    
    # Initialize database connections
    from app.database import init_db, close_db
    await init_db()
    logger.info("database_initialized")
    
    # Initialize Redis connection
    from app.dependencies import init_redis, close_redis
    await init_redis()
    logger.info("redis_initialized")
    
    # Initialize Qdrant collections
    from app.dependencies import init_qdrant
    await init_qdrant()
    logger.info("qdrant_initialized")
    
    logger.info("application_started", port=settings.api_port)
    
    yield
    
    # Shutdown
    logger.info("application_shutting_down")
    
    await close_redis()
    await close_db()
    
    logger.info("application_stopped")


def create_application() -> FastAPI:
    """
    Application factory.
    
    Creates and configures the FastAPI application instance.
    """
    app = FastAPI(
        title=settings.app_name,
        description="AI-powered customer support agent for Singapore SMBs",
        version="1.0.0",
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        openapi_url="/openapi.json" if settings.is_development else None,
        lifespan=lifespan,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register exception handlers
    register_exception_handlers(app)
    
    # Register routes
    register_routes(app)
    
    return app


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers."""
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle request validation errors."""
        logger.warning(
            "validation_error",
            path=request.url.path,
            errors=exc.errors(),
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "detail": exc.errors(),
            },
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle unexpected exceptions."""
        logger.exception(
            "unhandled_exception",
            path=request.url.path,
            error=str(exc),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "detail": "An unexpected error occurred" if settings.is_production else str(exc),
            },
        )


def register_routes(app: FastAPI) -> None:
    """Register API routes."""
    from app.api.routes import health, chat, knowledge
    
    # Health check routes (no prefix)
    app.include_router(health.router, tags=["Health"])
    
    # API routes with prefix
    app.include_router(
        chat.router,
        prefix=settings.api_prefix,
        tags=["Chat"],
    )
    app.include_router(
        knowledge.router,
        prefix=settings.api_prefix,
        tags=["Knowledge Base"],
    )


# Create application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.is_development,
        log_level=settings.log_level.lower(),
    )
