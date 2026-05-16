# SC Chatbot Makefile
# Development, build, test, and deployment targets

.PHONY: help dev build test docker-up docker-down clean install-lint

# Default target
help:
	@echo "SC Chatbot - Makefile Targets"
	@echo ""
	@echo "Development:"
	@echo "  dev         - Start backend development server"
	@echo "  start       - Start all services with docker-compose"
	@echo ""
	@echo "Build:"
	@echo "  build       - Build Docker images"
	@echo "  docker-up   - Start Docker containers"
	@echo "  docker-down - Stop Docker containers"
	@echo "  clean       - Remove Docker containers and volumes"
	@echo ""
	@echo "Testing:"
	@echo "  test        - Run unit tests"
	@echo "  test-cover  - Run tests with coverage report"
	@echo ""
	@echo "Maintenance:"
	@echo "  install     - Install Python dependencies"
	@echo "  lint        - Run linting checks"
	@echo "  fmt         - Format code"
	@echo ""
	@echo "Documentation:"
	@echo "  docs        - Open documentation"
	@echo ""
	@echo "Frontend:"
	@echo "  frontend    - Start frontend development server"
	@echo "  frontend:build - Build frontend for production"
	@echo ""


# ================================
# DEVELOPMENT
# ================================

install:
	@echo "=== Installing Python dependencies ==="
	pip install -r requirements.txt
	@echo "=== Done ==="

dev:
	@echo "=== Starting backend development server ==="
	@echo "   Visit http://localhost:8000/docs for API docs"
	@echo "   Press Ctrl+C to stop the server"
	bash -c ". /home/dihieu/.miniconda3/bin/activate base && cd src/backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
	@echo "=== Done ==="

frontend:
	@echo "=== Starting frontend development server ==="
	cd src/frontend && npm run dev
	@echo "=== Done ==="

# Start all services with docker-compose
start:
	@echo "=== Starting all services with docker-compose ==="
	docker-compose up -d
	@echo "=== Services started ==="
	@echo "   Backend:   http://localhost:8000"
	@echo "   Frontend:  http://localhost:3000"
	@echo "   API Docs:  http://localhost:8000/docs"

# ================================
# BUILD
# ================================

build:
	@echo "=== Building Docker images ==="
	docker-compose build
	@echo "=== Build complete ==="

docker-up:
	@echo "=== Starting Docker containers ==="
	docker-compose up -d
	@echo "=== Containers started ==="
	@echo "   Backend:   http://localhost:8000"
	@echo "   Frontend:  http://localhost:3000"

docker-down:
	@echo "=== Stopping Docker containers ==="
	docker-compose down
	@echo "=== Containers stopped ==="

clean:
	@echo "=== Cleaning up Docker containers and volumes ==="
	docker-compose down -v
	rm -rf data/faiss
	@echo "=== Cleanup complete ==="

# ================================
# TESTING
# ================================

test:
	@echo "=== Running unit tests ==="
	pytest test/ -v
	@echo "=== Tests complete ==="

test-cover:
	@echo "=== Running tests with coverage ==="
	pytest test/ --cov=src/backend --cov-report=html
	@echo "=== Coverage report: htmlcov/index.html ==="

# ================================
# LINTING & FORMATTING
# ================================

lint:
	@echo "=== Running linting checks ==="
	flake8 src/backend/ --max-line-length=120
	isort --check-only src/backend/
	@echo "=== Linting complete ==="

fmt:
	@echo "=== Formatting code ==="
	isort src/backend/
	black src/backend/
	@echo "=== Formatting complete ==="

# ================================
# DOCUMENTATION
# ================================

docs:
	@echo "=== Opening documentation ==="
	open docs/table-of-contents.html
	@echo "=== Done ==="

# ================================
# ZALO OAUTH (for POC)
# ================================

zalo-login:
	@echo "=== Zalo OAuth Login ==="
	@echo "1. Visit: https://www.zalo.me/devapps/portal/app"
	@echo "2. Register your Zalo Official Account"
	@echo "3. Create webhook in Zalo OA console"
	@echo "4. Add ZALO_APP_ID, ZALO_APP_SECRET, ZALO_WEBHOOK_URL to .env"

# ================================
# HELPERS
# ================================

db-init:
	@echo "=== Initializing database ==="
	cd src/backend && python -c "from models.database import init_db; import asyncio; asyncio.run(init_db())"
	@echo "=== Database initialized ==="

db-migrate:
	@echo "=== Running database migrations ==="
	alembic upgrade head
	@echo "=== Migrations complete ==="