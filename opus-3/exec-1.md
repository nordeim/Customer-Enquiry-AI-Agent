The user has approved my design and wants me to proceed with building the complete working codebase. They've emphasized keeping up the rigorous and meticulous approach. They want me to:

Plan in logical phases
Proceed step by step
Build the complete working codebase according to my design
Since they didn't specify answers to my decision points, I'll make reasonable default decisions:

GPT-4o-mini as primary LLM (cost-effective)
Qdrant as vector database (as designed)
Cohere for reranking (with fallback to local)
Start with English, prepare for Mandarin
Docker Compose for development
Create sample data for demonstration
Follow the 10-phase roadmap
Now, let me begin with Phase 1: Foundation. I need to be extremely thorough and create production-ready code. Let me structure this carefully.

Given the scope, I'll need to deliver this across multiple responses. Let me start with Phase 1 which includes:

Project setup
Configuration management
Database infrastructure setup
FastAPI skeleton
Basic React setup with Shadcn/UI
I'll create all the necessary files with complete, working code. Let me be meticulous about this.

---

Implementation Phase 1: Foundation
text

╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║   ██████╗ ██╗  ██╗ █████╗ ███████╗███████╗     ██╗                                  ║
║   ██╔══██╗██║  ██║██╔══██╗██╔════╝██╔════╝    ███║                                  ║
║   ██████╔╝███████║███████║███████╗█████╗      ╚██║                                  ║
║   ██╔═══╝ ██╔══██║██╔══██║╚════██║██╔══╝       ██║                                  ║
║   ██║     ██║  ██║██║  ██║███████║███████╗     ██║                                  ║
║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝     ╚═╝                                  ║
║                                                                                      ║
║                         F O U N D A T I O N                                          ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
Default Decisions Applied
Since no specific overrides were provided, I'm proceeding with these defaults:

Decision	Selection	Rationale
Primary LLM	GPT-4o-mini	Cost-effective, fast
Vector DB	Qdrant	Production-ready, rich filtering
Reranker	Cohere (primary) + bge-reranker (fallback)	Best quality + local option
Language	English first, Mandarin-ready	Phased approach
Deployment	Docker Compose	Development-first
Sample Data	Will create comprehensive samples	Demonstration ready
Phase 1.1: Project Initialization
Root Project Structure
text

singapore-smb-support-agent/
├── backend/
├── frontend/
├── infrastructure/
├── docs/
├── .env.example
├── .gitignore
├── README.md
├── Makefile
└── docker-compose.yml
File: .gitignore
gitignore

# ══════════════════════════════════════════════════════════════════════════════
# Singapore SMB Support Agent - Git Ignore Configuration
# ══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# Environment & Secrets
# ─────────────────────────────────────────────────────────────────────────────
.env
.env.local
.env.*.local
*.pem
*.key
secrets/

# ─────────────────────────────────────────────────────────────────────────────
# Python
# ─────────────────────────────────────────────────────────────────────────────
__pycache__/
*.py[cod]
*$py.class
*.so
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
MANIFEST
.venv/
venv/
ENV/
env/
.python-version

# ─────────────────────────────────────────────────────────────────────────────
# Node.js / Frontend
# ─────────────────────────────────────────────────────────────────────────────
node_modules/
.next/
out/
.nuxt/
dist/
.cache/
*.tsbuildinfo
next-env.d.ts

# ─────────────────────────────────────────────────────────────────────────────
# IDE & Editors
# ─────────────────────────────────────────────────────────────────────────────
.idea/
.vscode/
*.swp
*.swo
*~
.project
.classpath
.settings/
*.sublime-workspace
*.sublime-project

# ─────────────────────────────────────────────────────────────────────────────
# Testing & Coverage
# ─────────────────────────────────────────────────────────────────────────────
.coverage
.coverage.*
htmlcov/
.tox/
.nox/
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
pytest_cache/
.ruff_cache/
.mypy_cache/

# ─────────────────────────────────────────────────────────────────────────────
# Database & Data
# ─────────────────────────────────────────────────────────────────────────────
*.db
*.sqlite3
*.sqlite
*.sql
data/uploads/
data/processed/
qdrant_storage/

# ─────────────────────────────────────────────────────────────────────────────
# Logs
# ─────────────────────────────────────────────────────────────────────────────
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# ─────────────────────────────────────────────────────────────────────────────
# Docker
# ─────────────────────────────────────────────────────────────────────────────
docker-compose.override.yml

# ─────────────────────────────────────────────────────────────────────────────
# OS Generated
# ─────────────────────────────────────────────────────────────────────────────
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# ─────────────────────────────────────────────────────────────────────────────
# Temporary Files
# ─────────────────────────────────────────────────────────────────────────────
tmp/
temp/
*.tmp
*.bak
*.backup
File: .env.example
Bash

# ══════════════════════════════════════════════════════════════════════════════
# Singapore SMB Support Agent - Environment Configuration
# ══════════════════════════════════════════════════════════════════════════════
# Copy this file to .env and fill in your values
# NEVER commit .env to version control
# ══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# Application Settings
# ─────────────────────────────────────────────────────────────────────────────
APP_NAME="Singapore SMB Support Agent"
APP_ENV=development
APP_DEBUG=true
APP_SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars

# ─────────────────────────────────────────────────────────────────────────────
# API Configuration
# ─────────────────────────────────────────────────────────────────────────────
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_RELOAD=true

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000

# ─────────────────────────────────────────────────────────────────────────────
# LLM Configuration
# ─────────────────────────────────────────────────────────────────────────────
# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Anthropic (fallback)
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Cohere (for reranking)
COHERE_API_KEY=your-cohere-api-key-here

# ─────────────────────────────────────────────────────────────────────────────
# Vector Database (Qdrant)
# ─────────────────────────────────────────────────────────────────────────────
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=knowledge_base
QDRANT_SUMMARIES_COLLECTION=document_summaries

# ─────────────────────────────────────────────────────────────────────────────
# PostgreSQL Database
# ─────────────────────────────────────────────────────────────────────────────
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=support_agent
POSTGRES_USER=support_agent
POSTGRES_PASSWORD=your-secure-postgres-password

# Connection URL (constructed from above)
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# ─────────────────────────────────────────────────────────────────────────────
# Redis Configuration
# ─────────────────────────────────────────────────────────────────────────────
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Redis URL (constructed from above)
REDIS_URL=redis://:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB}

