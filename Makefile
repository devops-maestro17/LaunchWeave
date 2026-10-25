# Makefile for LaunchWeave API

PYTHON = .\.venv\Scripts\python.exe
DOCKER_IMAGE_NAME = launchweave-api

.PHONY: test build clean run test-neon dev-up dev-down lint format help

# Default target
all: test build

help:
	@echo "Available commands:"
	@echo "  make run        - Run FastAPI app locally with Uvicorn (reload enabled)"
	@echo "  make test       - Run unit/integration tests with pytest"
	@echo "  make test-neon  - Run verification script against running server or Neon"
	@echo "  make build      - Build local Docker image"
	@echo "  make dev-up     - Start local PostgreSQL & API via docker-compose"
	@echo "  make dev-down   - Stop docker-compose services"
	@echo "  make clean      - Clean up temporary python/test cache files"

# Run automated tests (Local)
test:
	@echo "Running tests against local test database..."
	$(PYTHON) -m pytest -v

# Run verification script against running server
test-neon:
	@echo "Running verification checks against LaunchWeave..."
	$(PYTHON) scripts/test_neon.py

# Build the Docker image
build:
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run the application locally (using uvicorn)
run:
	@echo "Starting application locally..."
	$(PYTHON) -m uvicorn app.main:app --reload --port 8000

# Docker Compose helpers
dev-up:
	docker compose up -d

dev-down:
	docker compose down -v

# Clean up temporary files
clean:
	@echo "Cleaning up..."
	if exist __pycache__ rd /s /q __pycache__
	if exist .pytest_cache rd /s /q .pytest_cache
	if exist app\__pycache__ rd /s /q app\__pycache__
	if exist tests\__pycache__ rd /s /q tests\__pycache__
