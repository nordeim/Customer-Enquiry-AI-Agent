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
