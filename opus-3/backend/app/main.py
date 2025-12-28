"""
FastAPI Application Entry Point

Main application module that configures and starts the FastAPI server.
"""

import uuid
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api.routes import chat, health, knowledge
from app.config import get_settings
from app.dependencies import close_dependencies, init_dependencies
from app.logging_config import configure_logging


# ─────────────────────────────────────────────────────────────────────────────
# Application Lifespan
# ─────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Handles initialization and cleanup of application resources.
    """
    # Configure logging first
    configure_logging()
    logger = structlog.get_logger()
    
    settings = get_settings()
    
    # Startup
    logger.info(
        "Starting application",
        app_name=settings.app_name,
        environment=settings.app_env,
        debug=settings.app_debug,
    )
    
    try:
        await init_dependencies(settings)
        logger.info("All dependencies initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize dependencies", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await close_dependencies()
    logger.info("Application shutdown complete")


# ─────────────────────────────────────────────────────────────────────────────
# Application Factory
# ─────────────────────────────────────────────────────────────────────────────

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance.
    """
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        description=(
            "Production-ready AI customer support agent for Singapore SMBs. "
            "Features advanced RAG, hierarchical memory, and PDPA compliance."
        ),
        version="0.1.0",
        docs_url="/docs" if settings.app_env != "production" else None,
        redoc_url="/redoc" if settings.app_env != "production" else None,
        openapi_url="/openapi.json" if settings.app_env != "production" else None,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Middleware Configuration
    # ─────────────────────────────────────────────────────────────────────────
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request ID middleware
    @app.middleware("http")
    async def add_request_id(request: Request, call_next) -> Response:
        """Add unique request ID to each request."""
        request_id = str(uuid.uuid4())
        
        # Add to request state
        request.state.request_id = request_id
        
        # Bind to structlog context
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.url.path,
            method=request.method,
        )
        
        # Process request
        response = await call_next(request)
        
        # Add to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
    
    # Logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next) -> Response:
        """Log all HTTP requests."""
        import time
        
        logger = structlog.get_logger()
        
        start_time = time.perf_counter()
        
        # Log request
        logger.info(
            "Request started",
            client_host=request.client.host if request.client else None,
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        # Log response
        logger.info(
            "Request completed",
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
        
        return response
    
    # ─────────────────────────────────────────────────────────────────────────
    # Router Registration
    # ─────────────────────────────────────────────────────────────────────────
    
    app.include_router(health.router, prefix="/api", tags=["Health"])
    app.include_router(chat.router, prefix="/api", tags=["Chat"])
    app.include_router(knowledge.router, prefix="/api", tags=["Knowledge"])
    
    return app


# ─────────────────────────────────────────────────────────────────────────────
# Application Instance
# ─────────────────────────────────────────────────────────────────────────────

app = create_application()


# ─────────────────────────────────────────────────────────────────────────────
# Development Server
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        workers=1 if settings.api_reload else settings.api_workers,
        log_level=settings.log_level.lower(),
    )
