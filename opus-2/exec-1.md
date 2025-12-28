The user has approved my design and is asking me to proceed with implementation. They want me to:

Plan in logical phases
Proceed step by step
Build the complete working codebase according to my design
This is a substantial undertaking. Let me organize this properly:

I'll need to create detailed phase-by-phase implementation
Each phase should be complete before moving to the next
I need to provide production-ready, working code
Follow my own design document precisely
Let me start with Phase 1: Foundation - this includes:

Project setup with proper structure
Python environment configuration
FastAPI skeleton
React + TypeScript + Tailwind setup
Shadcn/UI initialization
Docker Compose for local development
Database infrastructure
Configuration management
Given the scope, I'll need to be strategic about how I present this. I'll work through each phase methodically, providing complete, working code files.

Let me begin with Phase 1 and create all the necessary files with detailed implementation.

I should also confirm my technology choices based on the approval:

GPT-4o-mini as primary LLM
Qdrant as vector database
Cohere for reranking (with local fallback option)
English primary, with Mandarin support built in
Docker Compose for development
Let me start building this out comprehensively.

---

Implementation Begins: Singapore SMB Customer Support AI Agent
text

╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║   ██╗███╗   ███╗██████╗ ██╗     ███████╗███╗   ███╗███████╗███╗   ██╗████████╗      ║
║   ██║████╗ ████║██╔══██╗██║     ██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝      ║
║   ██║██╔████╔██║██████╔╝██║     █████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║         ║
║   ██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║         ║
║   ██║██║ ╚═╝ ██║██║     ███████╗███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║         ║
║   ╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝         ║
║                                                                                      ║
║                              PHASE 1: FOUNDATION                                     ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
Phase 1: Foundation - Execution Checklist
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          PHASE 1 EXECUTION PLAN                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

PHASE 1.1: PROJECT SETUP
├── [•] Initialize repository structure
├── [•] Python environment (pyproject.toml + requirements.txt)
├── [•] FastAPI application skeleton
├── [•] Configuration management (Pydantic Settings)
└── [•] Logging configuration

PHASE 1.2: DATABASE INFRASTRUCTURE  
├── [•] PostgreSQL SQLAlchemy models
├── [•] Alembic migrations setup
├── [•] Redis connection configuration
└── [•] Qdrant collection setup

PHASE 1.3: DOCKER INFRASTRUCTURE
├── [•] Backend Dockerfile
├── [•] Docker Compose (dev environment)
└── [•] Environment configuration

Legend: [•] In Progress  [✓] Complete  [ ] Pending
1.1 Project Root Configuration
.gitignore
gitignore

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Environments
.env
.env.local
.env.*.local
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre
.pyre/

# Node
node_modules/
.next/
out/
.turbo/

# Build
dist/
.vercel

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local
*.local

# Testing
coverage/

# Misc
.DS_Store
*.pem
Thumbs.db

# Database
*.db
*.sqlite3

# Logs
logs/
*.log

# Uploaded files
uploads/
data/uploads/

# Vector DB data (local development)
qdrant_data/
README.md
Markdown

# Singapore SMB Customer Support AI Agent

A production-ready, context-aware AI customer support agent built for Singapore SMBs.

## Features

- 🤖 **Intelligent Responses**: Powered by GPT-4o-mini with RAG-grounded answers
- 🧠 **Memory System**: Short-term (Redis) + Long-term (PostgreSQL) memory
- 🔍 **Advanced RAG**: Multi-stage retrieval with hybrid search and reranking
- 🌏 **Multilingual**: English and Mandarin support
- 🔒 **PDPA Compliant**: Singapore data protection compliance built-in
- ⚡ **Real-time**: WebSocket-based streaming responses
- 📱 **Responsive UI**: Modern React chatbox interface

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- Pydantic AI
- LangChain 0.3.x
- Qdrant (Vector Database)
- Redis (Session Memory)
- PostgreSQL (Long-term Storage)

### Frontend
- React 18 + TypeScript
- Tailwind CSS
- Shadcn/UI Components
- Zustand (State Management)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd singapore-smb-support-agent
Set up environment variables

Bash

cp .env.example .env
# Edit .env with your API keys
Start infrastructure services

Bash

docker-compose up -d postgres redis qdrant
Install backend dependencies

Bash

cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
Run database migrations

Bash

alembic upgrade head
Seed knowledge base

Bash

python scripts/seed_knowledge.py
Start backend server

Bash

uvicorn app.main:app --reload --port 8000
Install frontend dependencies (new terminal)

Bash

cd frontend
npm install
Start frontend dev server

Bash

npm run dev
Access the application

Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
Project Structure
text

singapore-smb-support-agent/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── agent/          # Pydantic AI agent
│   │   ├── api/            # API routes
│   │   ├── ingestion/      # Document ingestion
│   │   ├── memory/         # Memory management
│   │   ├── models/         # Data models
│   │   ├── rag/            # RAG pipeline
│   │   └── services/       # Business services
│   ├── alembic/            # Database migrations
│   ├── scripts/            # Utility scripts
│   └── tests/              # Test suite
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── hooks/          # Custom hooks
│   │   ├── lib/            # Utilities
│   │   └── stores/         # State management
│   └── public/             # Static assets
├── infrastructure/         # Docker & deployment
└── docs/                   # Documentation
Configuration
See .env.example for all available configuration options.

API Documentation
Once the backend is running, visit:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
Testing
Bash

# Backend tests
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html

# RAG evaluation
python scripts/evaluate_rag.py
License
MIT License - see LICENSE file for details.

text


### `.env.example`

