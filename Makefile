# Makefile for LaunchWeave API

# Variables
PYTHON = .venv/bin/python
DOCKER_IMAGE_NAME = launchweave-api

.PHONY: test build clean run

# Default target
all: test build

# Run automated tests
test:
	@echo "Running tests..."
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
