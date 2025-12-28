"""
FastAPI Application Entry Point
═══════════════════════════════════════════════════════════════════════════════════

Main application factory and configuration.

Design Principles:
- Clean separation of concerns
- Graceful startup/shutdown
- Comprehensive error handling
- Structured logging
"""

import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api.routes import chat, health, knowledge
from app.config import get_settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for initializing
    and cleaning up resources (database connections, caches, etc.)
    """
    settings = get_settings()
    
    # ═══════════════════════════════════════════════════════════════════════
    # STARTUP
    # ═══════════════════════════════════════════════════════════════════════
    logger.info(
        "Starting application",
        app_name=settings.app.app_name,
        version=settings.app.app_version,
        environment=settings.app.app_env,
    )
    
    # Initialize database connections
    # await init_database()
    
    # Initialize Redis connection
    # await init_redis()
    
    # Initialize Qdrant client
    # await init_qdrant()
    
    # Warm up models (optional)
    # await warm_up_models()
    
    logger.info("Application startup complete")
    
    yield  # Application runs here
    
    # ═══════════════════════════════════════════════════════════════════════
    # SHUTDOWN
    # ═══════════════════════════════════════════════════════════════════════
    logger.info("Initiating graceful shutdown")
    
    # Close database connections
    # await close_database()
    
    # Close Redis connection
    # await close_redis()
    
    # Close Qdrant client
    # await close_qdrant()
    
    logger.info("Application shutdown complete")


def create_application() -> FastAPI:
    """
    Application factory function.
    
    Creates and configures the FastAPI application instance.
    
    Returns:
        FastAPI: Configured application instance
    """
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app.app_name,
        description="""
        ## Singapore SMB Customer Support AI Agent
        
        An intelligent, context-aware customer support agent powered by 
        advanced RAG (Retrieval Augmented Generation) and memory systems.
        
        ### Features
        - 🤖 AI-powered customer support
        - 📚 RAG-based knowledge retrieval
        - 🧠 Short-term and long-term memory
        - 🌏 Multilingual support (English, Mandarin)
        - 🔒 PDPA-compliant data handling
        
        ### API Endpoints
        - `/api/chat` - Main chat interface
        - `/api/knowledge` - Knowledge base management
        - `/api/health` - Health monitoring
        """,
        version=settings.app.app_version,
        docs_url="/docs" if settings.app.is_development else None,
        redoc_url="/redoc" if settings.app.is_development else None,
        openapi_url="/openapi.json" if settings.app.is_development else None,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    
    # ═══════════════════════════════════════════════════════════════════════
    # MIDDLEWARE
    # ═══════════════════════════════════════════════════════════════════════
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Processing-Time"],
    )
    
    # Request timing middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000
        response.headers["X-Processing-Time"] = f"{process_time:.2f}ms"
        return response
    
    # Request ID middleware
    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        import uuid
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    
    # ═══════════════════════════════════════════════════════════════════════
    # ROUTES
    # ═══════════════════════════════════════════════════════════════════════
    
    # Health check routes
    app.include_router(
        health.router,
        prefix="/api",
        tags=["Health"],
    )
    
    # Chat routes
    app.include_router(
        chat.router,
        prefix="/api/chat",
        tags=["Chat"],
    )
    
    # Knowledge base routes
    app.include_router(
        knowledge.router,
        prefix="/api/knowledge",
        tags=["Knowledge Base"],
    )
    
    # ═══════════════════════════════════════════════════════════════════════
    # EXCEPTION HANDLERS
    # ═══════════════════════════════════════════════════════════════════════
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler for unhandled errors."""
        logger.exception(
            "Unhandled exception",
            request_id=getattr(request.state, "request_id", "unknown"),
            path=request.url.path,
            method=request.method,
            error=str(exc),
        )
        
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later.",
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )
    
    return app


# Create the application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.app.app_host,
        port=settings.app.app_port,
        reload=settings.app.is_development,
        log_level=settings.app.app_log_level.lower(),
    )
