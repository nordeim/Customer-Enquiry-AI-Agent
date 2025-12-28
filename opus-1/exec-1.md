Let me start with Phase 1: Foundation - this includes:

Project structure setup
Configuration management
Database models
FastAPI skeleton
Docker setup
I'll provide complete, production-ready code with proper documentation. Let me begin systematically.

For the technology choices that weren't explicitly confirmed, I'll proceed with:

GPT-4o-mini as primary LLM
Qdrant as vector database
Cohere for reranking (with local fallback)
English first, Mandarin support built-in
Docker Compose for development
Sample data provided
Let me create the complete implementation following my phased approach.

Phase 1: Foundation

pyproject.toml
requirements.txt
.env.example
config.py
main.py (FastAPI)
database models
Pydantic schemas
Docker setup
Phase 2: Ingestion Pipeline

Document parsers
Chunking strategies
Embedding generation
Qdrant integration
Phase 3: RAG Pipeline

Query transformation
Hybrid retrieval
Reranking
Context compression
Phase 4: Memory System

Redis short-term memory
PostgreSQL long-term memory
Summarization
Working memory assembly
Phase 5: Agent Implementation

Pydantic AI agent
Tools
Prompts
Validators
Phase 6: API Layer

REST endpoints
WebSocket
Authentication
Phase 7: Frontend

React components

Chat widget

State management

WebSocket client

Let me start with Phase 1 and provide complete, working code.

Implementation Execution: Singapore SMB Customer Support AI Agent
text

╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║   ███████╗██╗  ██╗███████╗ ██████╗██╗   ██╗████████╗██╗ ██████╗ ███╗   ██╗          ║
║   ██╔════╝╚██╗██╔╝██╔════╝██╔════╝██║   ██║╚════██╔╝██║██╔═══██╗████╗  ██║          ║
║   █████╗   ╚███╔╝ █████╗  ██║     ██║   ██║    ██╔╝ ██║██║   ██║██╔██╗ ██║          ║
║   ██╔══╝   ██╔██╗ ██╔══╝  ██║     ██║   ██║   ██╔╝  ██║██║   ██║██║╚██╗██║          ║
║   ███████╗██╔╝ ██╗███████╗╚██████╗╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚████║          ║
║   ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝          ║
║                                                                                      ║
║                         PHASE 1: FOUNDATION                                          ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
Phase 1: Foundation Layer
1.1 Project Configuration Files
pyproject.toml
toml

