.PHONY: help install install-dev lint format test clean run

help:
	@echo "TrainWreck - Makefile commands"
	@echo ""
	@echo "  make install       Install runtime dependencies"
	@echo "  make install-dev   Install runtime + dev dependencies"
	@echo "  make lint          Run linters (ruff, mypy)"
	@echo "  make format        Format code (black, isort)"
	@echo "  make test          Run tests with pytest"
	@echo "  make clean         Remove cache and build artifacts"
	@echo "  make run           Run the TrainWreck CLI"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

lint:
	ruff check src/
	mypy src/

format:
	black src/
	isort src/

test:
	pytest tests/ -v --cov=src/trainwreck --cov-report=term-missing

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov/

run:
	python -m trainwreck --help
