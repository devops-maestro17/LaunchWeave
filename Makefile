# Makefile for LaunchWeave API

# Variables
PYTHON = .\.venv\Scripts\python.exe
DOCKER_IMAGE_NAME = launchweave-api

.PHONY: test build clean run test-neon

# Default target
all: test build

# Run automated tests (Local)
test:
	@echo "Running tests against local database..."
	$(PYTHON) -m pytest

# Run automated tests against Neon DB
# Usage: make test-neon TEST_DATABASE_URL="postgresql+psycopg2://..."
test-neon:
	@echo "Running tests against Neon database..."
	$(PYTHON) -m pytest

# Build the Docker image
build:
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run the application locally (using uvicorn)
run:
	@echo "Starting application..."
	$(PYTHON) -m uvicorn app.main:app --reload

# Clean up temporary files
clean:
	@echo "Cleaning up..."
	if exist __pycache__ rd /s /q __pycache__
	if exist .pytest_cache rd /s /q .pytest_cache
	if exist .venv\.venv rd /s /q .venv\.venv
