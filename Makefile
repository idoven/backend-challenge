.PHONY: test build run run_new clean


# Run tests
test:
	docker-compose up -d --build
	docker-compose exec app poetry run pytest -s tests/ ; docker-compose down

# Build Docker image
build:
	docker-compose build

run:
	docker-compose up

# Run new docker environment
run-new:
	docker-compose down
	docker-compose up --build


# Clean up generated files
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf .ruff_cache