```env
# =============================================================================
# SINGAPORE SMB CUSTOMER SUPPORT AI AGENT - ENVIRONMENT CONFIGURATION
# =============================================================================
# Copy this file to .env and fill in your values
# NEVER commit .env to version control
# =============================================================================

# -----------------------------------------------------------------------------
# APPLICATION SETTINGS
# -----------------------------------------------------------------------------
APP_NAME="Singapore SMB Support Agent"
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_PREFIX=/api/v1

# Security
SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars
API_KEY=your-api-key-for-client-authentication
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# -----------------------------------------------------------------------------
# DATABASE SETTINGS
# -----------------------------------------------------------------------------
# PostgreSQL (Long-term Memory)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=support_agent
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=support_agent_db
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Redis (Short-term Memory)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_URL=redis://${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB}

# Session Settings
SESSION_TTL_SECONDS=1800  # 30 minutes
MAX_MESSAGES_BEFORE_SUMMARY=20

# -----------------------------------------------------------------------------
# VECTOR DATABASE SETTINGS (Qdrant)
# -----------------------------------------------------------------------------
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=knowledge_base
QDRANT_COLLECTION_SUMMARIES=document_summaries

# -----------------------------------------------------------------------------
# LLM SETTINGS
# -----------------------------------------------------------------------------
# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_MAX_TOKENS=2048
OPENAI_TEMPERATURE=0.7

# Fallback Model (Optional - Claude)
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-3-haiku-20240307

# -----------------------------------------------------------------------------
# RAG SETTINGS
# -----------------------------------------------------------------------------
# Retrieval
RAG_TOP_K_RETRIEVAL=50
RAG_TOP_K_RERANK=5
RAG_SIMILARITY_THRESHOLD=0.7

# Chunking
CHUNK_SIZE=512
CHUNK_OVERLAP=100
CHUNKING_STRATEGY=semantic  # semantic or recursive

# Reranking
RERANKER_PROVIDER=cohere  # cohere or local
COHERE_API_KEY=your-cohere-api-key
COHERE_RERANK_MODEL=rerank-english-v3.0

# Context
MAX_CONTEXT_TOKENS=4000
ENABLE_CONTEXT_COMPRESSION=true

# -----------------------------------------------------------------------------
# AGENT SETTINGS
# -----------------------------------------------------------------------------
AGENT_CONFIDENCE_THRESHOLD=0.7
AGENT_ESCALATION_ENABLED=true
AGENT_MAX_TOOL_CALLS=5

# Business Context
BUSINESS_NAME="Sample Singapore SMB"
BUSINESS_TIMEZONE=Asia/Singapore
BUSINESS_HOURS_START=09:00
BUSINESS_HOURS_END=18:00
BUSINESS_WORKING_DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday"]

# -----------------------------------------------------------------------------
# PDPA COMPLIANCE SETTINGS
# -----------------------------------------------------------------------------
PDPA_DATA_RETENTION_DAYS=30
PDPA_REQUIRE_CONSENT=true
PDPA_ANONYMIZE_ANALYTICS=true

# -----------------------------------------------------------------------------
# MONITORING & OBSERVABILITY
# -----------------------------------------------------------------------------
ENABLE_METRICS=true
METRICS_PORT=9090

# Sentry (Optional)
SENTRY_DSN=
SENTRY_ENVIRONMENT=${APP_ENV}

# -----------------------------------------------------------------------------
# FRONTEND SETTINGS (for reference)
# -----------------------------------------------------------------------------
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_APP_NAME=${APP_NAME}
Makefile
Makefile

# =============================================================================
# SINGAPORE SMB CUSTOMER SUPPORT AI AGENT - MAKEFILE
# =============================================================================

.PHONY: help install dev test lint format docker-up docker-down clean migrate seed

# Default target
help:
	@echo "Singapore SMB Customer Support AI Agent"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install       Install all dependencies"
	@echo "  dev           Start development environment"
	@echo "  test          Run all tests"
	@echo "  lint          Run linters"
	@echo "  format        Format code"
	@echo "  docker-up     Start Docker services"
	@echo "  docker-down   Stop Docker services"
	@echo "  migrate       Run database migrations"
	@echo "  seed          Seed knowledge base"
	@echo "  clean         Clean up generated files"

# =============================================================================
# INSTALLATION
# =============================================================================

install: install-backend install-frontend

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && pip install -e ".[dev]"

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# =============================================================================
# DEVELOPMENT
# =============================================================================

dev: docker-up
	@echo "Starting development servers..."
	@make -j2 dev-backend dev-frontend

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

# =============================================================================
# DOCKER
# =============================================================================

docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-logs:
	docker-compose logs -f

# =============================================================================
# DATABASE
# =============================================================================

migrate:
	@echo "Running database migrations..."
	cd backend && alembic upgrade head

migrate-create:
	@echo "Creating new migration..."
	cd backend && alembic revision --autogenerate -m "$(name)"

migrate-down:
	@echo "Rolling back migration..."
	cd backend && alembic downgrade -1

seed:
	@echo "Seeding knowledge base..."
	cd backend && python scripts/seed_knowledge.py

# =============================================================================
# TESTING
# =============================================================================

test: test-backend test-frontend

test-backend:
	@echo "Running backend tests..."
	cd backend && pytest -v

test-backend-cov:
	@echo "Running backend tests with coverage..."
	cd backend && pytest --cov=app --cov-report=html --cov-report=term

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm test

test-e2e:
	@echo "Running end-to-end tests..."
	cd frontend && npm run test:e2e

evaluate-rag:
	@echo "Running RAG evaluation..."
	cd backend && python scripts/evaluate_rag.py

# =============================================================================
# CODE QUALITY
# =============================================================================

lint: lint-backend lint-frontend

lint-backend:
	@echo "Linting backend..."
	cd backend && ruff check .
	cd backend && mypy app

lint-frontend:
	@echo "Linting frontend..."
	cd frontend && npm run lint

format: format-backend format-frontend

format-backend:
	@echo "Formatting backend..."
	cd backend && ruff format .
	cd backend && ruff check --fix .

format-frontend:
	@echo "Formatting frontend..."
	cd frontend && npm run format

# =============================================================================
# CLEANUP
# =============================================================================

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "Cleanup complete!"

# =============================================================================
# PRODUCTION
# =============================================================================

build-prod:
	@echo "Building production images..."
	docker-compose -f docker-compose.prod.yml build

deploy-prod:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.prod.yml up -d
1.2 Backend Foundation
backend/pyproject.toml
toml

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "singapore-smb-support-agent"
version = "1.0.0"
description = "Production-ready AI Customer Support Agent for Singapore SMBs"
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.11"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Framework :: FastAPI",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]
keywords = ["ai", "chatbot", "customer-support", "rag", "langchain", "fastapi"]

dependencies = [
    # Core Framework
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "python-multipart>=0.0.12",
    
    # Pydantic & Validation
    "pydantic>=2.9.0",
    "pydantic-settings>=2.6.0",
    "pydantic-ai>=0.0.24",
    
    # LangChain Ecosystem
    "langchain>=0.3.7",
    "langchain-core>=0.3.15",
    "langchain-community>=0.3.5",
    "langchain-openai>=0.2.5",
    "langchain-qdrant>=0.2.0",
    "langgraph>=0.2.45",
    
    # LLM Providers
    "openai>=1.55.0",
    "anthropic>=0.39.0",
    "cohere>=5.11.0",
    
    # Vector Database
    "qdrant-client>=1.12.0",
    
    # Embeddings & NLP
    "sentence-transformers>=3.3.0",
    "tiktoken>=0.8.0",
    
    # Database
    "sqlalchemy[asyncio]>=2.0.35",
    "asyncpg>=0.30.0",
    "alembic>=1.14.0",
    "greenlet>=3.1.0",
    
    # Redis
    "redis>=5.2.0",
    
    # Document Processing
    "unstructured[all-docs]>=0.16.0",
    "pypdf>=5.1.0",
    "python-docx>=1.1.0",
    "beautifulsoup4>=4.12.0",
    "lxml>=5.3.0",
    "markdown>=3.7",
    
    # HTTP & WebSocket
    "httpx>=0.27.0",
    "websockets>=13.1",
    
    # Utilities
    "python-dateutil>=2.9.0",
    "pytz>=2024.2",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "tenacity>=9.0.0",
    "structlog>=24.4.0",
    
    # Async Utilities
    "aiofiles>=24.1.0",
    "aiocache>=0.12.0",
]

[project.optional-dependencies]
dev = [
    # Testing
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "pytest-mock>=3.14.0",
    "httpx>=0.27.0",
    "faker>=30.0.0",
    
    # RAG Evaluation
    "ragas>=0.2.0",
    "deepeval>=1.3.0",
    
    # Code Quality
    "ruff>=0.7.0",
    "mypy>=1.13.0",
    "pre-commit>=4.0.0",
    
    # Type Stubs
    "types-redis>=4.6.0",
    "types-python-dateutil>=2.9.0",
    "types-pytz>=2024.2.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/singapore-smb-support-agent"
Documentation = "https://github.com/yourusername/singapore-smb-support-agent#readme"
Repository = "https://github.com/yourusername/singapore-smb-support-agent"
Issues = "https://github.com/yourusername/singapore-smb-support-agent/issues"

[tool.hatch.build.targets.wheel]
packages = ["app"]

# =============================================================================
# RUFF CONFIGURATION
# =============================================================================
[tool.ruff]
target-version = "py311"
line-length = 100
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "alembic/versions",
]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
]
ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # do not perform function calls in argument defaults
    "B009",   # do not call getattr with a constant attribute value
]

[tool.ruff.lint.isort]
known-first-party = ["app"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false

# =============================================================================
# MYPY CONFIGURATION
# =============================================================================
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_configs = true
show_error_codes = true
show_column_numbers = true

[[tool.mypy.overrides]]
module = [
    "unstructured.*",
    "langchain.*",
    "langchain_core.*",
    "langchain_community.*",
    "langchain_openai.*",
    "langchain_qdrant.*",
    "langgraph.*",
    "qdrant_client.*",
    "sentence_transformers.*",
    "cohere.*",
    "redis.*",
    "pydantic_ai.*",
    "ragas.*",
    "deepeval.*",
]
ignore_missing_imports = true

# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
    "ignore::UserWarning",
]

# =============================================================================
# COVERAGE CONFIGURATION
# =============================================================================
[tool.coverage.run]
source = ["app"]
branch = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/alembic/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
show_missing = true
backend/requirements.txt
text

# =============================================================================
# PRODUCTION DEPENDENCIES
# Generated from pyproject.toml for compatibility
# =============================================================================

# Core Framework
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
python-multipart>=0.0.12

# Pydantic & Validation
pydantic>=2.9.0
pydantic-settings>=2.6.0
pydantic-ai>=0.0.24

# LangChain Ecosystem
langchain>=0.3.7
langchain-core>=0.3.15
langchain-community>=0.3.5
langchain-openai>=0.2.5
langchain-qdrant>=0.2.0
langgraph>=0.2.45

# LLM Providers
openai>=1.55.0
anthropic>=0.39.0
cohere>=5.11.0

# Vector Database
qdrant-client>=1.12.0

# Embeddings & NLP
sentence-transformers>=3.3.0
tiktoken>=0.8.0

# Database
sqlalchemy[asyncio]>=2.0.35
asyncpg>=0.30.0
alembic>=1.14.0
greenlet>=3.1.0

# Redis
redis>=5.2.0

# Document Processing
unstructured>=0.16.0
pypdf>=5.1.0
python-docx>=1.1.0
beautifulsoup4>=4.12.0
lxml>=5.3.0
markdown>=3.7

# HTTP & WebSocket
httpx>=0.27.0
websockets>=13.1

# Utilities
python-dateutil>=2.9.0
pytz>=2024.2
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
tenacity>=9.0.0
structlog>=24.4.0

# Async Utilities
aiofiles>=24.1.0
aiocache>=0.12.0
backend/app/__init__.py
Python

"""
Singapore SMB Customer Support AI Agent

A production-ready, context-aware AI customer support agent
built for Singapore SMBs with advanced RAG capabilities.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
backend/app/config.py
Python

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
backend/app/logging_config.py
Python

"""
Structured Logging Configuration

Implements structured logging using structlog for consistent,
machine-parseable log output in both development and production.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import Processor

from app.config import settings


def setup_logging() -> None:
    """
    Configure structured logging for the application.
    
    In development: Human-readable colored console output
    In production: JSON-formatted logs for log aggregation
    """
    # Determine log level
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # Shared processors for all environments
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]
    
    if settings.is_development:
        # Development: Pretty console output
        processors: list[Processor] = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    else:
        # Production: JSON output
        processors = [
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )
    
    # Reduce noise from third-party libraries
    for logger_name in [
        "httpx",
        "httpcore",
        "uvicorn.access",
        "uvicorn.error",
        "sqlalchemy.engine",
        "openai",
        "anthropic",
        "langchain",
    ]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: Logger name, typically __name__
        
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


# Type alias for logger
Logger = structlog.BoundLogger
backend/app/main.py
Python

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
backend/app/database.py
Python

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
backend/app/dependencies.py
Python

"""
Dependency Injection Configuration

Centralized dependency management for FastAPI using dependency injection.
Includes Redis, Qdrant, and other service dependencies.
"""

from typing import Annotated, AsyncGenerator

import redis.asyncio as redis
from fastapi import Depends, Header, HTTPException, status
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.logging_config import get_logger

logger = get_logger(__name__)

# =============================================================================
# GLOBAL CLIENTS
# =============================================================================

_redis_client: redis.Redis | None = None
_qdrant_client: QdrantClient | None = None


# =============================================================================
# REDIS
# =============================================================================

async def init_redis() -> None:
    """Initialize Redis connection pool."""
    global _redis_client
    
    try:
        _redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
        )
        # Test connection
        await _redis_client.ping()
        logger.info("redis_connected", host=settings.redis_host, port=settings.redis_port)
    except Exception as e:
        logger.error("redis_connection_failed", error=str(e))
        raise


async def close_redis() -> None:
    """Close Redis connection pool."""
    global _redis_client
    
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("redis_disconnected")


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """Get Redis client dependency."""
    if _redis_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis connection not available",
        )
    yield _redis_client


# =============================================================================
# QDRANT
# =============================================================================

async def init_qdrant() -> None:
    """Initialize Qdrant client and collections."""
    global _qdrant_client
    
    try:
        # Create client
        api_key = settings.qdrant_api_key.get_secret_value()
        _qdrant_client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=api_key if api_key else None,
        )
        
        # Ensure collections exist
        await _ensure_collections()
        
        logger.info("qdrant_connected", host=settings.qdrant_host, port=settings.qdrant_port)
    except Exception as e:
        logger.error("qdrant_connection_failed", error=str(e))
        raise


async def _ensure_collections() -> None:
    """Ensure required Qdrant collections exist."""
    if _qdrant_client is None:
        return
    
    collections_to_create = [
        (settings.qdrant_collection_name, 1536),  # OpenAI text-embedding-3-small
        (settings.qdrant_collection_summaries, 1536),
    ]
    
    existing_collections = {
        col.name for col in _qdrant_client.get_collections().collections
    }
    
    for collection_name, vector_size in collections_to_create:
        if collection_name not in existing_collections:
            _qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=qdrant_models.VectorParams(
                    size=vector_size,
                    distance=qdrant_models.Distance.COSINE,
                ),
            )
            logger.info("qdrant_collection_created", collection=collection_name)
        else:
            logger.debug("qdrant_collection_exists", collection=collection_name)


def get_qdrant() -> QdrantClient:
    """Get Qdrant client dependency."""
    if _qdrant_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Qdrant connection not available",
        )
    return _qdrant_client


# =============================================================================
# AUTHENTICATION
# =============================================================================

async def verify_api_key(
    x_api_key: Annotated[str | None, Header()] = None
) -> str:
    """
    Verify API key from request header.
    
    In development mode, allows requests without API key.
    """
    if settings.is_development and not x_api_key:
        return "development"
    
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    if x_api_key != settings.api_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return x_api_key


# =============================================================================
# TYPE ALIASES FOR DEPENDENCY INJECTION
# =============================================================================

# Database session dependency
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Redis client dependency
RedisDep = Annotated[redis.Redis, Depends(get_redis)]

# Qdrant client dependency
QdrantDep = Annotated[QdrantClient, Depends(get_qdrant)]

# API key verification dependency
ApiKeyDep = Annotated[str, Depends(verify_api_key)]
1.3 API Routes Foundation
backend/app/api/__init__.py
Python

"""API routes package."""
backend/app/api/routes/__init__.py
Python

"""API route modules."""
backend/app/api/routes/health.py
Python

"""
Health Check Endpoints

Provides health and readiness endpoints for monitoring
and container orchestration systems.
"""

from datetime import datetime, timezone
from typing import Any

import redis.asyncio as redis
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from qdrant_client import QdrantClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.dependencies import get_session, get_redis, get_qdrant
from app.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter()


class HealthStatus(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    version: str
    environment: str


class ReadinessStatus(BaseModel):
    """Readiness check response model."""
    status: str
    timestamp: str
    checks: dict[str, Any]


@router.get(
    "/health",
    response_model=HealthStatus,
    summary="Health Check",
    description="Simple health check endpoint for load balancers",
)
async def health_check() -> HealthStatus:
    """
    Basic health check.
    
    Returns 200 OK if the application is running.
    Does not check dependencies.
    """
    return HealthStatus(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version="1.0.0",
        environment=settings.app_env,
    )


@router.get(
    "/ready",
    response_model=ReadinessStatus,
    summary="Readiness Check",
    description="Checks all dependencies are available",
)
async def readiness_check(
    session: AsyncSession = Depends(get_session),
    redis_client: redis.Redis = Depends(get_redis),
    qdrant_client: QdrantClient = Depends(get_qdrant),
) -> ReadinessStatus:
    """
    Comprehensive readiness check.
    
    Verifies all critical dependencies:
    - PostgreSQL database
    - Redis cache
    - Qdrant vector database
    """
    checks: dict[str, Any] = {}
    all_healthy = True
    
    # Check PostgreSQL
    try:
        await session.execute(text("SELECT 1"))
        checks["postgresql"] = {"status": "healthy"}
    except Exception as e:
        logger.error("postgresql_health_check_failed", error=str(e))
        checks["postgresql"] = {"status": "unhealthy", "error": str(e)}
        all_healthy = False
    
    # Check Redis
    try:
        await redis_client.ping()
        checks["redis"] = {"status": "healthy"}
    except Exception as e:
        logger.error("redis_health_check_failed", error=str(e))
        checks["redis"] = {"status": "unhealthy", "error": str(e)}
        all_healthy = False
    
    # Check Qdrant
    try:
        qdrant_client.get_collections()
        checks["qdrant"] = {"status": "healthy"}
    except Exception as e:
        logger.error("qdrant_health_check_failed", error=str(e))
        checks["qdrant"] = {"status": "unhealthy", "error": str(e)}
        all_healthy = False
    
    response = ReadinessStatus(
        status="ready" if all_healthy else "not_ready",
        timestamp=datetime.now(timezone.utc).isoformat(),
        checks=checks,
    )
    
    if not all_healthy:
        # Return 503 if any dependency is unhealthy
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=response.model_dump(),
        )
    
    return response


@router.get(
    "/info",
    summary="Application Info",
    description="Returns application metadata",
)
async def app_info() -> dict[str, Any]:
    """Return application information."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "environment": settings.app_env,
        "debug": settings.debug,
        "docs_url": "/docs" if settings.is_development else None,
    }
backend/app/api/routes/chat.py
Python

"""
Chat API Endpoints

Handles customer chat interactions with the AI support agent.
Supports both REST and WebSocket communication.
"""

from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel, Field

from app.config import settings
from app.dependencies import SessionDep, RedisDep, ApiKeyDep
from app.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/chat")


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class ChatMessage(BaseModel):
    """A single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ChatRequest(BaseModel):
    """Chat request from client."""
    message: str = Field(..., min_length=1, max_length=4000, description="User message")
    session_id: str | None = Field(default=None, description="Session ID for conversation continuity")
    customer_id: str | None = Field(default=None, description="Optional customer identifier")
    metadata: dict | None = Field(default=None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What are your business hours?",
                "session_id": "sess_abc123",
                "customer_id": "cust_xyz789",
            }
        }


class SourceCitation(BaseModel):
    """Citation from knowledge base."""
    source: str = Field(..., description="Source document identifier")
    content: str = Field(..., description="Relevant excerpt")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class ChatResponse(BaseModel):
    """Chat response to client."""
    session_id: str = Field(..., description="Session ID for conversation continuity")
    message: str = Field(..., description="Agent response message")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence score")
    sources: list[SourceCitation] = Field(default_factory=list, description="Knowledge base sources")
    suggested_actions: list[str] = Field(default_factory=list, description="Suggested follow-up actions")
    requires_escalation: bool = Field(default=False, description="Whether human escalation is needed")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "sess_abc123",
                "message": "Our business hours are Monday to Friday, 9 AM to 6 PM Singapore Time.",
                "confidence": 0.95,
                "sources": [
                    {
                        "source": "faq_business_hours",
                        "content": "We operate from 9 AM to 6 PM SGT, Monday through Friday.",
                        "relevance_score": 0.92,
                    }
                ],
                "suggested_actions": ["View location", "Contact us"],
                "requires_escalation": False,
            }
        }


class ConversationHistory(BaseModel):
    """Conversation history response."""
    session_id: str
    messages: list[ChatMessage]
    created_at: str
    updated_at: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post(
    "",
    response_model=ChatResponse,
    summary="Send Chat Message",
    description="Send a message to the AI support agent and receive a response",
)
async def send_message(
    request: ChatRequest,
    session: SessionDep,
    redis: RedisDep,
    api_key: ApiKeyDep,
) -> ChatResponse:
    """
    Process a chat message and return AI response.
    
    This endpoint:
    1. Loads or creates a session
    2. Retrieves relevant context from knowledge base
    3. Generates a response using the AI agent
    4. Stores the conversation in memory
    """
    # Generate session ID if not provided
    session_id = request.session_id or f"sess_{uuid4().hex[:12]}"
    
    logger.info(
        "chat_message_received",
        session_id=session_id,
        message_length=len(request.message),
        customer_id=request.customer_id,
    )
    
    # TODO: Implement full agent pipeline in Phase 5
    # For now, return a placeholder response
    
    response = ChatResponse(
        session_id=session_id,
        message=f"Thank you for your message. Our AI agent is being set up and will be fully operational soon. You asked: '{request.message[:100]}...'",
        confidence=0.0,
        sources=[],
        suggested_actions=["Contact support for immediate assistance"],
        requires_escalation=True,
    )
    
    logger.info(
        "chat_response_sent",
        session_id=session_id,
        confidence=response.confidence,
        requires_escalation=response.requires_escalation,
    )
    
    return response


@router.get(
    "/history/{session_id}",
    response_model=ConversationHistory,
    summary="Get Conversation History",
    description="Retrieve the conversation history for a session",
)
async def get_conversation_history(
    session_id: str,
    redis: RedisDep,
    api_key: ApiKeyDep,
) -> ConversationHistory:
    """
    Retrieve conversation history for a session.
    
    Returns all messages exchanged in the specified session.
    """
    # TODO: Implement memory retrieval in Phase 4
    
    # For now, return empty history
    return ConversationHistory(
        session_id=session_id,
        messages=[],
        created_at=datetime.now(timezone.utc).isoformat(),
        updated_at=datetime.now(timezone.utc).isoformat(),
    )


@router.delete(
    "/history/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Conversation History",
    description="Delete conversation history for PDPA compliance",
)
async def delete_conversation_history(
    session_id: str,
    redis: RedisDep,
    api_key: ApiKeyDep,
) -> None:
    """
    Delete conversation history.
    
    Supports PDPA right to erasure requirements.
    """
    # TODO: Implement in Phase 4
    logger.info("conversation_history_deleted", session_id=session_id)


# =============================================================================
# WEBSOCKET ENDPOINT
# =============================================================================

@router.websocket("/ws/{session_id}")
async def websocket_chat(
    websocket: WebSocket,
    session_id: str,
) -> None:
    """
    WebSocket endpoint for real-time chat.
    
    Enables streaming responses for better UX.
    """
    await websocket.accept()
    
    logger.info("websocket_connected", session_id=session_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = data.get("message", "")
            
            logger.debug(
                "websocket_message_received",
                session_id=session_id,
                message_length=len(message),
            )
            
            # TODO: Implement streaming response in Phase 6
            # For now, send placeholder response
            
            await websocket.send_json({
                "type": "response",
                "session_id": session_id,
                "message": f"Received: {message}",
                "confidence": 0.0,
                "done": True,
            })
            
    except WebSocketDisconnect:
        logger.info("websocket_disconnected", session_id=session_id)
    except Exception as e:
        logger.error("websocket_error", session_id=session_id, error=str(e))
        await websocket.close(code=1011, reason=str(e))
backend/app/api/routes/knowledge.py
Python

"""
Knowledge Base API Endpoints

Handles knowledge base management including document upload,
search, and administration.
"""

from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from pydantic import BaseModel, Field

from app.config import settings
from app.dependencies import SessionDep, QdrantDep, ApiKeyDep
from app.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/knowledge")


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class DocumentMetadata(BaseModel):
    """Metadata for a knowledge base document."""
    source: str = Field(..., description="Source identifier")
    category: str = Field(..., description="Document category")
    language: str = Field(default="en", description="Document language code")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SearchResult(BaseModel):
    """A single search result from the knowledge base."""
    id: str = Field(..., description="Document chunk ID")
    content: str = Field(..., description="Document content")
    metadata: DocumentMetadata
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class SearchRequest(BaseModel):
    """Search request for the knowledge base."""
    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of results to return")
    category: str | None = Field(default=None, description="Filter by category")
    language: str | None = Field(default=None, description="Filter by language")


class SearchResponse(BaseModel):
    """Search response from the knowledge base."""
    query: str
    results: list[SearchResult]
    total_results: int
    search_time_ms: float


class UploadResponse(BaseModel):
    """Response after document upload."""
    document_id: str
    filename: str
    chunks_created: int
    status: str


class KnowledgeBaseStats(BaseModel):
    """Knowledge base statistics."""
    total_documents: int
    total_chunks: int
    categories: dict[str, int]
    languages: dict[str, int]
    last_updated: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search Knowledge Base",
    description="Search the knowledge base using semantic similarity",
)
async def search_knowledge_base(
    request: SearchRequest,
    qdrant: QdrantDep,
    api_key: ApiKeyDep,
) -> SearchResponse:
    """
    Perform semantic search on the knowledge base.
    
    Uses hybrid search (dense + sparse vectors) with optional
    metadata filtering for category and language.
    """
    import time
    start_time = time.time()
    
    logger.info(
        "knowledge_search_started",
        query_length=len(request.query),
        top_k=request.top_k,
        category=request.category,
    )
    
    # TODO: Implement full RAG retrieval in Phase 3
    # For now, return empty results
    
    search_time_ms = (time.time() - start_time) * 1000
    
    response = SearchResponse(
        query=request.query,
        results=[],
        total_results=0,
        search_time_ms=search_time_ms,
    )
    
    logger.info(
        "knowledge_search_completed",
        total_results=response.total_results,
        search_time_ms=search_time_ms,
    )
    
    return response


@router.post(
    "/upload",
    response_model=UploadResponse,
    summary="Upload Document",
    description="Upload a document to the knowledge base",
)
async def upload_document(
    file: Annotated[UploadFile, File(description="Document file (PDF, DOCX, TXT, MD)")],
    category: Annotated[str, Query(description="Document category")],
    language: Annotated[str, Query(default="en", description="Document language")],
    session: SessionDep,
    qdrant: QdrantDep,
    api_key: ApiKeyDep,
) -> UploadResponse:
    """
    Upload and process a document into the knowledge base.
    
    Supports:
    - PDF files
    - Word documents (.docx)
    - Text files (.txt)
    - Markdown files (.md)
    
    The document will be parsed, chunked, and embedded.
    """
    # Validate file type
    allowed_extensions = {".pdf", ".docx", ".txt", ".md"}
    file_ext = "." + (file.filename or "").split(".")[-1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed types: {allowed_extensions}",
        )
    
    document_id = f"doc_{uuid4().hex[:12]}"
    
    logger.info(
        "document_upload_started",
        document_id=document_id,
        filename=file.filename,
        category=category,
    )
    
    # TODO: Implement document processing in Phase 2
    # For now, return placeholder response
    
    response = UploadResponse(
        document_id=document_id,
        filename=file.filename or "unknown",
        chunks_created=0,
        status="pending",
    )
    
    logger.info(
        "document_upload_completed",
        document_id=document_id,
        chunks_created=response.chunks_created,
    )
    
    return response


@router.get(
    "/stats",
    response_model=KnowledgeBaseStats,
    summary="Get Knowledge Base Statistics",
    description="Get statistics about the knowledge base",
)
async def get_knowledge_base_stats(
    qdrant: QdrantDep,
    api_key: ApiKeyDep,
) -> KnowledgeBaseStats:
    """
    Retrieve statistics about the knowledge base.
    
    Includes document counts, category breakdown,
    and language distribution.
    """
    # TODO: Implement proper stats retrieval
    
    return KnowledgeBaseStats(
        total_documents=0,
        total_chunks=0,
        categories={},
        languages={},
        last_updated=datetime.now(timezone.utc).isoformat(),
    )


@router.delete(
    "/document/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Document",
    description="Delete a document from the knowledge base",
)
async def delete_document(
    document_id: str,
    session: SessionDep,
    qdrant: QdrantDep,
    api_key: ApiKeyDep,
) -> None:
    """
    Delete a document and all its chunks from the knowledge base.
    """
    logger.info("document_delete_started", document_id=document_id)
    
    # TODO: Implement document deletion in Phase 2
    
    logger.info("document_deleted", document_id=document_id)
1.4 Database Models
backend/app/models/__init__.py
Python

"""Data models package."""

from app.models.schemas import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    SourceCitation,
)
from app.models.database import (
    Customer,
    Conversation,
    ConversationMessage,
    Document,
    SupportTicket,
)
from app.models.domain import (
    MessageRole,
    TicketStatus,
    TicketPriority,
)

__all__ = [
    # Schemas
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "SourceCitation",
    # Database Models
    "Customer",
    "Conversation",
    "ConversationMessage",
    "Document",
    "SupportTicket",
    # Domain
    "MessageRole",
    "TicketStatus",
    "TicketPriority",
]
backend/app/models/domain.py
Python

"""
Domain Models and Enums

Core domain types used throughout the application.
"""

from enum import Enum


class MessageRole(str, Enum):
    """Chat message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class TicketStatus(str, Enum):
    """Support ticket statuses."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    """Support ticket priorities."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class DocumentCategory(str, Enum):
    """Knowledge base document categories."""
    FAQ = "faq"
    PRODUCT = "product"
    POLICY = "policy"
    PRICING = "pricing"
    SUPPORT = "support"
    GENERAL = "general"


class Language(str, Enum):
    """Supported languages."""
    ENGLISH = "en"
    CHINESE = "zh"
    MALAY = "ms"
    TAMIL = "ta"


class ConsentStatus(str, Enum):
    """PDPA consent status."""
    PENDING = "pending"
    GRANTED = "granted"
    REVOKED = "revoked"
backend/app/models/database.py
Python

"""
SQLAlchemy Database Models

Defines the PostgreSQL schema for long-term persistent storage.
Follows PDPA compliance requirements for data retention.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.domain import (
    ConsentStatus,
    DocumentCategory,
    Language,
    MessageRole,
    TicketPriority,
    TicketStatus,
)


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid4())


class Customer(Base):
    """
    Customer profile for long-term storage.
    
    Stores customer information with PDPA compliance considerations.
    """
    __tablename__ = "customers"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
    )
    external_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
        comment="External customer ID from client system",
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    language_preference: Mapped[str] = mapped_column(
        SQLEnum(Language),
        default=Language.ENGLISH,
    )
    
    # PDPA Compliance
    consent_status: Mapped[str] = mapped_column(
        SQLEnum(ConsentStatus),
        default=ConsentStatus.PENDING,
    )
    consent_timestamp: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    data_retention_days: Mapped[int] = mapped_column(Integer, default=30)
    
    # Metadata
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
    
    # Relationships
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    tickets: Mapped[list["SupportTicket"]] = relationship(
        "SupportTicket",
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        Index("ix_customers_consent", "consent_status"),
        Index("ix_customers_created", "created_at"),
    )


class Conversation(Base):
    """
    Conversation record for long-term storage.
    
    Stores conversation metadata and summaries.
    Individual messages are stored separately.
    """
    __tablename__ = "conversations"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
    )
    session_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        comment="Session ID for linking with Redis short-term memory",
    )
    customer_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    # Conversation metadata
    title: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Auto-generated conversation title",
    )
    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Rolling summary of conversation",
    )
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_escalated: Mapped[bool] = mapped_column(Boolean, default=False)
    escalation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Analytics
    avg_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    topics: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="PDPA data retention expiry",
    )
    
    # Relationships
    customer: Mapped[Optional["Customer"]] = relationship(
        "Customer",
        back_populates="conversations",
    )
    messages: Mapped[list["ConversationMessage"]] = relationship(
        "ConversationMessage",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="ConversationMessage.created_at",
    )
    
    __table_args__ = (
        Index("ix_conversations_active", "is_active"),
        Index("ix_conversations_expires", "expires_at"),
    )


class ConversationMessage(Base):
    """
    Individual message in a conversation.
    
    Stored in PostgreSQL for long-term persistence.
    Redis is used for short-term session storage.
    """
    __tablename__ = "conversation_messages"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
    )
    conversation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    
    # Message content
    role: Mapped[str] = mapped_column(SQLEnum(MessageRole))
    content: Mapped[str] = mapped_column(Text)
    
    # AI response metadata (for assistant messages)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sources: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    token_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        index=True,
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )
    
    __table_args__ = (
        Index("ix_messages_conversation_created", "conversation_id", "created_at"),
    )


class Document(Base):
    """
    Knowledge base document metadata.
    
    Stores document information; actual embeddings are in Qdrant.
    """
    __tablename__ = "documents"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
    )
    
    # Document info
    filename: Mapped[str] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(
        SQLEnum(DocumentCategory),
        index=True,
    )
    language: Mapped[str] = mapped_column(
        SQLEnum(Language),
        default=Language.ENGLISH,
        index=True,
    )
    
    # Processing status
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    processing_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_hash: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        unique=True,
        comment="SHA-256 hash for deduplication",
    )
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
    
    __table_args__ = (
        Index("ix_documents_category_lang", "category", "language"),
        Index("ix_documents_processed", "is_processed"),
    )


class SupportTicket(Base):
    """
    Support ticket for escalated conversations.
    
    Created when AI agent escalates to human support.
    """
    __tablename__ = "support_tickets"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
    )
    ticket_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    
    # Relationships
    customer_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    conversation_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Ticket details
    subject: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        SQLEnum(TicketStatus),
        default=TicketStatus.OPEN,
        index=True,
    )
    priority: Mapped[str] = mapped_column(
        SQLEnum(TicketPriority),
        default=TicketPriority.MEDIUM,
        index=True,
    )
    
    # Assignment
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Resolution
    resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
    
    # Relationships
    customer: Mapped[Optional["Customer"]] = relationship(
        "Customer",
        back_populates="tickets",
    )
    
    __table_args__ = (
        Index("ix_tickets_status_priority", "status", "priority"),
        Index("ix_tickets_created", "created_at"),
    )
backend/app/models/schemas.py
Python

"""
Pydantic Schemas for API

Request and response models for the API layer.
Separate from database models for flexibility.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# =============================================================================
# CHAT SCHEMAS
# =============================================================================

class ChatMessage(BaseModel):
    """A single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(default=None, description="ISO timestamp")


class SourceCitation(BaseModel):
    """Citation from knowledge base."""
    source: str = Field(..., description="Source document identifier")
    content: str = Field(..., description="Relevant excerpt")
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[dict[str, Any]] = Field(default=None)


class ChatRequest(BaseModel):
    """Chat request from client."""
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: Optional[str] = Field(default=None)
    customer_id: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default="en")
    metadata: Optional[dict[str, Any]] = Field(default=None)


class ChatResponse(BaseModel):
    """Chat response to client."""
    session_id: str
    message: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources: list[SourceCitation] = Field(default_factory=list)
    suggested_actions: list[str] = Field(default_factory=list)
    requires_escalation: bool = Field(default=False)
    timestamp: str


# =============================================================================
# KNOWLEDGE BASE SCHEMAS
# =============================================================================

class DocumentMetadata(BaseModel):
    """Metadata for a knowledge base document."""
    source: str
    category: str
    language: str = "en"
    created_at: Optional[str] = None
    custom: Optional[dict[str, Any]] = None


class ChunkMetadata(BaseModel):
    """Metadata for a document chunk."""
    document_id: str
    chunk_index: int
    source: str
    category: str
    language: str
    created_at: str


class SearchResult(BaseModel):
    """A single search result."""
    id: str
    content: str
    score: float
    metadata: ChunkMetadata


# =============================================================================
# CUSTOMER SCHEMAS
# =============================================================================

class CustomerProfile(BaseModel):
    """Customer profile for context."""
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    language_preference: str = "en"
    previous_topics: list[str] = Field(default_factory=list)
    metadata: Optional[dict[str, Any]] = None


# =============================================================================
# TICKET SCHEMAS
# =============================================================================

class TicketCreate(BaseModel):
    """Request to create a support ticket."""
    subject: str = Field(..., max_length=500)
    description: str
    priority: str = "medium"
    customer_id: Optional[str] = None
    conversation_id: Optional[str] = None


class TicketResponse(BaseModel):
    """Response after ticket creation."""
    ticket_id: str
    ticket_number: str
    status: str
    created_at: str
1.5 Alembic Migrations Setup
backend/alembic.ini
ini

# Alembic Configuration
# See https://alembic.sqlalchemy.org/en/latest/tutorial.html

[alembic]
# Path to migration scripts
script_location = alembic

# Template for migration file names
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# Truncate slug at this many characters
truncate_slug_length = 40

# Set to 'true' to run environment.py within the transaction
# Do not set if using async
# transaction_per_migration = true

# Set timezone for file_template
timezone = UTC

# Use revision ID in migration file names
revision_environment = false

# Prepend environment to revision ID
sourceless = false

# Inline output for version locations
version_locations = %(here)s/alembic/versions

# Output encoding
output_encoding = utf-8

# SQLAlchemy URL (overridden in env.py)
sqlalchemy.url = driver://user:pass@localhost/dbname

[post_write_hooks]
# Uncomment to run ruff after generating migrations
# hooks = ruff
# ruff.type = console_scripts
# ruff.entrypoint = ruff
# ruff.options = format REVISION_SCRIPT_FILENAME

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
backend/alembic/env.py
Python

"""
Alembic Environment Configuration

Configures Alembic to work with our SQLAlchemy models
and async database connection.
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Import settings and models
from app.config import settings
from app.database import Base
from app.models import database  # noqa: F401 - Import to register models

# Alembic Config object
config = context.config

# Set SQLAlchemy URL from settings
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with a database connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
backend/alembic/script.py.mako
mako

"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade database schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade database schema."""
    ${downgrades if downgrades else "pass"}

backend/alembic/versions/.gitkeep
text

# Keep this directory for Alembic migrations
1.6 Docker Configuration
docker-compose.yml
YAML

# =============================================================================
# DEVELOPMENT DOCKER COMPOSE
# Singapore SMB Customer Support AI Agent
# =============================================================================

version: "3.9"

services:
  # ===========================================================================
  # PostgreSQL - Long-term Memory Storage
  # ===========================================================================
  
