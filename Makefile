.PHONY: help install dev test clean docker-build docker-run

help: ## Show help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

dev: ## Run in development mode
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	pytest -v

test-cov: ## Run tests with coverage
	pytest --cov=app --cov-report=html --cov-report=term

clean: ## Clean temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Docker commands - SQLite (current configuration)
docker-build: ## Build Docker image
	docker compose build

docker-run: ## Run with Docker Compose (SQLite)
	docker compose up -d

docker-stop: ## Stop Docker containers
	docker compose down

docker-logs: ## View Docker logs
	docker compose logs -f

docker-restart: ## Restart Docker services
	docker compose restart

docker-rebuild: ## Rebuild and restart Docker services
	docker compose down
	docker compose build --no-cache
	docker compose up -d

# Docker commands - PostgreSQL (full configuration)
docker-full-build: ## Build with PostgreSQL and Redis
	docker compose -f docker-compose.full.yml build

docker-full-run: ## Run full configuration (PostgreSQL + Redis + Adminer)
	docker compose -f docker-compose.full.yml up -d

docker-full-stop: ## Stop full configuration
	docker compose -f docker-compose.full.yml down

docker-full-logs: ## View logs for full configuration
	docker compose -f docker-compose.full.yml logs -f

# Application commands
create-admin: ## Create admin user
	docker compose exec user-api python scripts/create_admin.py

check-db: ## Check database status
	docker compose exec user-api python scripts/check_db.py

format: ## Format code with black
	black app/ tests/ main.py

lint: ## Check code with flake8
	flake8 app/ tests/ main.py

# SQLite specific commands
sqlite-shell: ## Open SQLite shell
	docker compose exec user-api sqlite3 users.db

sqlite-backup: ## Create SQLite backup
	docker compose exec user-api cp users.db users_backup_$(shell date +%Y%m%d_%H%M%S).db

sqlite-restore: ## Restore SQLite backup (specify BACKUP_FILE)
	docker compose exec user-api cp $(BACKUP_FILE) users.db

# Database migration commands
migrate-to-postgres: ## Migrate from SQLite to PostgreSQL
	@echo "To migrate to PostgreSQL:"
	@echo "1. Change DATABASE_URL in .env"
	@echo "2. Run: docker compose -f docker-compose.full.yml up -d"
	@echo "3. Migrate data with custom script"

migrate-to-sqlite: ## Migrate from PostgreSQL to SQLite
	@echo "To migrate to SQLite:"
	@echo "1. Change DATABASE_URL in .env"
	@echo "2. Run: docker compose up -d"
	@echo "3. Migrate data with custom script"

# Development helpers
shell: ## Access container shell
	docker compose exec user-api bash

python-shell: ## Access Python shell in container
	docker compose exec user-api python

# Production commands
prod-build: ## Build production image
	docker build -t user-management-api:latest .

prod-run: ## Run in production mode
	docker run -d -p 8000:8000 --env-file .env.production user-management-api:latest

# Health checks
health: ## Check application health
	curl -s http://localhost:8000/api/v1/health | jq . || curl -s http://localhost:8000/api/v1/health

debug: ## Check debug information
	curl -s http://localhost:8000/debug | jq . || curl -s http://localhost:8000/debug

# Quick test
quick-test: ## Quick API test
	@echo "🚀 Quick API test..."
	@echo "Health check:"
	@curl -s http://localhost:8000/api/v1/health | jq . || echo "Health check failed"
	@echo "\nRoot endpoint:"
	@curl -s http://localhost:8000/ | jq . || echo "Root endpoint failed"