[project]
name = "singapore-smb-support-agent"
version = "1.0.0"
description = "Production-ready AI Customer Support Agent for Singapore SMBs"
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.11"
authors = [
    { name = "Your Company", email = "dev@yourcompany.com" }
]
keywords = ["ai", "chatbot", "rag", "customer-support", "langchain", "pydantic-ai"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    # Core Framework
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "python-multipart>=0.0.12",
    "python-dotenv>=1.0.1",
    
    # Pydantic & Validation
    "pydantic>=2.9.0",
    "pydantic-settings>=2.6.0",
    "pydantic-ai>=0.0.24",
    
    # LangChain Ecosystem
    "langchain>=0.3.7",
    "langchain-core>=0.3.15",
    "langchain-openai>=0.2.6",
    "langchain-community>=0.3.5",
    "langgraph>=0.2.45",
    
    # Vector Database
    "qdrant-client>=1.12.0",
    "langchain-qdrant>=0.2.0",
    
    # Embeddings & Reranking
    "openai>=1.55.0",
    "sentence-transformers>=3.3.0",
    "cohere>=5.11.0",
    
    # Memory & Database
    "redis>=5.2.0",
    "sqlalchemy[asyncio]>=2.0.35",
    "asyncpg>=0.30.0",
    "alembic>=1.14.0",
    "greenlet>=3.1.0",
    
    # Document Processing
    "unstructured>=0.16.5",
    "pypdf>=5.1.0",
    "python-docx>=1.1.2",
    "beautifulsoup4>=4.12.3",
    "markdownify>=0.14.1",
    
    # NLP & Text Processing
    "tiktoken>=0.8.0",
    "nltk>=3.9.1",
    "langdetect>=1.0.9",
    
    # Utilities
    "httpx>=0.27.2",
    "tenacity>=9.0.0",
    "structlog>=24.4.0",
    "orjson>=3.10.11",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.3",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "httpx>=0.27.2",
    "ruff>=0.7.3",
    "mypy>=1.13.0",
    "pre-commit>=4.0.1",
    "ragas>=0.2.5",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["app"]

[tool.ruff]
target-version = "py311"
line-length = 100
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by formatter)
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.isort]
known-first-party = ["app"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
filterwarnings = [
    "ignore::DeprecationWarning",
]
backend/.env.example
Bash

# ═══════════════════════════════════════════════════════════════════════════════
# SINGAPORE SMB SUPPORT AGENT - ENVIRONMENT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────────
# APPLICATION SETTINGS
# ─────────────────────────────────────────────────────────────────────────────────
APP_NAME="Singapore SMB Support Agent"
APP_ENV=development
APP_DEBUG=true
APP_VERSION=1.0.0
APP_HOST=0.0.0.0
APP_PORT=8000
APP_LOG_LEVEL=INFO

# Timezone (Singapore)
TZ=Asia/Singapore

# ─────────────────────────────────────────────────────────────────────────────────
# API KEYS - LLM PROVIDERS
# ─────────────────────────────────────────────────────────────────────────────────
OPENAI_API_KEY=sk-your-openai-api-key-here
COHERE_API_KEY=your-cohere-api-key-here

# Optional: Anthropic for fallback
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# ─────────────────────────────────────────────────────────────────────────────────
# LLM CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────────
# Primary model for chat responses
LLM_PRIMARY_MODEL=gpt-4o-mini
LLM_PRIMARY_TEMPERATURE=0.3
LLM_PRIMARY_MAX_TOKENS=1024

# Secondary model for complex queries
LLM_SECONDARY_MODEL=gpt-4o
LLM_SECONDARY_TEMPERATURE=0.2
LLM_SECONDARY_MAX_TOKENS=2048

# Embedding model
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# ─────────────────────────────────────────────────────────────────────────────────
# VECTOR DATABASE - QDRANT
# ─────────────────────────────────────────────────────────────────────────────────
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=knowledge_base
QDRANT_COLLECTION_SUMMARIES=document_summaries

# ─────────────────────────────────────────────────────────────────────────────────
# REDIS - SHORT-TERM MEMORY
# ─────────────────────────────────────────────────────────────────────────────────
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_SESSION_TTL=1800  # 30 minutes in seconds

# ─────────────────────────────────────────────────────────────────────────────────
# POSTGRESQL - LONG-TERM MEMORY
# ─────────────────────────────────────────────────────────────────────────────────
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=support_agent
POSTGRES_PASSWORD=your-secure-password-here
POSTGRES_DB=support_agent_db

# Connection pool settings
POSTGRES_POOL_SIZE=10
POSTGRES_MAX_OVERFLOW=20

# ─────────────────────────────────────────────────────────────────────────────────
# RAG CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────────
# Chunking
CHUNK_SIZE=512
CHUNK_OVERLAP=100
SEMANTIC_CHUNK_THRESHOLD=0.5

# Retrieval
RETRIEVAL_TOP_K=50
RERANK_TOP_K=5
HYBRID_SEARCH_ALPHA=0.5  # Balance between semantic (1.0) and keyword (0.0)

# Reranking
RERANKER_MODEL=rerank-english-v3.0
USE_LOCAL_RERANKER=false

# Context Management
MAX_CONTEXT_TOKENS=4000
MAX_CONVERSATION_MESSAGES=20

# ─────────────────────────────────────────────────────────────────────────────────
# MEMORY CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────────
# Summarization threshold (number of messages before summarization)
SUMMARIZATION_THRESHOLD=15
SUMMARY_MAX_TOKENS=500

# Customer data retention (PDPA compliance)
CUSTOMER_DATA_RETENTION_DAYS=30
ANONYMIZE_AFTER_DAYS=7

# ─────────────────────────────────────────────────────────────────────────────────
# AGENT CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────────
# Confidence thresholds
CONFIDENCE_THRESHOLD=0.7
ESCALATION_SENTIMENT_THRESHOLD=-0.5

# Response settings
MAX_RESPONSE_LENGTH=1500
INCLUDE_SOURCES=true

# ─────────────────────────────────────────────────────────────────────────────────
# BUSINESS CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────────
BUSINESS_NAME="Your Singapore SMB"
BUSINESS_TIMEZONE=Asia/Singapore
BUSINESS_HOURS_START=09:00
BUSINESS_HOURS_END=18:00
BUSINESS_DAYS=Monday,Tuesday,Wednesday,Thursday,Friday

# Support email for escalations
SUPPORT_EMAIL=support@yourcompany.com
SUPPORT_PHONE=+65-6123-4567

# ─────────────────────────────────────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────────────────────────────────────
API_KEY_HEADER=X-API-Key
API_KEYS=dev-key-12345,prod-key-67890
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
RATE_LIMIT_PER_MINUTE=60

# JWT (if using authenticated sessions)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# ─────────────────────────────────────────────────────────────────────────────────
# MONITORING & LOGGING
# ─────────────────────────────────────────────────────────────────────────────────
ENABLE_METRICS=true
METRICS_PORT=9090
LOG_FORMAT=json
SENTRY_DSN=
1.2 Core Configuration Module
backend/app/config.py
Python

"""
Configuration Management Module
═══════════════════════════════════════════════════════════════════════════════════

Centralized configuration using Pydantic Settings with validation,
environment variable loading, and type safety.

Design Principles:
- Single source of truth for all configuration
- Environment-based overrides
- Validation at startup (fail fast)
- Immutable after initialization
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application-level settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application
    app_name: str = Field(default="Singapore SMB Support Agent")
    app_env: Literal["development", "staging", "production"] = Field(default="development")
    app_debug: bool = Field(default=False)
    app_version: str = Field(default="1.0.0")
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    app_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO"
    )
    
    @property
    def is_development(self) -> bool:
        return self.app_env == "development"
    
    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


class LLMSettings(BaseSettings):
    """LLM provider configuration."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    # API Keys
    openai_api_key: str = Field(default="")
    cohere_api_key: str = Field(default="")
    anthropic_api_key: str = Field(default="")
    
    # Primary Model (for most queries)
    llm_primary_model: str = Field(default="gpt-4o-mini")
    llm_primary_temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    llm_primary_max_tokens: int = Field(default=1024, ge=100, le=4096)
    
    # Secondary Model (for complex queries)
    llm_secondary_model: str = Field(default="gpt-4o")
    llm_secondary_temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    llm_secondary_max_tokens: int = Field(default=2048, ge=100, le=8192)
    
    # Embedding
    embedding_model: str = Field(default="text-embedding-3-small")
    embedding_dimensions: int = Field(default=1536)
    
    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        if not v or not v.startswith("sk-"):
            raise ValueError("Valid OpenAI API key required (must start with 'sk-')")
        return v


class QdrantSettings(BaseSettings):
    """Qdrant vector database configuration."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    qdrant_host: str = Field(default="localhost")
    qdrant_port: int = Field(default=6333)
    qdrant_api_key: str | None = Field(default=None)
    qdrant_collection_name: str = Field(default="knowledge_base")
    qdrant_collection_summaries: str = Field(default="document_summaries")
    
    @property
    def url(self) -> str:
        return f"http://{self.qdrant_host}:{self.qdrant_port}"


class RedisSettings(BaseSettings):
    """Redis configuration for short-term memory."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_password: str | None = Field(default=None)
    redis_db: int = Field(default=0, ge=0, le=15)
    redis_session_ttl: int = Field(default=1800)  # 30 minutes
    
    @property
    def url(self) -> str:
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


class PostgresSettings(BaseSettings):
    """PostgreSQL configuration for long-term memory."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="support_agent")
    postgres_password: str = Field(default="")
    postgres_db: str = Field(default="support_agent_db")
    postgres_pool_size: int = Field(default=10, ge=1, le=50)
    postgres_max_overflow: int = Field(default=20, ge=0, le=100)
    
    @property
    def async_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    @property
    def sync_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


class RAGSettings(BaseSettings):
    """RAG pipeline configuration."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    # Chunking
    chunk_size: int = Field(default=512, ge=100, le=2000)
    chunk_overlap: int = Field(default=100, ge=0, le=500)
    semantic_chunk_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # Retrieval
    retrieval_top_k: int = Field(default=50, ge=10, le=200)
    rerank_top_k: int = Field(default=5, ge=1, le=20)
    hybrid_search_alpha: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # Reranking
    reranker_model: str = Field(default="rerank-english-v3.0")
    use_local_reranker: bool = Field(default=False)
    
    # Context
    max_context_tokens: int = Field(default=4000, ge=1000, le=16000)
    max_conversation_messages: int = Field(default=20, ge=5, le=50)


class MemorySettings(BaseSettings):
    """Memory management configuration."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    summarization_threshold: int = Field(default=15, ge=5, le=50)
    summary_max_tokens: int = Field(default=500, ge=100, le=2000)
    customer_data_retention_days: int = Field(default=30, ge=1, le=365)
    anonymize_after_days: int = Field(default=7, ge=1, le=30)


class AgentSettings(BaseSettings):
    """Agent behavior configuration."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    escalation_sentiment_threshold: float = Field(default=-0.5, ge=-1.0, le=0.0)
    max_response_length: int = Field(default=1500, ge=100, le=5000)
    include_sources: bool = Field(default=True)


class BusinessSettings(BaseSettings):
    """Business-specific configuration."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    business_name: str = Field(default="Your Singapore SMB")
    business_timezone: str = Field(default="Asia/Singapore")
    business_hours_start: str = Field(default="09:00")
    business_hours_end: str = Field(default="18:00")
    business_days: str = Field(default="Monday,Tuesday,Wednesday,Thursday,Friday")
    support_email: str = Field(default="support@yourcompany.com")
    support_phone: str = Field(default="+65-6123-4567")
    
    @property
    def working_days(self) -> list[str]:
        return [day.strip() for day in self.business_days.split(",")]


class SecuritySettings(BaseSettings):
    """Security configuration."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    api_key_header: str = Field(default="X-API-Key")
    api_keys: str = Field(default="")
    cors_origins: str = Field(default="http://localhost:3000")
    rate_limit_per_minute: int = Field(default=60, ge=1, le=1000)
    jwt_secret_key: str = Field(default="change-me-in-production")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiration_hours: int = Field(default=24, ge=1, le=168)
    
    @property
    def api_keys_list(self) -> list[str]:
        return [key.strip() for key in self.api_keys.split(",") if key.strip()]
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


class Settings(BaseSettings):
    """
    Master Settings Container
    
    Aggregates all configuration sections into a single, validated settings object.
    Uses lru_cache to ensure singleton pattern - settings loaded once at startup.
    """
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    app: AppSettings = Field(default_factory=AppSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    qdrant: QdrantSettings = Field(default_factory=QdrantSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    rag: RAGSettings = Field(default_factory=RAGSettings)
    memory: MemorySettings = Field(default_factory=MemorySettings)
    agent: AgentSettings = Field(default_factory=AgentSettings)
    business: BusinessSettings = Field(default_factory=BusinessSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses LRU cache to ensure settings are only loaded once per process.
    This is the recommended way to access settings throughout the application.
    
    Returns:
        Settings: Validated settings object
        
    Example:
        settings = get_settings()
        print(settings.app.app_name)
    """
    return Settings()


# Convenience export
settings = get_settings()
1.3 Database Models
backend/app/models/database.py
Python

"""
SQLAlchemy Database Models
═══════════════════════════════════════════════════════════════════════════════════

Defines the relational database schema for long-term memory storage.
Follows PDPA compliance requirements with data retention tracking.

Tables:
- customers: Customer profiles and preferences
- conversations: Conversation sessions
- messages: Individual messages within conversations
- conversation_summaries: LLM-generated conversation summaries
- feedback: User feedback on responses
- support_tickets: Escalated support tickets
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""
    
    type_annotation_map = {
        dict: JSONB,
    }


class MessageRole(str, Enum):
    """Message sender role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationStatus(str, Enum):
    """Conversation lifecycle status."""
    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    EXPIRED = "expired"


class TicketStatus(str, Enum):
    """Support ticket status."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    """Support ticket priority level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Customer(Base):
    """
    Customer Profile Model
    
    Stores customer information with PDPA-compliant data handling.
    Includes consent tracking and data retention management.
    """
    
    __tablename__ = "customers"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Customer Identification
    external_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
        comment="External system customer ID",
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Preferences
    preferred_language: Mapped[str] = mapped_column(
        String(10),
        default="en",
        comment="ISO 639-1 language code",
    )
    timezone: Mapped[str] = mapped_column(
        String(50),
        default="Asia/Singapore",
    )
    
    # PDPA Compliance
    consent_given: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="PDPA consent for data collection",
    )
    consent_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    data_retention_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Date until which data can be retained",
    )
    is_anonymized: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        comment="Additional customer metadata",
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    # Relationships
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        Index("idx_customer_email_active", "email", "is_anonymized"),
    )


class Conversation(Base):
    """
    Conversation Session Model
    
    Tracks conversation sessions between customers and the AI agent.
    Links to messages, summaries, and any escalation tickets.
    """
    
    __tablename__ = "conversations"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign Keys
    customer_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    # Session Identification
    session_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        comment="External session identifier (e.g., from frontend)",
    )
    
    # Status Tracking
    status: Mapped[ConversationStatus] = mapped_column(
        String(50),
        default=ConversationStatus.ACTIVE,
        index=True,
    )
    
    # Context Tracking
    topic: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Detected conversation topic",
    )
    intent: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Primary user intent",
    )
    sentiment_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Overall conversation sentiment (-1 to 1)",
    )
    
    # Language
    detected_language: Mapped[str] = mapped_column(
        String(10),
        default="en",
    )
    
    # Metrics
    message_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    resolution_time_seconds: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )
    
    # Timestamps
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    customer: Mapped[Optional["Customer"]] = relationship(
        "Customer",
        back_populates="conversations",
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )
    summaries: Mapped[list["ConversationSummary"]] = relationship(
        "ConversationSummary",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="ConversationSummary.created_at.desc()",
    )
    feedback: Mapped[list["Feedback"]] = relationship(
        "Feedback",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )
    tickets: Mapped[list["SupportTicket"]] = relationship(
        "SupportTicket",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        Index("idx_conversation_status_activity", "status", "last_activity_at"),
    )