# ─────────────────────────────────────────────────────────────────────────────
# Memory Configuration
# ─────────────────────────────────────────────────────────────────────────────
# Short-term memory TTL in seconds (30 minutes default)
SESSION_TTL_SECONDS=1800

# Maximum messages before summarization triggers
MAX_MESSAGES_BEFORE_SUMMARY=20

# Token budget for working memory
WORKING_MEMORY_TOKEN_BUDGET=4000

# ─────────────────────────────────────────────────────────────────────────────
# RAG Configuration
# ─────────────────────────────────────────────────────────────────────────────
# Retrieval settings
RAG_TOP_K_RETRIEVAL=50
RAG_TOP_K_RERANK=5
RAG_SIMILARITY_THRESHOLD=0.7

# Chunking settings
CHUNK_SIZE=512
CHUNK_OVERLAP=100

# ─────────────────────────────────────────────────────────────────────────────
# Agent Configuration
# ─────────────────────────────────────────────────────────────────────────────
# Confidence threshold for escalation
CONFIDENCE_THRESHOLD=0.7

# Maximum retries for LLM calls
MAX_LLM_RETRIES=3

# Response timeout in seconds
RESPONSE_TIMEOUT_SECONDS=30

# ─────────────────────────────────────────────────────────────────────────────
# Business Configuration (Singapore SMB)
# ─────────────────────────────────────────────────────────────────────────────
BUSINESS_NAME="Your Business Name"
BUSINESS_TIMEZONE=Asia/Singapore
BUSINESS_HOURS_START=09:00
BUSINESS_HOURS_END=18:00
BUSINESS_WORKING_DAYS=Monday,Tuesday,Wednesday,Thursday,Friday

# ─────────────────────────────────────────────────────────────────────────────
# Logging Configuration
# ─────────────────────────────────────────────────────────────────────────────
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=logs/app.log

# ─────────────────────────────────────────────────────────────────────────────
# PDPA Compliance Settings
# ─────────────────────────────────────────────────────────────────────────────
# Data retention period in days
DATA_RETENTION_DAYS=30

# Enable anonymization for analytics
ENABLE_ANONYMIZATION=true
File: README.md
Markdown

# 🇸🇬 Singapore SMB Customer Support AI Agent

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18+-blue.svg)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready, context-aware customer enquiry support AI Agent designed specifically for Singapore Small and Medium Businesses (SMBs). Built with advanced RAG (Retrieval Augmented Generation), hierarchical memory, and PDPA-compliant data handling.

## ✨ Features

- **🧠 Advanced RAG Pipeline**: Multi-stage retrieval with query transformation, hybrid search, and cross-encoder reranking
- **💾 Hierarchical Memory**: Short-term (Redis) + Long-term (PostgreSQL) + Working memory management
- **🔒 PDPA Compliant**: Built-in consent tracking, data minimization, and auto-expiry
- **🌏 Singapore Context**: Timezone-aware, bilingual-ready (English/Mandarin)
- **⚡ Real-time Chat**: WebSocket-based streaming responses
- **📊 Evaluation Ready**: RAGAS metrics integration for continuous quality monitoring

## 🏗️ Architecture
┌─────────────────┐ ┌─────────────────────────────────────────────┐
│ React Chat │────▶│ FastAPI Backend │
│ Widget │◀────│ ┌─────────────────────────────────────┐ │
└─────────────────┘ │ │ Pydantic AI Agent │ │
│ │ ┌─────────┐ ┌─────────┐ ┌───────┐ │ │
│ │ │ RAG │ │ Memory │ │ Tools │ │ │
│ │ │Pipeline │ │ Manager │ │ │ │ │
│ │ └────┬────┘ └────┬────┘ └───────┘ │ │
│ └───────┼───────────┼──────────────────┘ │
│ │ │ │
│ ┌───────▼───┐ ┌─────▼─────┐ ┌───────────┐ │
│ │ Qdrant │ │ Redis │ │PostgreSQL │ │
│ │ (Vectors) │ │(Sessions) │ │ (Long) │ │
│ └───────────┘ └───────────┘ └───────────┘ │
└─────────────────────────────────────────────┘

text


## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API Key
- Cohere API Key (optional, for reranking)

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/singapore-smb-support-agent.git
cd singapore-smb-support-agent

# Copy environment configuration
cp .env.example .env

# Edit .env with your API keys
nano .env
2. Start Infrastructure
Bash

# Start all services with Docker Compose
docker-compose up -d

# Or use Make
make up
3. Start Development Servers
Bash

# Terminal 1: Backend
cd backend
pip install -e ".[dev]"
python -m app.main

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
4. Seed Knowledge Base
Bash

cd backend
python scripts/seed_knowledge.py
5. Access the Application
Frontend: http://localhost:3000
API Docs: http://localhost:8000/docs
Qdrant Dashboard: http://localhost:6333/dashboard
📁 Project Structure
text

singapore-smb-support-agent/
├── backend/                 # FastAPI + Pydantic AI backend
│   ├── app/
│   │   ├── agent/          # AI agent with tools
│   │   ├── api/            # REST & WebSocket endpoints
│   │   ├── ingestion/      # Document processing pipeline
│   │   ├── memory/         # Hierarchical memory system
│   │   ├── models/         # Pydantic & SQLAlchemy models
│   │   ├── rag/            # RAG pipeline components
│   │   └── services/       # Business logic services
│   ├── tests/              # Unit & integration tests
│   └── scripts/            # Utility scripts
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/     # UI components (Shadcn/UI)
│   │   ├── hooks/          # Custom React hooks
│   │   ├── stores/         # Zustand state management
│   │   └── lib/            # Utilities & API client
├── infrastructure/         # Docker & deployment configs
└── docs/                   # Documentation
🧪 Testing
Bash

# Run backend tests
cd backend
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run RAG evaluation
python scripts/evaluate_rag.py
📊 RAG Quality Metrics
Metric	Target	Current
Faithfulness	> 0.90	-
Answer Relevancy	> 0.85	-
Context Precision	> 0.80	-
Context Recall	> 0.85	-
🔐 PDPA Compliance
This system is designed with Singapore's Personal Data Protection Act in mind:

