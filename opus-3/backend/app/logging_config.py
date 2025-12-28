"""
Logging Configuration Module

Configures structured logging using structlog for consistent,
machine-readable log output.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.typing import Processor

from app.config import get_settings


def configure_logging() -> None:
    """
    Configure structured logging for the application.
    
    Sets up structlog with appropriate processors based on
    the environment (development vs production).
    """
    settings = get_settings()
    
    # Common processors for all environments
    shared_processors: list[Processor] = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]
    
    if settings.log_format == "json":
        # JSON format for production
        processors: list[Processor] = [
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Console format for development
        processors = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level),
    )
    
    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str | None = None) -> structlog.BoundLogger:
    """
    Get a configured logger instance.
    
    Args:
        name: Optional logger name for identification.
    
    Returns:
        structlog.BoundLogger: Configured logger instance.
    """
    return structlog.get_logger(name)


def log_request_context(
    request_id: str,
    method: str,
    path: str,
    **extra: Any
) -> dict[str, Any]:
    """
    Create a log context for HTTP requests.
    
    Args:
        request_id: Unique request identifier.
        method: HTTP method.
        path: Request path.
        **extra: Additional context fields.
    
    Returns:
        dict: Context dictionary for logging.
    """
    return {
        "request_id": request_id,
        "http_method": method,
        "http_path": path,
        **extra,
    }