class Message(Base):
    """
    Individual Message Model
    
    Stores each message in a conversation with role, content,
    and associated metadata like sources and confidence scores.
    """
    
    __tablename__ = "messages"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign Keys
    conversation_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    
    # Message Content
    role: Mapped[MessageRole] = mapped_column(
        String(20),
        index=True,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # Assistant Response Metadata (only for assistant messages)
    confidence_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Agent confidence in response (0-1)",
    )
    sources: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        comment="RAG sources used for response",
    )
    tools_used: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
        comment="Tools invoked during response generation",
    )
    
    # Token Usage (for cost tracking)
    prompt_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    completion_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    # Processing Metadata
    processing_time_ms: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    model_used: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )
    
    __table_args__ = (
        Index("idx_message_conversation_created", "conversation_id", "created_at"),
    )


class ConversationSummary(Base):
    """
    Conversation Summary Model
    
    Stores LLM-generated summaries of conversation segments.
    Used for context compression in long conversations.
    """
    
    __tablename__ = "conversation_summaries"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign Keys
    conversation_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    
    # Summary Content
    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # Coverage
    message_range_start: Mapped[int] = mapped_column(
        Integer,
        comment="First message index covered by this summary",
    )
    message_range_end: Mapped[int] = mapped_column(
        Integer,
        comment="Last message index covered by this summary",
    )
    
    # Key Information Extracted
    key_topics: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )
    action_items: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )
    
    # Token Count
    token_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="summaries",
    )


