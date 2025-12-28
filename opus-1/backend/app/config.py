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
