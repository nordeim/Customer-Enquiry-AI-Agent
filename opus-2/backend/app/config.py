"""
Configuration Management

Centralized configuration using Pydantic Settings with environment variable support.
Follows the 12-factor app methodology for configuration management.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables.
    Secrets are wrapped in SecretStr for security.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # =========================================================================
    # APPLICATION SETTINGS
    # =========================================================================
    app_name: str = Field(default="Singapore SMB Support Agent")
    app_env: Literal["development", "staging", "production"] = Field(default="development")
    debug: bool = Field(default=False)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="INFO")
    
    # API Settings
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    api_prefix: str = Field(default="/api/v1")
    
    # Security
    secret_key: SecretStr = Field(default=SecretStr("change-me-in-production-min-32-chars"))
    api_key: SecretStr = Field(default=SecretStr("change-me-api-key"))
    cors_origins: list[str] = Field(default=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # =========================================================================
    # DATABASE SETTINGS
    # =========================================================================
    # PostgreSQL
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="support_agent")
    postgres_password: SecretStr = Field(default=SecretStr("password"))
    postgres_db: str = Field(default="support_agent_db")
    
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
    
    # Redis
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_password: SecretStr = Field(default=SecretStr(""))
    redis_db: int = Field(default=0)
    
    @property
    def redis_url(self) -> str:
        """Construct Redis connection URL."""
        password = self.redis_password.get_secret_value()
        if password:
            return f"redis://:{password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    # Session Settings
    session_ttl_seconds: int = Field(default=1800)  # 30 minutes
    max_messages_before_summary: int = Field(default=20)
    
    # =========================================================================
    # VECTOR DATABASE SETTINGS (Qdrant)
    # =========================================================================
    qdrant_host: str = Field(default="localhost")
    qdrant_port: int = Field(default=6333)
    qdrant_api_key: SecretStr = Field(default=SecretStr(""))
    qdrant_collection_name: str = Field(default="knowledge_base")
    qdrant_collection_summaries: str = Field(default="document_summaries")
    
    # =========================================================================
    # LLM SETTINGS
    # =========================================================================
    # OpenAI
    openai_api_key: SecretStr = Field(default=SecretStr(""))
    openai_model: str = Field(default="gpt-4o-mini")
    openai_embedding_model: str = Field(default="text-embedding-3-small")
    openai_max_tokens: int = Field(default=2048)
    openai_temperature: float = Field(default=0.7)
    
    # Anthropic (Fallback)
    anthropic_api_key: SecretStr = Field(default=SecretStr(""))
    anthropic_model: str = Field(default="claude-3-haiku-20240307")
    
    # =========================================================================
    # RAG SETTINGS
    # =========================================================================
    # Retrieval
    rag_top_k_retrieval: int = Field(default=50)
    rag_top_k_rerank: int = Field(default=5)
    rag_similarity_threshold: float = Field(default=0.7)
    
    # Chunking
    chunk_size: int = Field(default=512)
    chunk_overlap: int = Field(default=100)
    chunking_strategy: Literal["semantic", "recursive"] = Field(default="semantic")
    
    # Reranking
    reranker_provider: Literal["cohere", "local"] = Field(default="cohere")
    cohere_api_key: SecretStr = Field(default=SecretStr(""))
    cohere_rerank_model: str = Field(default="rerank-english-v3.0")
    
    # Context
    max_context_tokens: int = Field(default=4000)
    enable_context_compression: bool = Field(default=True)
    
    # =========================================================================
    # AGENT SETTINGS
    # =========================================================================
    agent_confidence_threshold: float = Field(default=0.7)
    agent_escalation_enabled: bool = Field(default=True)
    agent_max_tool_calls: int = Field(default=5)
    
    # Business Context
    business_name: str = Field(default="Sample Singapore SMB")
    business_timezone: str = Field(default="Asia/Singapore")
    business_hours_start: str = Field(default="09:00")
    business_hours_end: str = Field(default="18:00")
    business_working_days: list[str] = Field(
        default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    )
    
    # =========================================================================
    # PDPA COMPLIANCE SETTINGS
    # =========================================================================
    pdpa_data_retention_days: int = Field(default=30)
    pdpa_require_consent: bool = Field(default=True)
    pdpa_anonymize_analytics: bool = Field(default=True)
    
    # =========================================================================
    # MONITORING
    # =========================================================================
    enable_metrics: bool = Field(default=True)
    metrics_port: int = Field(default=9090)
    sentry_dsn: str = Field(default="")
    
    # =========================================================================
    # VALIDATORS
    # =========================================================================
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("business_working_days", mode="before")
    @classmethod
    def parse_working_days(cls, v: str | list[str]) -> list[str]:
        """Parse working days from string or list."""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [day.strip() for day in v.split(",")]
        return v
    
    # =========================================================================
    # COMPUTED PROPERTIES
    # =========================================================================
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to ensure settings are only loaded once.
    """
    return Settings()


# Expose settings instance for convenience
settings = get_settings()