✅ Consent tracking for data collection
✅ Purpose limitation (support only)
✅ Configurable data retention (default: 30 days)
✅ Anonymization for analytics
✅ No cross-border data transfer (SG-hosted)
🤝 Contributing
Contributions are welcome! Please read our Contributing Guide for details.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Built with Pydantic AI
RAG powered by LangChain
Vector search by Qdrant
UI components from Shadcn/UI
text


---

### File: `Makefile`

```makefile
# ══════════════════════════════════════════════════════════════════════════════
# Singapore SMB Support Agent - Makefile
# ══════════════════════════════════════════════════════════════════════════════

.PHONY: help install up down restart logs shell test lint format seed evaluate clean

# Default target
.DEFAULT_GOAL := help

# Colors for terminal output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# ─────────────────────────────────────────────────────────────────────────────
# Help
# ─────────────────────────────────────────────────────────────────────────────
help: ## Show this help message
	@echo ""
	@echo "$(CYAN)Singapore SMB Support Agent$(NC)"
	@echo "$(CYAN)═══════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Usage:$(NC)"
	@echo "  make $(GREEN)<target>$(NC)"
	@echo ""
	@echo "$(YELLOW)Targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ─────────────────────────────────────────────────────────────────────────────
# Installation
# ─────────────────────────────────────────────────────────────────────────────
install: install-backend install-frontend ## Install all dependencies

install-backend: ## Install backend dependencies
	@echo "$(CYAN)Installing backend dependencies...$(NC)"
	cd backend && pip install -e ".[dev]"

install-frontend: ## Install frontend dependencies
	@echo "$(CYAN)Installing frontend dependencies...$(NC)"
	cd frontend && npm install

# ─────────────────────────────────────────────────────────────────────────────
# Docker Operations
# ─────────────────────────────────────────────────────────────────────────────
up: ## Start all Docker services
	@echo "$(CYAN)Starting Docker services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Services started!$(NC)"
	@echo "  - PostgreSQL: localhost:5432"
	@echo "  - Redis: localhost:6379"
	@echo "  - Qdrant: localhost:6333"

down: ## Stop all Docker services
	@echo "$(CYAN)Stopping Docker services...$(NC)"
	docker-compose down

restart: down up ## Restart all Docker services

logs: ## Show Docker service logs
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

# ─────────────────────────────────────────────────────────────────────────────
# Development Servers
# ─────────────────────────────────────────────────────────────────────────────
dev-backend: ## Start backend development server
	@echo "$(CYAN)Starting backend server...$(NC)"
	cd backend && python -m app.main

dev-frontend: ## Start frontend development server
	@echo "$(CYAN)Starting frontend server...$(NC)"
	cd frontend && npm run dev

dev: ## Start both backend and frontend (requires tmux or run separately)
	@echo "$(YELLOW)Please run 'make dev-backend' and 'make dev-frontend' in separate terminals$(NC)"

# ─────────────────────────────────────────────────────────────────────────────
# Database Operations
# ─────────────────────────────────────────────────────────────────────────────
db-migrate: ## Run database migrations
	@echo "$(CYAN)Running database migrations...$(NC)"
	cd backend && alembic upgrade head

db-rollback: ## Rollback last database migration
	@echo "$(CYAN)Rolling back last migration...$(NC)"
	cd backend && alembic downgrade -1

db-reset: ## Reset database (WARNING: destroys all data)
	@echo "$(RED)WARNING: This will destroy all data!$(NC)"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	cd backend && alembic downgrade base && alembic upgrade head

shell-db: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U support_agent -d support_agent

shell-redis: ## Open Redis CLI
	docker-compose exec redis redis-cli

# ─────────────────────────────────────────────────────────────────────────────
# Knowledge Base Operations
# ─────────────────────────────────────────────────────────────────────────────
seed: ## Seed the knowledge base with sample data
	@echo "$(CYAN)Seeding knowledge base...$(NC)"
	cd backend && python scripts/seed_knowledge.py

evaluate: ## Run RAG evaluation
	@echo "$(CYAN)Running RAG evaluation...$(NC)"
	cd backend && python scripts/evaluate_rag.py

# ─────────────────────────────────────────────────────────────────────────────
# Testing
# ─────────────────────────────────────────────────────────────────────────────
test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests
	@echo "$(CYAN)Running backend tests...$(NC)"
	cd backend && pytest -v

test-backend-cov: ## Run backend tests with coverage
	@echo "$(CYAN)Running backend tests with coverage...$(NC)"
	cd backend && pytest --cov=app --cov-report=html --cov-report=term-missing

test-frontend: ## Run frontend tests
	@echo "$(CYAN)Running frontend tests...$(NC)"
	cd frontend && npm test

# ─────────────────────────────────────────────────────────────────────────────
# Code Quality
# ─────────────────────────────────────────────────────────────────────────────
lint: lint-backend lint-frontend ## Lint all code

lint-backend: ## Lint backend code
	@echo "$(CYAN)Linting backend...$(NC)"
	cd backend && ruff check app tests
	cd backend && mypy app

lint-frontend: ## Lint frontend code
	@echo "$(CYAN)Linting frontend...$(NC)"
	cd frontend && npm run lint

format: format-backend format-frontend ## Format all code

format-backend: ## Format backend code
	@echo "$(CYAN)Formatting backend...$(NC)"
	cd backend && ruff format app tests

format-frontend: ## Format frontend code
	@echo "$(CYAN)Formatting frontend...$(NC)"
	cd frontend && npm run format

# ─────────────────────────────────────────────────────────────────────────────
# Cleanup
# ─────────────────────────────────────────────────────────────────────────────
clean: ## Clean up temporary files and caches
	@echo "$(CYAN)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-docker: ## Remove all Docker volumes (WARNING: destroys all data)
	@echo "$(RED)WARNING: This will destroy all Docker data!$(NC)"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	docker-compose down -v
	@echo "$(GREEN)Docker volumes removed!$(NC)"

# ─────────────────────────────────────────────────────────────────────────────
# Production
# ─────────────────────────────────────────────────────────────────────────────
build: ## Build production Docker images
	@echo "$(CYAN)Building production images...$(NC)"
	docker-compose -f docker-compose.prod.yml build

deploy: ## Deploy to production (placeholder)
	@echo "$(YELLOW)Production deployment not configured yet$(NC)"
	@echo "See docs/DEPLOYMENT.md for instructions"
File: docker-compose.yml
YAML

# ══════════════════════════════════════════════════════════════════════════════
# Singapore SMB Support Agent - Docker Compose (Development)
# ══════════════════════════════════════════════════════════════════════════════

version: "3.8"

services:
  # ─────────────────────────────────────────────────────────────────────────────
  # PostgreSQL - Long-term Memory Storage
  # ─────────────────────────────────────────────────────────────────────────────
  postgres:
    image: postgres:16-alpine
    container_name: smb_support_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-support_agent}
      POSTGRES_USER: ${POSTGRES_USER:-support_agent}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-devpassword123}
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./infrastructure/init-scripts/postgres:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-support_agent} -d ${POSTGRES_DB:-support_agent}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - smb_support_network

  # ─────────────────────────────────────────────────────────────────────────────
  # Redis - Short-term Memory & Session Storage
  # ─────────────────────────────────────────────────────────────────────────────
  redis:
    image: redis:7-alpine
    container_name: smb_support_redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - smb_support_network

  # ─────────────────────────────────────────────────────────────────────────────
  # Qdrant - Vector Database for RAG
  # ─────────────────────────────────────────────────────────────────────────────
  qdrant:
    image: qdrant/qdrant:v1.12.1
    container_name: smb_support_qdrant
    restart: unless-stopped
    ports:
      - "${QDRANT_PORT:-6333}:6333"
      - "6334:6334"  # gRPC port
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      QDRANT__SERVICE__GRPC_PORT: 6334
      QDRANT__LOG_LEVEL: INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - smb_support_network

  # ─────────────────────────────────────────────────────────────────────────────
  # Backend API (Optional - for full containerized development)
  # ─────────────────────────────────────────────────────────────────────────────
  # Uncomment to run backend in Docker instead of locally
  # backend:
  #   build:
  #     context: ./backend
  #     dockerfile: Dockerfile
  #   container_name: smb_support_backend
  #   restart: unless-stopped
  #   ports:
  #     - "${API_PORT:-8000}:8000"
  #   volumes:
  #     - ./backend:/app
  #   environment:
  #     - POSTGRES_HOST=postgres
  #     - REDIS_HOST=redis
  #     - QDRANT_HOST=qdrant
  #   depends_on:
  #     postgres:
  #       condition: service_healthy
  #     redis:
  #       condition: service_healthy
  #     qdrant:
  #       condition: service_healthy
  #   networks:
  #     - smb_support_network

# ─────────────────────────────────────────────────────────────────────────────
# Volumes
# ─────────────────────────────────────────────────────────────────────────────
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  qdrant_data:
    driver: local

# ─────────────────────────────────────────────────────────────────────────────
# Networks
# ─────────────────────────────────────────────────────────────────────────────
networks:
  smb_support_network:
    driver: bridge
Phase 1.2: Backend Foundation
File: backend/pyproject.toml
toml

# ══════════════════════════════════════════════════════════════════════════════
# Singapore SMB Support Agent - Backend Package Configuration
# ══════════════════════════════════════════════════════════════════════════════

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "smb-support-agent"
version = "0.1.0"
description = "Production-ready AI customer support agent for Singapore SMBs"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [
    { name = "SMB Support Team", email = "support@example.com" }
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Framework :: FastAPI",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

# ─────────────────────────────────────────────────────────────────────────────
# Core Dependencies
# ─────────────────────────────────────────────────────────────────────────────
dependencies = [
    # FastAPI & Web
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "python-multipart>=0.0.12",
    "websockets>=13.1",
    "httpx>=0.27.2",
    
    # Pydantic & Validation
    "pydantic>=2.9.0",
    "pydantic-settings>=2.6.0",
    "pydantic-ai>=0.0.24",
    
    # LangChain Ecosystem
    "langchain>=0.3.7",
    "langchain-core>=0.3.15",
    "langchain-openai>=0.2.6",
    "langchain-community>=0.3.5",
    "langchain-qdrant>=0.2.0",
    "langgraph>=0.2.45",
    
    # LLM Providers
    "openai>=1.55.0",
    "anthropic>=0.39.0",
    "cohere>=5.11.0",
    
    # Vector Database
    "qdrant-client>=1.12.0",
    
    # Embeddings (local option)
    "sentence-transformers>=3.3.0",
    
    # Database
    "sqlalchemy[asyncio]>=2.0.35",
    "asyncpg>=0.30.0",
    "alembic>=1.14.0",
    "greenlet>=3.1.1",
    
    # Redis
    "redis>=5.2.0",
    
    # Document Processing
    "unstructured>=0.16.5",
    "python-docx>=1.1.2",
    "pypdf>=5.1.0",
    "beautifulsoup4>=4.12.3",
    "lxml>=5.3.0",
    "markdown>=3.7",
    
    # Text Processing
    "tiktoken>=0.8.0",
    "nltk>=3.9.1",
    
    # Utilities
    "python-dateutil>=2.9.0",
    "pytz>=2024.2",
    "tenacity>=9.0.0",
    "structlog>=24.4.0",
    "python-dotenv>=1.0.1",
    "orjson>=3.10.11",
]

# ─────────────────────────────────────────────────────────────────────────────
# Development Dependencies
# ─────────────────────────────────────────────────────────────────────────────
[project.optional-dependencies]
dev = [
    # Testing
    "pytest>=8.3.3",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "pytest-mock>=3.14.0",
    "httpx>=0.27.2",
    "faker>=30.8.2",
    
    # RAG Evaluation
    "ragas>=0.2.6",
    "deepeval>=1.4.0",
    
    # Code Quality
    "ruff>=0.7.3",
    "mypy>=1.13.0",
    "pre-commit>=4.0.1",
    
    # Type Stubs
    "types-redis>=4.6.0",
    "types-python-dateutil>=2.9.0",
    
    # Documentation
    "mkdocs>=1.6.1",
    "mkdocs-material>=9.5.42",
]

# ─────────────────────────────────────────────────────────────────────────────
# Tool Configuration
# ─────────────────────────────────────────────────────────────────────────────
[tool.hatch.build.targets.wheel]
packages = ["app"]

[tool.ruff]
target-version = "py311"
line-length = 100
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "alembic",
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
    "B904",   # raise without from (sometimes intentional)
]

[tool.ruff.lint.isort]
known-first-party = ["app"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
filterwarnings = [
    "ignore::DeprecationWarning",
]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["app"]
branch = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
File: backend/app/__init__.py
Python

"""
Singapore SMB Customer Support AI Agent - Backend Application

A production-ready, context-aware customer enquiry support system
designed specifically for Singapore Small and Medium Businesses.

Features:
- Advanced RAG with multi-stage retrieval
- Hierarchical memory (short-term, long-term, working)
- PDPA-compliant data handling
- Real-time WebSocket chat interface
"""

__version__ = "0.1.0"
__author__ = "SMB Support Team"
File: backend/app/config.py
Python

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
File: backend/app/dependencies.py
Python

"""
Dependency Injection Module

Provides FastAPI dependencies for database connections,
services, and other shared resources.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, Request
from qdrant_client import AsyncQdrantClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings, get_settings


# ─────────────────────────────────────────────────────────────────────────────
# Database Engine & Session Factory
# ─────────────────────────────────────────────────────────────────────────────

def create_db_engine(settings: Settings):
    """Create async database engine with connection pooling."""
    return create_async_engine(
        settings.database_url,
        echo=settings.app_debug,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )


def create_session_factory(engine) -> async_sessionmaker[AsyncSession]:
    """Create async session factory."""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Global instances (initialized at startup)
# ─────────────────────────────────────────────────────────────────────────────

_engine = None
_session_factory = None
_redis_pool = None
_qdrant_client = None


async def init_dependencies(settings: Settings) -> None:
    """Initialize all dependencies at application startup."""
    global _engine, _session_factory, _redis_pool, _qdrant_client
    
    # PostgreSQL
    _engine = create_db_engine(settings)
    _session_factory = create_session_factory(_engine)
    
    # Redis
    _redis_pool = redis.ConnectionPool.from_url(
        settings.redis_url,
        decode_responses=True,
        max_connections=20,
    )
    
    # Qdrant
    _qdrant_client = AsyncQdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        api_key=settings.qdrant_api_key.get_secret_value() if settings.qdrant_api_key else None,
    )


async def close_dependencies() -> None:
    """Cleanup all dependencies at application shutdown."""
    global _engine, _redis_pool, _qdrant_client
    
    if _engine:
        await _engine.dispose()
    
    if _redis_pool:
        await _redis_pool.disconnect()
    
    if _qdrant_client:
        await _qdrant_client.close()


# ─────────────────────────────────────────────────────────────────────────────
# FastAPI Dependencies
# ─────────────────────────────────────────────────────────────────────────────

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session dependency.
    
    Yields:
        AsyncSession: Database session that is automatically closed after use.
    """
    if _session_factory is None:
        raise RuntimeError("Database not initialized. Call init_dependencies first.")
    
    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_redis_client() -> AsyncGenerator[redis.Redis, None]:
    """
    Get Redis client dependency.
    
    Yields:
        redis.Redis: Redis client that is automatically closed after use.
    """
    if _redis_pool is None:
        raise RuntimeError("Redis not initialized. Call init_dependencies first.")
    
    client = redis.Redis(connection_pool=_redis_pool)
    try:
        yield client
    finally:
        await client.close()


async def get_qdrant_client() -> AsyncQdrantClient:
    """
    Get Qdrant client dependency.
    
    Returns:
        AsyncQdrantClient: Shared Qdrant client instance.
    """
    if _qdrant_client is None:
        raise RuntimeError("Qdrant not initialized. Call init_dependencies first.")
    
    return _qdrant_client


# ─────────────────────────────────────────────────────────────────────────────
# Type Aliases for Dependency Injection
# ─────────────────────────────────────────────────────────────────────────────

SettingsDep = Annotated[Settings, Depends(get_settings)]
DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
RedisDep = Annotated[redis.Redis, Depends(get_redis_client)]
QdrantDep = Annotated[AsyncQdrantClient, Depends(get_qdrant_client)]


# ─────────────────────────────────────────────────────────────────────────────
# Lifespan Context Manager
# ─────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app):
    """
    Application lifespan manager.
    
    Handles startup and shutdown of all dependencies.
    """
    import structlog
    
    logger = structlog.get_logger()
    settings = get_settings()
    
    # Startup
    logger.info("Starting application", app_name=settings.app_name, env=settings.app_env)
    await init_dependencies(settings)
    logger.info("Dependencies initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await close_dependencies()
    logger.info("Dependencies closed successfully")
File: backend/app/logging_config.py
Python

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
File: backend/app/main.py
Python

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
File: backend/app/api/__init__.py
Python

"""
API Package

Contains all HTTP and WebSocket route handlers.
"""
File: backend/app/api/routes/__init__.py
Python

"""
Routes Package

Individual route modules for different API resources.
"""
File: backend/app/api/routes/health.py
Python

"""
Health Check Routes

Provides endpoints for monitoring application health and readiness.
"""

from datetime import datetime, timezone
from typing import Any

import structlog
from fastapi import APIRouter, status
from pydantic import BaseModel, Field
from qdrant_client import AsyncQdrantClient

from app.config import get_settings
from app.dependencies import get_db_session, get_qdrant_client, get_redis_client

router = APIRouter()
logger = structlog.get_logger()


class HealthStatus(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Overall health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Environment name")
    checks: dict[str, Any] = Field(default_factory=dict, description="Individual component checks")


class ComponentHealth(BaseModel):
    """Individual component health status."""
    
    status: str
    latency_ms: float | None = None
    error: str | None = None


@router.get(
    "/health",
    response_model=HealthStatus,
    summary="Health Check",
    description="Basic health check endpoint for load balancers and monitoring.",
)
async def health_check() -> HealthStatus:
    """
    Basic health check endpoint.
    
    Returns a simple health status without checking dependencies.
    Suitable for load balancer health probes.
    """
    settings = get_settings()
    
    return HealthStatus(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        version="0.1.0",
        environment=settings.app_env,
        checks={},
    )


@router.get(
    "/health/ready",
    response_model=HealthStatus,
    summary="Readiness Check",
    description="Comprehensive readiness check including all dependencies.",
    responses={
        503: {"description": "Service not ready"},
    },
)
async def readiness_check() -> HealthStatus:
    """
    Comprehensive readiness check.
    
    Checks all critical dependencies:
    - PostgreSQL database
    - Redis cache
    - Qdrant vector database
    
    Returns 503 if any dependency is unhealthy.
    """
    import time
    
    settings = get_settings()
    checks: dict[str, Any] = {}
    all_healthy = True
    
    # Check PostgreSQL
    try:
        start = time.perf_counter()
        async for session in get_db_session():
            await session.execute("SELECT 1")
        latency = (time.perf_counter() - start) * 1000
        checks["postgresql"] = ComponentHealth(status="healthy", latency_ms=round(latency, 2))
    except Exception as e:
        logger.error("PostgreSQL health check failed", error=str(e))
        checks["postgresql"] = ComponentHealth(status="unhealthy", error=str(e))
        all_healthy = False
    
    # Check Redis
    try:
        start = time.perf_counter()
        async for client in get_redis_client():
            await client.ping()
        latency = (time.perf_counter() - start) * 1000
        checks["redis"] = ComponentHealth(status="healthy", latency_ms=round(latency, 2))
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))
        checks["redis"] = ComponentHealth(status="unhealthy", error=str(e))
        all_healthy = False
    
    # Check Qdrant
    try:
        start = time.perf_counter()
        qdrant = await get_qdrant_client()
        await qdrant.get_collections()
        latency = (time.perf_counter() - start) * 1000
        checks["qdrant"] = ComponentHealth(status="healthy", latency_ms=round(latency, 2))
    except Exception as e:
        logger.error("Qdrant health check failed", error=str(e))
        checks["qdrant"] = ComponentHealth(status="unhealthy", error=str(e))
        all_healthy = False
    
    status_value = "healthy" if all_healthy else "unhealthy"
    
    health_status = HealthStatus(
        status=status_value,
        timestamp=datetime.now(timezone.utc),
        version="0.1.0",
        environment=settings.app_env,
        checks={k: v.model_dump() for k, v in checks.items()},
    )
    
    if not all_healthy:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_status.model_dump(),
        )
    
    return health_status


@router.get(
    "/health/live",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Liveness Check",
    description="Simple liveness probe for Kubernetes.",
)
async def liveness_check() -> None:
    """
    Simple liveness check.
    
    Returns 204 No Content if the application is running.
    Used by Kubernetes liveness probes.
    """
    pass
File: backend/app/api/routes/chat.py
Python

"""
Chat Routes

Handles customer chat interactions with the AI agent.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

import structlog
from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel, Field

from app.dependencies import DbSessionDep, QdrantDep, RedisDep, SettingsDep

router = APIRouter()
logger = structlog.get_logger()


# ─────────────────────────────────────────────────────────────────────────────
# Request/Response Models
# ─────────────────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    """Individual chat message."""
    
    id: UUID = Field(default_factory=uuid4, description="Message unique identifier")
    role: str = Field(..., pattern="^(user|assistant|system)$", description="Message sender role")
    content: str = Field(..., min_length=1, max_length=10000, description="Message content")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional message metadata")


class ChatRequest(BaseModel):
    """Chat request from client."""
    
    session_id: UUID | None = Field(default=None, description="Existing session ID or None for new")
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    customer_id: str | None = Field(default=None, description="Optional customer identifier")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Request metadata")


class SourceCitation(BaseModel):
    """Source citation for response grounding."""
    
    source: str = Field(..., description="Source document name")
    chunk_id: str = Field(..., description="Chunk identifier")
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance score")
    text_preview: str = Field(..., description="Preview of cited text")


class SuggestedAction(BaseModel):
    """Suggested follow-up action."""
    
    type: str = Field(..., description="Action type")
    label: str = Field(..., description="Display label")
    payload: dict[str, Any] = Field(default_factory=dict, description="Action payload")


class ChatResponse(BaseModel):
    """Chat response from agent."""
    
    session_id: UUID = Field(..., description="Session identifier")
    message_id: UUID = Field(default_factory=uuid4, description="Response message ID")
    content: str = Field(..., description="Response content")
    confidence: float = Field(..., ge=0, le=1, description="Response confidence score")
    sources: list[SourceCitation] = Field(default_factory=list, description="Source citations")
    suggested_actions: list[SuggestedAction] = Field(default_factory=list)
    requires_followup: bool = Field(default=False, description="Whether human follow-up needed")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class ConversationHistory(BaseModel):
    """Conversation history response."""
    
    session_id: UUID
    messages: list[ChatMessage]
    created_at: datetime
    last_activity: datetime
    message_count: int


# ─────────────────────────────────────────────────────────────────────────────
# REST Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send Chat Message",
    description="Send a message to the AI support agent and receive a response.",
    responses={
        200: {"description": "Successful response from agent"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
    },
)
async def send_message(
    request: ChatRequest,
    settings: SettingsDep,
    db: DbSessionDep,
    redis: RedisDep,
    qdrant: QdrantDep,
) -> ChatResponse:
    """
    Process a chat message through the AI agent.
    
    This endpoint:
    1. Creates or retrieves a session
    2. Loads conversation history from memory
    3. Processes the message through the RAG pipeline
    4. Generates a response using the AI agent
    5. Stores the conversation in memory
    
    Args:
        request: Chat request containing the user message.
        settings: Application settings.
        db: Database session.
        redis: Redis client for short-term memory.
        qdrant: Qdrant client for vector search.
    
    Returns:
        ChatResponse: AI agent response with sources and metadata.
    """
    import time
    
    start_time = time.perf_counter()
    
    # Generate or use provided session ID
    session_id = request.session_id or uuid4()
    
    logger.info(
        "Processing chat message",
        session_id=str(session_id),
        message_length=len(request.message),
        has_customer_id=request.customer_id is not None,
    )
    
    # TODO: Implement full agent processing in Phase 5
    # For now, return a placeholder response
    
    processing_time = (time.perf_counter() - start_time) * 1000
    
    # Placeholder response (will be replaced with actual agent logic)
    return ChatResponse(
        session_id=session_id,
        content=(
            f"Thank you for your message. I'm {settings.business_name}'s AI assistant. "
            "This is a placeholder response - the full agent implementation is coming in Phase 5. "
            f"You said: '{request.message[:100]}...'" if len(request.message) > 100 
            else f"You said: '{request.message}'"
        ),
        confidence=0.95,
        sources=[],
        suggested_actions=[
            SuggestedAction(
                type="quick_reply",
                label="Tell me more about your services",
                payload={"message": "Tell me more about your services"},
            ),
            SuggestedAction(
                type="quick_reply",
                label="What are your business hours?",
                payload={"message": "What are your business hours?"},
            ),
        ],
        requires_followup=False,
        processing_time_ms=round(processing_time, 2),
    )


@router.get(
    "/chat/history/{session_id}",
    response_model=ConversationHistory,
    summary="Get Conversation History",
    description="Retrieve the conversation history for a session.",
    responses={
        200: {"description": "Conversation history"},
        404: {"description": "Session not found"},
    },
)
async def get_conversation_history(
    session_id: UUID,
    redis: RedisDep,
    limit: int = Query(default=50, ge=1, le=100, description="Maximum messages to return"),
) -> ConversationHistory:
    """
    Retrieve conversation history for a session.
    
    Args:
        session_id: Session identifier.
        redis: Redis client.
        limit: Maximum number of messages to return.
    
    Returns:
        ConversationHistory: Session conversation history.
    """
    # TODO: Implement in Phase 4 with memory system
    
    logger.info("Retrieving conversation history", session_id=str(session_id))
    
    # Placeholder - will be replaced with actual memory retrieval
    return ConversationHistory(
        session_id=session_id,
        messages=[],
        created_at=datetime.now(timezone.utc),
        last_activity=datetime.now(timezone.utc),
        message_count=0,
    )


# ─────────────────────────────────────────────────────────────────────────────
# WebSocket Endpoint
# ─────────────────────────────────────────────────────────────────────────────

class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str) -> None:
        """Accept and register a new connection."""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info("WebSocket connected", session_id=session_id)
    
    def disconnect(self, session_id: str) -> None:
        """Remove a connection."""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info("WebSocket disconnected", session_id=session_id)
    
    async def send_message(self, session_id: str, message: dict[str, Any]) -> None:
        """Send a message to a specific connection."""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/chat/{session_id}")
async def websocket_chat(
    websocket: WebSocket,
    session_id: str,
) -> None:
    """
    WebSocket endpoint for real-time chat.
    
    Enables streaming responses and real-time updates.
    
    Protocol:
    - Client sends: {"type": "message", "content": "..."}
    - Server sends: {"type": "chunk", "content": "..."} for streaming
    - Server sends: {"type": "complete", "response": {...}} when done
    - Server sends: {"type": "error", "error": "..."} on error
    """
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            logger.info(
                "WebSocket message received",
                session_id=session_id,
                message_type=data.get("type"),
            )
            
            if data.get("type") == "message":
                content = data.get("content", "")
                
                # TODO: Implement streaming response in Phase 5
                # For now, send a simple response
                
                await manager.send_message(session_id, {
                    "type": "chunk",
                    "content": "Thank you for your message. ",
                })
                
                await manager.send_message(session_id, {
                    "type": "chunk",
                    "content": "I'm processing your request...",
                })
                
                await manager.send_message(session_id, {
                    "type": "complete",
                    "response": {
                        "content": f"This is a placeholder response to: {content}",
                        "confidence": 0.95,
                        "sources": [],
                    },
                })
            
            elif data.get("type") == "ping":
                await manager.send_message(session_id, {"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        logger.error("WebSocket error", session_id=session_id, error=str(e))
        await manager.send_message(session_id, {
            "type": "error",
            "error": "An error occurred processing your request.",
        })
        manager.disconnect(session_id)
File: backend/app/api/routes/knowledge.py
Python

"""
Knowledge Base Routes

Handles knowledge base management including document upload,
search, and administration.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

import structlog
from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from pydantic import BaseModel, Field

from app.dependencies import QdrantDep, SettingsDep

router = APIRouter()
logger = structlog.get_logger()


# ─────────────────────────────────────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────────────────────────────────────

class KnowledgeDocument(BaseModel):
    """Knowledge base document."""
    
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    source: str = Field(..., description="Document source (faq, product, policy, etc.)")
    category: str = Field(..., description="Document category")
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DocumentUploadResponse(BaseModel):
    """Response after document upload."""
    
    document_id: UUID
    title: str
    chunks_created: int
    status: str
    message: str


class SearchQuery(BaseModel):
    """Search query for knowledge base."""
    
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)
    filter_source: str | None = None
    filter_category: str | None = None
    min_score: float = Field(default=0.5, ge=0, le=1)


class SearchResult(BaseModel):
    """Individual search result."""
    
    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: dict[str, Any]


class SearchResponse(BaseModel):
    """Search response."""
    
    query: str
    results: list[SearchResult]
    total_results: int
    search_time_ms: float


class CollectionStats(BaseModel):
    """Knowledge base collection statistics."""
    
    collection_name: str
    total_documents: int
    total_chunks: int
    sources: dict[str, int]
    categories: dict[str, int]
    last_updated: datetime | None


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "/knowledge/documents",
    response_model=DocumentUploadResponse,
    summary="Upload Document",
    description="Upload a document to the knowledge base.",
    responses={
        200: {"description": "Document uploaded successfully"},
        400: {"description": "Invalid document format"},
        413: {"description": "Document too large"},
    },
)
async def upload_document(
    file: UploadFile = File(...),
    source: str = Query(..., description="Document source type"),
    category: str = Query(..., description="Document category"),
    settings: SettingsDep = None,
    qdrant: QdrantDep = None,
) -> DocumentUploadResponse:
    """
    Upload a document to the knowledge base.
    
    Supported formats:
    - PDF
    - Markdown (.md)
    - Plain text (.txt)
    - HTML
    
    The document will be:
    1. Parsed and cleaned
    2. Chunked into semantic segments
    3. Embedded using the configured model
    4. Stored in the vector database
    
    Args:
        file: Document file to upload.
        source: Source type (faq, product, policy, website).
        category: Document category for filtering.
    
    Returns:
        DocumentUploadResponse: Upload result with document ID.
    """
    logger.info(
        "Document upload requested",
        filename=file.filename,
        content_type=file.content_type,
        source=source,
        category=category,
    )
    
    # Validate file type
    allowed_types = {
        "application/pdf",
        "text/plain",
        "text/markdown",
        "text/html",
        "application/json",
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Allowed: {allowed_types}",
        )
    
    # TODO: Implement full ingestion pipeline in Phase 2
    # For now, return a placeholder response
    
    document_id = uuid4()
    
    return DocumentUploadResponse(
        document_id=document_id,
        title=file.filename or "Untitled",
        chunks_created=0,  # Will be populated after actual processing
        status="queued",
        message="Document queued for processing. Full implementation in Phase 2.",
    )


@router.post(
    "/knowledge/search",
    response_model=SearchResponse,
    summary="Search Knowledge Base",
    description="Search the knowledge base using semantic search.",
)
async def search_knowledge(
    query: SearchQuery,
    qdrant: QdrantDep = None,
    settings: SettingsDep = None,
) -> SearchResponse:
    """
    Search the knowledge base.
    
    Uses hybrid search combining:
    - Semantic similarity (dense vectors)
    - Keyword matching (sparse vectors)
    
    Results are reranked for optimal relevance.
    
    Args:
        query: Search query with filters.
    
    Returns:
        SearchResponse: Search results with relevance scores.
    """
    import time
    
    start_time = time.perf_counter()
    
    logger.info(
        "Knowledge search requested",
        query=query.query[:100],
        top_k=query.top_k,
        filter_source=query.filter_source,
    )
    
    # TODO: Implement full search pipeline in Phase 3
    # For now, return placeholder response
    
    search_time = (time.perf_counter() - start_time) * 1000
    
    return SearchResponse(
        query=query.query,
        results=[],  # Will be populated by actual search
        total_results=0,
        search_time_ms=round(search_time, 2),
    )


@router.get(
    "/knowledge/stats",
    response_model=CollectionStats,
    summary="Get Collection Statistics",
    description="Get statistics about the knowledge base.",
)
async def get_collection_stats(
    qdrant: QdrantDep = None,
    settings: SettingsDep = None,
) -> CollectionStats:
    """
    Get knowledge base statistics.
    
    Returns counts of documents, chunks, and breakdowns by source/category.
    
    Returns:
        CollectionStats: Collection statistics.
    """
    logger.info("Collection stats requested")
    
    # TODO: Implement actual stats retrieval
    # For now, return placeholder
    
    return CollectionStats(
        collection_name=settings.qdrant_collection_name if settings else "knowledge_base",
        total_documents=0,
        total_chunks=0,
        sources={},
        categories={},
        last_updated=None,
    )


@router.delete(
    "/knowledge/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Document",
    description="Delete a document from the knowledge base.",
)
async def delete_document(
    document_id: UUID,
    qdrant: QdrantDep = None,
) -> None:
    """
    Delete a document and all its chunks from the knowledge base.
    
    Args:
        document_id: Document UUID to delete.
    """
    logger.info("Document deletion requested", document_id=str(document_id))
    
    # TODO: Implement deletion in Phase 2
    pass
File: backend/app/models/__init__.py
Python

"""
Models Package

Contains Pydantic schemas, domain models, and SQLAlchemy ORM models.
"""
File: backend/app/models/schemas.py
Python

"""
Pydantic Schemas

API request/response schemas and validation models.
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────────────────────

class MessageRole(str, Enum):
    """Chat message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class DocumentSource(str, Enum):
    """Knowledge base document sources."""
    FAQ = "faq"
    PRODUCT = "product"
    POLICY = "policy"
    WEBSITE = "website"
    TICKET = "ticket"


class ConsentStatus(str, Enum):
    """PDPA consent status."""
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    WITHDRAWN = "withdrawn"


class EscalationReason(str, Enum):
    """Reasons for escalating to human support."""
    LOW_CONFIDENCE = "low_confidence"
    NEGATIVE_SENTIMENT = "negative_sentiment"
    EXPLICIT_REQUEST = "explicit_request"
    SENSITIVE_TOPIC = "sensitive_topic"
    REPEATED_FAILURE = "repeated_failure"


# ─────────────────────────────────────────────────────────────────────────────
# Base Schemas
# ─────────────────────────────────────────────────────────────────────────────

class TimestampMixin(BaseModel):
    """Mixin for created/updated timestamps."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UUIDMixin(BaseModel):
    """Mixin for UUID primary key."""
    id: UUID = Field(default_factory=uuid4)


# ─────────────────────────────────────────────────────────────────────────────
# Customer Schemas
# ─────────────────────────────────────────────────────────────────────────────

class CustomerBase(BaseModel):
    """Base customer schema."""
    email: str | None = None
    name: str | None = None
    phone: str | None = None
    company: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class CustomerCreate(CustomerBase):
    """Schema for creating a customer."""
    external_id: str | None = Field(None, description="External system customer ID")
    consent_status: ConsentStatus = ConsentStatus.PENDING


class CustomerRead(CustomerBase, UUIDMixin, TimestampMixin):
    """Schema for reading customer data."""
    external_id: str | None = None
    consent_status: ConsentStatus
    total_conversations: int = 0
    last_interaction: datetime | None = None


# ─────────────────────────────────────────────────────────────────────────────
# Conversation Schemas
# ─────────────────────────────────────────────────────────────────────────────

class ConversationSummary(BaseModel):
    """Summarized conversation for long-term storage."""
    session_id: UUID
    customer_id: UUID | None = None
    summary: str
    key_topics: list[str] = Field(default_factory=list)
    sentiment: str | None = None
    resolution_status: str | None = None
    message_count: int = 0


# ─────────────────────────────────────────────────────────────────────────────
# Agent Schemas
# ─────────────────────────────────────────────────────────────────────────────

class AgentContext(BaseModel):
    """Context provided to the agent for processing."""
    session_id: UUID
    customer_id: UUID | None = None
    customer_info: CustomerRead | None = None
    conversation_history: list[dict[str, Any]] = Field(default_factory=list)
    conversation_summary: str | None = None
    retrieved_context: list[dict[str, Any]] = Field(default_factory=list)
    business_context: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    """Structured response from the agent."""
    content: str
    confidence: float = Field(ge=0, le=1)
    sources: list[dict[str, Any]] = Field(default_factory=list)
    suggested_actions: list[dict[str, Any]] = Field(default_factory=list)
    escalate: bool = False
    escalation_reason: EscalationReason | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


# ─────────────────────────────────────────────────────────────────────────────
# Feedback Schemas
# ─────────────────────────────────────────────────────────────────────────────

class FeedbackCreate(BaseModel):
    """Schema for creating feedback on a response."""
    session_id: UUID
    message_id: UUID
    rating: int = Field(ge=1, le=5, description="Rating from 1-5")
    feedback_type: str = Field(..., pattern="^(helpful|not_helpful|incorrect|other)$")
    comment: str | None = Field(None, 
Som
