"""
Configuration Management Module

Centralized configuration using Pydantic Settings with validation,
type safety, and environment variable loading.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings are validated at startup to ensure correct configuration.
    Secrets are handled securely using SecretStr.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Application Settings
    # ─────────────────────────────────────────────────────────────────────────
    app_name: str = Field(
        default="Singapore SMB Support Agent",
        description="Application name for logging and identification"
    )
    app_env: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Environment the application is running in"
    )
    app_debug: bool = Field(
        default=False,
        description="Enable debug mode (never in production!)"
    )
    app_secret_key: SecretStr = Field(
        ...,
        min_length=32,
        description="Secret key for cryptographic operations"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # API Configuration
    # ─────────────────────────────────────────────────────────────────────────
    api_host: str = Field(default="0.0.0.0", description="API host to bind to")
    api_port: int = Field(default=8000, ge=1, le=65535, description="API port")
    api_workers: int = Field(default=4, ge=1, description="Number of worker processes")
    api_reload: bool = Field(default=False, description="Enable auto-reload for development")
    
    frontend_url: str = Field(
        default="http://localhost:3000",
        description="Frontend URL for CORS configuration"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # LLM Configuration
    # ─────────────────────────────────────────────────────────────────────────
    openai_api_key: SecretStr = Field(..., description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o-mini", description="OpenAI model for generation")
    openai_embedding_model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI model for embeddings"
    )
    
    anthropic_api_key: SecretStr | None = Field(
        default=None,
        description="Anthropic API key (fallback LLM)"
    )
    
    cohere_api_key: SecretStr | None = Field(
        default=None,
        description="Cohere API key (for reranking)"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Vector Database (Qdrant)
    # ─────────────────────────────────────────────────────────────────────────
    qdrant_host: str = Field(default="localhost", description="Qdrant host")
    qdrant_port: int = Field(default=6333, description="Qdrant port")
    qdrant_api_key: SecretStr | None = Field(default=None, description="Qdrant API key")
    qdrant_collection_name: str = Field(
        default="knowledge_base",
        description="Main knowledge base collection name"
    )
    qdrant_summaries_collection: str = Field(
        default="document_summaries",
        description="Document summaries collection name"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # PostgreSQL Database
    # ─────────────────────────────────────────────────────────────────────────
    postgres_host: str = Field(default="localhost", description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")
    postgres_db: str = Field(default="support_agent", description="Database name")
    postgres_user: str = Field(default="support_agent", description="Database user")
    postgres_password: SecretStr = Field(..., description="Database password")
    
    @property
    def database_url(self) -> str:
        """Construct async PostgreSQL connection URL."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password.get_secret_value()}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    @property
    def database_url_sync(self) -> str:
        """Construct sync PostgreSQL connection URL (for Alembic)."""
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password.get_secret_value()}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Redis Configuration
    # ─────────────────────────────────────────────────────────────────────────
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_password: SecretStr | None = Field(default=None, description="Redis password")
    redis_db: int = Field(default=0, ge=0, le=15, description="Redis database number")
    
    @property
    def redis_url(self) -> str:
        """Construct Redis connection URL."""
        if self.redis_password:
            return (
                f"redis://:{self.redis_password.get_secret_value()}@"
                f"{self.redis_host}:{self.redis_port}/{self.redis_db}"
            )
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    # ─────────────────────────────────────────────────────────────────────────
    # Memory Configuration
    # ─────────────────────────────────────────────────────────────────────────
    session_ttl_seconds: int = Field(
        default=1800,  # 30 minutes
        ge=60,
        description="Session TTL in seconds"
    )
    max_messages_before_summary: int = Field(
        default=20,
        ge=5,
        description="Maximum messages before triggering summarization"
    )
    working_memory_token_budget: int = Field(
        default=4000,
        ge=1000,
        description="Token budget for working memory"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # RAG Configuration
    # ─────────────────────────────────────────────────────────────────────────
    rag_top_k_retrieval: int = Field(
        default=50,
        ge=10,
        description="Number of documents to retrieve in initial search"
    )
    rag_top_k_rerank: int = Field(
        default=5,
        ge=1,
        description="Number of documents after reranking"
    )
    rag_similarity_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score for retrieval"
    )
    chunk_size: int = Field(
        default=512,
        ge=100,
        description="Target chunk size in tokens"
    )
    chunk_overlap: int = Field(
        default=100,
        ge=0,
        description="Overlap between chunks"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Agent Configuration
    # ─────────────────────────────────────────────────────────────────────────
    confidence_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for escalation"
    )
    max_llm_retries: int = Field(
        default=3,
        ge=1,
        description="Maximum retries for LLM calls"
    )
    response_timeout_seconds: int = Field(
        default=30,
        ge=5,
        description="Response timeout in seconds"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Business Configuration (Singapore SMB)
    # ─────────────────────────────────────────────────────────────────────────
    business_name: str = Field(
        default="Your Business",
        description="Business name for personalization"
    )
    business_timezone: str = Field(
        default="Asia/Singapore",
        description="Business timezone"
    )
    business_hours_start: str = Field(
        default="09:00",
        pattern=r"^\d{2}:\d{2}$",
        description="Business hours start time (HH:MM)"
    )
    business_hours_end: str = Field(
        default="18:00",
        pattern=r"^\d{2}:\d{2}$",
        description="Business hours end time (HH:MM)"
    )
    business_working_days: str = Field(
        default="Monday,Tuesday,Wednesday,Thursday,Friday",
        description="Comma-separated list of working days"
    )
    
    @property
    def working_days_list(self) -> list[str]:
        """Parse working days into a list."""
        return [day.strip() for day in self.business_working_days.split(",")]
    
    # ─────────────────────────────────────────────────────────────────────────
    # Logging Configuration
    # ─────────────────────────────────────────────────────────────────────────
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level"
    )
    log_format: Literal["json", "console"] = Field(
        default="json",
        description="Log output format"
    )
    log_file: str | None = Field(
        default=None,
        description="Log file path (optional)"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # PDPA Compliance Settings
    # ─────────────────────────────────────────────────────────────────────────
    data_retention_days: int = Field(
        default=30,
        ge=1,
        description="Data retention period in days"
    )
    enable_anonymization: bool = Field(
        default=True,
        description="Enable data anonymization for analytics"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Validators
    # ─────────────────────────────────────────────────────────────────────────
    @field_validator("app_debug")
    @classmethod
    def disable_debug_in_production(cls, v: bool, info) -> bool:
        """Ensure debug mode is disabled in production."""
        if info.data.get("app_env") == "production" and v:
            raise ValueError("Debug mode must be disabled in production")
        return v
    
    @model_validator(mode="after")
    def validate_chunk_settings(self) -> "Settings":
        """Ensure chunk overlap is less than chunk size."""
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return self


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Uses lru_cache to ensure settings are only loaded once
    and shared across the application.
    """
    return Settings()