class Feedback(Base):
    """
    User Feedback Model
    
    Captures user feedback on AI responses for quality improvement.
    """
    
    __tablename__ = "feedback"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign Keys
    conversation_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    message_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Feedback Content
    rating: Mapped[int] = mapped_column(
        Integer,
        comment="Rating 1-5 or thumbs up (1) / down (-1)",
    )
    feedback_type: Mapped[str] = mapped_column(
        String(50),
        default="rating",
        comment="Type: rating, thumbs, detailed",
    )
    comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Categories
    categories: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        comment="Feedback categories: accuracy, helpfulness, clarity, etc.",
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="feedback",
    )


class SupportTicket(Base):
    """
    Support Ticket Model
    
    Created when conversations are escalated to human support.
    """
    
    __tablename__ = "support_tickets"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign Keys
    conversation_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    customer_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Ticket Details
    ticket_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    subject: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # Status & Priority
    status: Mapped[TicketStatus] = mapped_column(
        String(50),
        default=TicketStatus.OPEN,
        index=True,
    )
    priority: Mapped[TicketPriority] = mapped_column(
        String(50),
        default=TicketPriority.MEDIUM,
    )
    
    # Escalation Reason
    escalation_reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Why the conversation was escalated",
    )
    
    # AI Summary
    ai_summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="AI-generated summary for support agent",
    )
    suggested_resolution: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Assignment
    assigned_to: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="tickets",
    )


class KnowledgeDocument(Base):
    """
    Knowledge Document Tracking Model
    
    Tracks documents ingested into the knowledge base.
    Used for document management and update tracking.
    """
    
    __tablename__ = "knowledge_documents"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Document Identification
    filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    source_type: Mapped[str] = mapped_column(
        String(50),
        comment="Type: faq, product, policy, website, manual",
    )
    
    # Processing Status
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        comment="Status: pending, processing, completed, failed",
    )
    
    # Chunk Information
    chunk_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    vector_ids: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        comment="List of vector IDs in Qdrant",
    )
    
    # Content Hash (for change detection)
    content_hash: Mapped[str] = mapped_column(
        String(64),
        comment="SHA-256 hash of document content",
    )
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )
    
    # Error Tracking
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    last_indexed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    __table_args__ = (
        Index("idx_knowledge_doc_status", "status", "source_type"),
    )
1.4 Pydantic Schemas (API Models)
backend/app/models/schemas.py
Python

"""
Pydantic Schemas for API Request/Response Validation
═══════════════════════════════════════════════════════════════════════════════════

Defines all data transfer objects (DTOs) for the API layer.
These schemas ensure type safety and validation at API boundaries.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════


class MessageRole(str, Enum):
    """Message sender role."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationStatus(str, Enum):
    """Conversation lifecycle status."""
    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    EXPIRED = "expired"


class FeedbackType(str, Enum):
    """Type of feedback provided."""
    THUMBS = "thumbs"
    RATING = "rating"
    DETAILED = "detailed"


# ═══════════════════════════════════════════════════════════════════════════════
# BASE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    
    created_at: datetime
    updated_at: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════════════════════
