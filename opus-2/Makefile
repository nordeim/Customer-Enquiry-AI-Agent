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
