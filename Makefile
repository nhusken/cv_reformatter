.PHONY: help install clean test lint docker-build docker-up docker-down docker-logs venv dev docker-start docker-stop docker-status

# Python version and virtual environment
PYTHON = python
VENV = .venv
BIN = $(VENV)/bin/

# Default target
help:
	@echo "Available commands:"
	@echo "  make venv        - Create virtual environment"
	@echo "  make install     - Install dependencies in development mode"
	@echo "  make clean       - Remove Python file artifacts"
	@echo "  make test        - Run tests with pytest"
	@echo "  make lint        - Run code linting (black, flake8, isort)"
	@echo "  make format      - Format code with black and isort"
	@echo "  make coverage    - Run tests with coverage report"
	@echo ""
	@echo "Docker commands:"
	@echo "  make docker-build  - Build Docker container"
	@echo "  make docker-start  - Start container in background"
	@echo "  make docker-stop   - Stop container"
	@echo "  make docker-logs   - View container logs"
	@echo "  make docker-status - Show container status"

# Virtual environment
venv:
	$(PYTHON) -m venv $(VENV)
	$(BIN)pip install --upgrade pip
	$(BIN)pip install hatch

# Development setup
install: venv
	$(BIN)pip install -e ".[dev]"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

test:
	$(BIN)pytest

coverage:
	$(BIN)pytest --cov=backend --cov-report=term-missing

lint:
	$(BIN)black --check backend/
	$(BIN)flake8 backend/
	$(BIN)isort --check-only backend/

format:
	$(BIN)black backend/
	$(BIN)isort backend/

# Docker commands
docker-build:
	docker compose build

docker-start:
	docker compose up -d

docker-stop:
	docker compose down

docker-logs:
	docker compose logs -f

docker-status:
	docker ps

# Development server (local)
dev:
	$(BIN)flask run --host=0.0.0.0 --port=5000