# CHAT SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class ChatMessageRequest(BaseSchema):
    """
    Incoming chat message from user.
    
    Attributes:
        message: The user's message content
        session_id: Client-generated session identifier
        customer_id: Optional customer identifier for personalization
        metadata: Optional additional context
    """
    
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User message content",
        examples=["What are your business hours?"],
    )
    session_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Unique session identifier",
        examples=["sess_abc123"],
    )
    customer_id: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional customer identifier",
    )
    language: Optional[str] = Field(
        default=None,
        max_length=10,
        description="Preferred response language (ISO 639-1)",
        examples=["en", "zh"],
    )
    metadata: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional context metadata",
    )
    
    @field_validator("message")
    @classmethod
    def validate_message_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()


class SourceCitation(BaseSchema):
    """
    Citation for a source used in generating the response.
    """
    
    source_id: str = Field(..., description="Unique identifier for the source")
    title: Optional[str] = Field(default=None, description="Source document title")
    category: Optional[str] = Field(default=None, description="Source category")
    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Relevance score from retrieval",
    )
    snippet: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Relevant text snippet from source",
    )


class SuggestedAction(BaseSchema):
    """
    Suggested follow-up action for the user.
    """
    
    action_type: str = Field(
        ...,
        description="Type of action: link, button, form",
        examples=["link", "button", "quick_reply"],
    )
    label: str = Field(..., description="Display label for the action")
    value: str = Field(..., description="Action value (URL, intent, etc.)")
    metadata: Optional[dict[str, Any]] = Field(default=None)


class ChatMessageResponse(BaseSchema):
    """
    Response from the AI agent.
    
    Comprehensive response including the message, confidence metrics,
    sources used, and suggested follow-up actions.
    """
    
    message_id: UUID = Field(..., description="Unique message identifier")
    session_id: str = Field(..., description="Session identifier")
    
    # Response Content
    content: str = Field(..., description="AI response content")
    
    # Confidence & Quality
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Agent confidence in the response",
    )
    
    # Sources (if RAG was used)
    sources: list[SourceCitation] = Field(
        default_factory=list,
        description="Sources used to generate response",
    )
    
    # Follow-up Suggestions
    suggested_actions: list[SuggestedAction] = Field(
        default_factory=list,
        description="Suggested follow-up actions",
    )
    quick_replies: list[str] = Field(
        default_factory=list,
        max_length=5,
        description="Quick reply suggestions",
    )
    
    # Status Flags
    requires_followup: bool = Field(
        default=False,
        description="Whether user follow-up is expected",
    )
    escalated: bool = Field(
        default=False,
        description="Whether conversation was escalated to human",
    )
    
    # Metadata
    detected_language: str = Field(
        default="en",
        description="Detected language of user message",
    )
    detected_intent: Optional[str] = Field(
        default=None,
        description="Detected user intent",
    )
    processing_time_ms: int = Field(
        ...,
        ge=0,
        description="Response generation time in milliseconds",
    )
    
    # Timestamps
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp (UTC)",
    )


class ConversationHistoryItem(BaseSchema):
    """Single message in conversation history."""
    
    message_id: UUID
    role: MessageRole
    content: str
    timestamp: datetime
    confidence: Optional[float] = None
    sources: Optional[list[SourceCitation]] = None


class ConversationHistory(BaseSchema):
    """Complete conversation history response."""
    
    session_id: str
    status: ConversationStatus
    messages: list[ConversationHistoryItem]
    message_count: int
    started_at: datetime
    last_activity_at: datetime
    detected_language: str = "en"
    topic: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# FEEDBACK SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class FeedbackRequest(BaseSchema):
    """
    User feedback submission.
    """
    
    session_id: str = Field(..., description="Session identifier")
    message_id: Optional[UUID] = Field(
        default=None,
        description="Specific message ID if feedback is for a single message",
    )
    feedback_type: FeedbackType = Field(
        default=FeedbackType.THUMBS,
        description="Type of feedback",
    )
    rating: int = Field(
        ...,
        ge=-1,
        le=5,
        description="Rating value: -1/1 for thumbs, 1-5 for rating",
    )
    comment: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional feedback comment",
    )
    categories: Optional[list[str]] = Field(
        default=None,
        description="Feedback categories",
        examples=[["accuracy", "helpfulness", "clarity"]],
    )


class FeedbackResponse(BaseSchema):
    """Feedback submission confirmation."""
    
    feedback_id: UUID
    message: str = "Thank you for your feedback!"
    received_at: datetime = Field(default_factory=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE BASE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class KnowledgeSearchRequest(BaseSchema):
    """Search request for knowledge base."""
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Search query",
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of results to return",
    )
    category: Optional[str] = Field(
        default=None,
        description="Filter by category",
    )
    min_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Minimum relevance score",
    )


class KnowledgeSearchResult(BaseSchema):
    """Single search result from knowledge base."""
    
    chunk_id: str
    content: str
    score: float
    source: str
    category: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeSearchResponse(BaseSchema):
    """Knowledge base search response."""
    
    query: str
    results: list[KnowledgeSearchResult]
    total_results: int
    search_time_ms: int


class DocumentUploadRequest(BaseSchema):
    """Request to upload a document to knowledge base."""
    
    source_type: str = Field(
        ...,
        description="Document type: faq, product, policy, website",
        examples=["faq", "product", "policy"],
    )
    metadata: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional document metadata",
    )


class DocumentUploadResponse(BaseSchema):
    """Document upload confirmation."""
    
    document_id: UUID
    filename: str
    status: str
    chunk_count: int
    message: str


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class HealthStatus(str, Enum):
    """Health check status values."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class ComponentHealth(BaseSchema):
    """Individual component health status."""
    
    name: str
    status: HealthStatus
    latency_ms: Optional[float] = None
    message: Optional[str] = None


class HealthCheckResponse(BaseSchema):
    """Complete health check response."""
    
    status: HealthStatus
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    components: list[ComponentHealth] = Field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class WebSocketMessageType(str, Enum):
    """WebSocket message types."""
    CHAT = "chat"
    TYPING = "typing"
    PING = "ping"
    PONG = "pong"
    ERROR = "error"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class WebSocketMessage(BaseSchema):
    """WebSocket message envelope."""
    
    type: WebSocketMessageType
    payload: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StreamingChunk(BaseSchema):
    """Streaming response chunk for real-time output."""
    
    chunk_index: int
    content: str
    is_final: bool = False
    message_id: Optional[UUID] = None
1.5 Domain Models
backend/app/models/domain.py
Python

"""
Domain Models
═══════════════════════════════════════════════════════════════════════════════════

