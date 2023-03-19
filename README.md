

## TODO
### Phase 1
- [X] Editorconfig
- [X] gitignore
- [X] Pre-commit
  - [X] MyPy
  - [X] Ruff (Black style)
- [X] Basic Test Structure
- [X] Basic App Structure
  - [X] Views
  - [X] Swagger Docs
  - [X] Logging
- [X] Basic Configuration
- [X] Basic CI
  - [X] Workflow for testing
- [X] Add Database

## Phase 2
- [ ] App creation
  - [ ] Models
  - [ ] Views

## Phase 3
- [ ] Write docs
- [ ] Manual testing
- [ ] Review

# Idoven ECG API

TODO: Fill me

## Prerequisites

- Python 3.10
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management and packaging
- Docker for building and running the Docker container

## Getting Started

### Install dependencies

To install the project's dependencies, run:

```bash
make install
```

## Run tests
To run tests for your project, execute:

```bash
make test
```

## Lint the code
To check your code for linting issues, run:
```bash
make lint
```

## Format the code
To automatically format your code according to the project's style guide, use:
```bash
make format
```

## Build Docker image
To build the Docker image for your project, run:
```bash
make build
```

## Run Docker container
To run your project in a Docker container, execute:
```
make run
```
This command maps port 8000 on your host machine to port 8000 in the Docker container.

## Clean up generated files
To remove any generated files, such as .pyc files and __pycache__ directories, run:
```bash
make clean
```
