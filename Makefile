.PHONY: install test lint format build run clean

# Install dependencies
install:
	poetry install

# Run tests
test:
	poetry run pytest tests/

# Lint the code
lint:
	poetry run ruff ecg/ tests/

# Format the code
format:
	poetry run black ecg/ tests/

# Build Docker image
build:
	docker build -t ecg .

# Run Docker container
run:
	docker run --rm -it -p 8000:8000 ecg

# Clean up generated files
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