Core business domain models used internally within the application.
These are distinct from API schemas and database models.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4


class Intent(str, Enum):
    """Detected user intent categories."""
    
    PRODUCT_INQUIRY = "product_inquiry"
    PRICING = "pricing"
    BUSINESS_HOURS = "business_hours"
    ORDER_STATUS = "order_status"
    COMPLAINT = "complaint"
    TECHNICAL_SUPPORT = "technical_support"
    GENERAL_INQUIRY = "general_inquiry"
    GREETING = "greeting"
    FAREWELL = "farewell"
    UNKNOWN = "unknown"


class Sentiment(str, Enum):
    """Sentiment classification."""
    
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class Document:
    """
    Represents a document chunk from the knowledge base.
    """
    
    id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    score: float = 0.0
    
    @property
    def source(self) -> str:
        return self.metadata.get("source", "unknown")
    
    @property
    def category(self) -> str:
        return self.metadata.get("category", "general")
    
    @property
    def language(self) -> str:
        return self.metadata.get("language", "en")


@dataclass
class RetrievalResult:
    """
    Result from the RAG retrieval pipeline.
    """
    
    documents: list[Document]
    query_used: str
    retrieval_time_ms: int
    reranking_applied: bool = False
    
    @property
    def top_document(self) -> Optional[Document]:
        return self.documents[0] if self.documents else None
    
    @property
    def average_score(self) -> float:
        if not self.documents:
            return 0.0
        return sum(d.score for d in self.documents) / len(self.documents)


@dataclass
class ConversationContext:
    """
    Current conversation context assembled for the agent.
    """
    
    session_id: str
    messages: list[dict[str, Any]]
    customer_info: Optional[dict[str, Any]] = None
    summary: Optional[str] = None
    retrieved_context: Optional[str] = None
    detected_intent: Intent = Intent.UNKNOWN
    detected_language: str = "en"
    sentiment: Sentiment = Sentiment.NEUTRAL
    
    @property
    def message_count(self) -> int:
        return len(self.messages)
    
    @property
    def last_user_message(self) -> Optional[str]:
        for msg in reversed(self.messages):
            if msg.get("role") == "user":
                return msg.get("content")
        return None


@dataclass
class AgentResponse:
    """
    Complete response from the AI agent.
    """
    
    content: str
    confidence: float
    sources: list[Document] = field(default_factory=list)
    tools_used: list[str] = field(default_factory=list)
    requires_escalation: bool = False
    escalation_reason: Optional[str] = None
    suggested_actions: list[dict[str, Any]] = field(default_factory=list)
    quick_replies: list[str] = field(default_factory=list)
    processing_time_ms: int = 0
    model_used: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    
    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


@dataclass
class EscalationRequest:
    """
    Request to escalate conversation to human support.
    """
    
    session_id: str
    reason: str
    priority: str = "medium"
    summary: str = ""
    customer_info: Optional[dict[str, Any]] = None
    conversation_history: list[dict[str, Any]] = field(default_factory=list)
    
    def to_ticket_data(self) -> dict[str, Any]:
        return {
            "ticket_number": f"TKT-{uuid4().hex[:8].upper()}",
            "subject": f"Escalated: {self.reason[:100]}",
            "description": self.summary,
            "priority": self.priority,
            "escalation_reason": self.reason,
            "ai_summary": self.summary,
        }


@dataclass
class BusinessHoursStatus:
    """
    Current business hours status.
    """
    
    is_open: bool
    current_time: datetime
    opens_at: Optional[datetime] = None
    closes_at: Optional[datetime] = None
    next_opening: Optional[datetime] = None
    timezone: str = "Asia/Singapore"
    
    @property
    def status_message(self) -> str:
        if self.is_open:
            return f"We're currently open until {self.closes_at.strftime('%I:%M %p') if self.closes_at else 'later today'}."
        elif self.next_opening:
            return f"We're currently closed. We'll be open again on {self.next_opening.strftime('%A at %I:%M %p')}."
        return "We're currently closed."


@dataclass
class CustomerProfile:
    """
    Customer profile for personalization.
    """
    
    id: UUID
    external_id: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    preferred_language: str = "en"
    timezone: str = "Asia/Singapore"
    metadata: dict[str, Any] = field(default_factory=dict)
    interaction_count: int = 0
    last_interaction: Optional[datetime] = None
    
    @property
    def display_name(self) -> str:
        return self.name or self.email or "Valued Customer"


@dataclass
class TokenBudget:
    """
    Token budget tracking for context management.
    """
    
    max_tokens: int = 4000
    system_prompt_tokens: int = 0
    conversation_tokens: int = 0
    retrieved_context_tokens: int = 0
    reserved_for_response: int = 1000
    
    @property
    def used_tokens(self) -> int:
        return (
            self.system_prompt_tokens
            + self.conversation_tokens
            + self.retrieved_context_tokens
        )
    
    @property
    def available_tokens(self) -> int:
        return max(0, self.max_tokens - self.used_tokens - self.reserved_for_response)
    
    @property
    def utilization(self) -> float:
        return self.used_tokens / self.max_tokens if self.max_tokens > 0 else 0.0
    
    def can_add(self, tokens: int) -> bool:
        return (self.used_tokens + tokens + self.reserved_for_response) <= self.max_tokens
1.6 FastAPI Application Entry Point
backend/app/main.py
Python

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
1.7 API Route Stubs
backend/app/api/routes/__init__.py
Python

"""API Routes Package."""
backend/app/api/routes/health.py
Python

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
backend/app/api/routes/chat.py
Python

