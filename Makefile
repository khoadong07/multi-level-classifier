.PHONY: help install run docker-build docker-up docker-down test check-config clear-cache clean

help:
	@echo "SPX Classification System - Makefile Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install       - Install dependencies"
	@echo "  make run          - Run the application"
	@echo "  make test         - Run tests"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo ""
	@echo "Utilities:"
	@echo "  make check-config - Check system configuration"
	@echo "  make clear-cache  - Clear classification cache"
	@echo "  make clean        - Clean temporary files"

install:
	pip install -r requirements.txt

run:
	streamlit run run.py

docker-build:
	docker-compose build

docker-up:
	docker-compose up

docker-down:
	docker-compose down

test:
	python scripts/test_system.py

check-config:
	python scripts/check_config.py

clear-cache:
	python scripts/clear_cache.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