"""
Chat API Endpoints
═══════════════════════════════════════════════════════════════════════════════════

Main chat interface for customer support conversations.

Endpoints:
- POST /chat - Send a message and receive AI response
- GET /chat/history/{session_id} - Get conversation history
- POST /chat/feedback - Submit feedback on responses
- WebSocket /chat/ws/{session_id} - Real-time chat
"""

import time
from datetime import datetime
from typing import Optional
from uuid import uuid4

import structlog
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect

from app.config import Settings, get_settings
from app.models.schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationHistory,
    FeedbackRequest,
    FeedbackResponse,
    SourceCitation,
)

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.post(
    "",
    response_model=ChatMessageResponse,
    summary="Send chat message",
    description="Send a message to the AI support agent and receive a response",
    responses={
        200: {"description": "Successful response from AI agent"},
        400: {"description": "Invalid request"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
    },
)
async def send_message(
    request: ChatMessageRequest,
    settings: Settings = Depends(get_settings),
) -> ChatMessageResponse:
    """
    Process a user message and return AI response.
    
    This endpoint:
    1. Loads/creates conversation context
    2. Retrieves relevant knowledge (RAG)
    3. Generates AI response
    4. Stores message in memory
    5. Returns response with sources and suggestions
    """
    start_time = time.perf_counter()
    
    logger.info(
        "Processing chat message",
        session_id=request.session_id,
        customer_id=request.customer_id,
        message_length=len(request.message),
    )
    
    try:
        # TODO: Implement full agent pipeline
        # For now, return a placeholder response
        
        processing_time = int((time.perf_counter() - start_time) * 1000)
        
        # Placeholder response
        response = ChatMessageResponse(
            message_id=uuid4(),
            session_id=request.session_id,
            content="Thank you for your message! I'm currently being set up. "
                    "In the full implementation, I'll be able to help you with "
                    "product information, business hours, pricing, and more.",
            confidence=0.95,
            sources=[
                SourceCitation(
                    source_id="placeholder-1",
                    title="Getting Started Guide",
                    category="documentation",
                    relevance_score=0.9,
                    snippet="This is a placeholder response.",
                )
            ],
            suggested_actions=[],
            quick_replies=[
                "What are your business hours?",
                "Tell me about your products",
                "I need help with an order",
            ],
            requires_followup=False,
            escalated=False,
            detected_language="en",
            detected_intent="general_inquiry",
            processing_time_ms=processing_time,
            timestamp=datetime.utcnow(),
        )
        
        logger.info(
            "Chat response generated",
            session_id=request.session_id,
            processing_time_ms=processing_time,
            confidence=response.confidence,
        )
        
        return response
        
    except Exception as e:
        logger.exception(
            "Error processing chat message",
            session_id=request.session_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process message. Please try again.",
        )


@router.get(
    "/history/{session_id}",
    response_model=ConversationHistory,
    summary="Get conversation history",
    description="Retrieve the full conversation history for a session",
)
async def get_conversation_history(
    session_id: str,
    limit: int = 50,
    settings: Settings = Depends(get_settings),
) -> ConversationHistory:
    """
    Retrieve conversation history for a session.
    
    Args:
        session_id: The session identifier
        limit: Maximum number of messages to return
    
    Returns:
        ConversationHistory: Full conversation with all messages
    """
    logger.info("Fetching conversation history", session_id=session_id, limit=limit)
    
    # TODO: Implement actual history retrieval from memory
    
    # Placeholder response
    return ConversationHistory(
        session_id=session_id,
        status="active",
        messages=[],
        message_count=0,
        started_at=datetime.utcnow(),
        last_activity_at=datetime.utcnow(),
        detected_language="en",
        topic=None,
    )


@router.post(
    "/feedback",
    response_model=FeedbackResponse,
    summary="Submit feedback",
    description="Submit feedback on a conversation or specific message",
)
async def submit_feedback(
    request: FeedbackRequest,
    settings: Settings = Depends(get_settings),
) -> FeedbackResponse:
    """
    Submit user feedback on AI responses.
    
    This feedback is used to:
    - Improve response quality
    - Identify issues in the knowledge base
    - Train future model iterations
    """
    logger.info(
        "Feedback received",
        session_id=request.session_id,
        message_id=request.message_id,
        rating=request.rating,
        feedback_type=request.feedback_type,
    )
    
    # TODO: Store feedback in database
    
    return FeedbackResponse(
        feedback_id=uuid4(),
        message="Thank you for your feedback!",
        received_at=datetime.utcnow(),
    )


@router.websocket("/ws/{session_id}")
async def websocket_chat(
    websocket: WebSocket,
    session_id: str,
):
    """
    WebSocket endpoint for real-time chat.
    
    Supports:
    - Real-time message streaming
    - Typing indicators
    - Connection status updates
    """
    await websocket.accept()
    
    logger.info("WebSocket connection established", session_id=session_id)
    
    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "payload": {
                "session_id": session_id,
                "message": "Connected to chat service",
            },
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        while True:
            # Receive message
            data = await websocket.receive_json()
            
            message_type = data.get("type", "chat")
            
            if message_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat(),
                })
            
            elif message_type == "chat":
                # TODO: Process chat message through agent
                payload = data.get("payload", {})
                message = payload.get("message", "")
                
                # Send typing indicator
                await websocket.send_json({
                    "type": "typing",
                    "payload": {"is_typing": True},
                    "timestamp": datetime.utcnow().isoformat(),
                })
                
                # Simulate processing (replace with actual agent call)
                import asyncio
                await asyncio.sleep(1)
                
                # Send response
                await websocket.send_json({
                    "type": "chat",
                    "payload": {
                        "message_id": str(uuid4()),
                        "content": f"I received your message: '{message}'. "
                                   "Full implementation coming soon!",
                        "confidence": 0.95,
                    },
                    "timestamp": datetime.utcnow().isoformat(),
                })
                
                # Clear typing indicator
                await websocket.send_json({
                    "type": "typing",
                    "payload": {"is_typing": False},
                    "timestamp": datetime.utcnow().isoformat(),
                })
    
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected", session_id=session_id)
    
    except Exception as e:
        logger.exception("WebSocket error", session_id=session_id, error=str(e))
        await websocket.close(code=1011, reason="Internal server error")
backend/app/api/routes/knowledge.py
Python

"""
Knowledge Base API Endpoints
═══════════════════════════════════════════════════════════════════════════════════

Endpoints for managing the knowledge base:
- Search knowledge
- Upload documents
- Manage document lifecycle
"""

import time
from datetime import datetime
from typing import Optional
from uuid import uuid4

import structlog
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.config import Settings, get_settings
from app.models.schemas import (
    DocumentUploadRequest,
    DocumentUploadResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
    KnowledgeSearchResult,
)

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.post(
    "/search",
    response_model=KnowledgeSearchResponse,
    summary="Search knowledge base",
    description="Search the knowledge base using semantic search",
)
async def search_knowledge(
    request: KnowledgeSearchRequest,
    settings: Settings = Depends(get_settings),
) -> KnowledgeSearchResponse:
    """
    Search the knowledge base for relevant documents.
    
    Uses hybrid search (semantic + keyword) with optional reranking.
    """
    start_time = time.perf_counter()
    
    logger.info(
        "Knowledge search request",
        query=request.query[:100],
        top_k=request.top_k,
        category=request.category,
    )
    
    # TODO: Implement actual RAG search
    
    search_time = int((time.perf_counter() - start_time) * 1000)
    
    # Placeholder response
    return KnowledgeSearchResponse(
        query=request.query,
        results=[
            KnowledgeSearchResult(
                chunk_id="placeholder-chunk-1",
                content="This is a placeholder search result. "
                        "In the full implementation, this will return "
                        "relevant documents from your knowledge base.",
                score=0.92,
                source="documentation",
                category="general",
                metadata={"page": 1, "section": "overview"},
            )
        ],
        total_results=1,
        search_time_ms=search_time,
    )


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    summary="Upload document",
    description="Upload a document to the knowledge base",
)
async def upload_document(
    file: UploadFile = File(...),
    source_type: str = "general",
    settings: Settings = Depends(get_settings),
) -> DocumentUploadResponse:
    """
    Upload a document to be indexed in the knowledge base.
    
    Supported formats:
    - PDF (.pdf)
    - Word (.docx)
    - Markdown (.md)
    - Text (.txt)
    - HTML (.html)
    - CSV (.csv)
    - JSON (.json)
    """
    logger.info(
        "Document upload request",
        filename=file.filename,
        source_type=source_type,
        content_type=file.content_type,
    )
    
    # Validate file type
    allowed_extensions = {".pdf", ".docx", ".md", ".txt", ".html", ".csv", ".json"}
    file_ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}",
        )
    
    # TODO: Implement actual document processing
    # 1. Save file temporarily
    # 2. Parse document
    # 3. Chunk document
    # 4. Generate embeddings
    # 5. Store in vector database
    # 6. Track in PostgreSQL
    
    # Placeholder response
    return DocumentUploadResponse(
        document_id=uuid4(),
        filename=file.filename,
        status="pending",
        chunk_count=0,
        message="Document queued for processing. "
                "Check back shortly for indexing status.",
    )


@router.get(
    "/documents",
    summary="List documents",
    description="List all documents in the knowledge base",
)
async def list_documents(
    source_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    settings: Settings = Depends(get_settings),
):
    """
    List documents in the knowledge base with optional filtering.
    """
    # TODO: Implement document listing from PostgreSQL
    
    return {
        "documents": [],
        "total": 0,
        "limit": limit,
        "offset": offset,
    }


@router.delete(
    "/documents/{document_id}",
    summary="Delete document",
    description="Remove a document from the knowledge base",
)
async def delete_document(
    document_id: str,
    settings: Settings = Depends(get_settings),
):
    """
    Delete a document and its associated chunks from the knowledge base.
    """
    logger.info("Document deletion request", document_id=document_id)
    
    # TODO: Implement document deletion
    # 1. Get document from PostgreSQL
    # 2. Delete vectors from Qdrant
    # 3. Delete document record from PostgreSQL
    
    return {
        "message": f"Document {document_id} deleted successfully",
        "document_id": document_id,
    }
1.8 Docker Configuration
backend/Dockerfile
Dockerfile

# ═══════════════════════════════════════════════════════════════════════════════
# SINGAPORE SMB SUPPORT AGENT - BACKEND DOCKERFILE
# ═══════════════════════════════════════════════════════════════════════════════
# Multi-stage build for optimized production image

# ───────────────────────────────────────────────────────────────────────────────
# Stage 1: Builder
# ───────────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ───────────────────────────────────────────────────────────────────────────────
# Stage 2: Production
# ───────────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim as production

WORKDIR /app

# Create non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appgroup . .

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
backend/requirements.txt
txt

# ═══════════════════════════════════════════════════════════════════════════════
# SINGAPORE SMB SUPPORT AGENT - PYTHON DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
# Generated from pyproject.toml - use this for Docker builds

# Core Framework
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
python-multipart>=0.0.12
python-dotenv>=1.0.1

# Pydantic & Validation
pydantic>=2.9.0
pydantic-settings>=2.6.0
pydantic-ai>=0.0.24

# LangChain Ecosystem
langchain>=0.3.7
langchain-core>=0.3.15
langchain-openai>=0.2.6
langchain-community>=0.3.5
langgraph>=0.2.45

# Vector Database
qdrant-client>=1.12.0
langchain-qdrant>=0.2.0

# Embeddings & Reranking
openai>=1.55.0
sentence-transformers>=3.3.0
cohere>=5.11.0

# Memory & Database
redis>=5.2.0
sqlalchemy[asyncio]>=2.0.35
asyncpg>=0.30.0
So
