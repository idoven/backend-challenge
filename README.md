# Idoven ECG API
- [Idoven ECG API](#idoven-ecg-api)
  - [Structure](#structure)
  - [Assumptions](#assumptions)
  - [Design decisions](#design-decisions)
  - [API](#api)
  - [Prerequisites](#prerequisites)
  - [Commands](#commands)
    - [test](#test)
    - [build](#build)
    - [run](#run)
    - [run-new](#run-new)
    - [clean](#clean)

## Structure
The project is structured as follows:
```
.
├── ecg # Main application package
│   ├── api # API-related components
│   │   ├── dependencies # API dependency implementations (e.g., database, authentication)
│   │   └── routers # API route handlers
│   ├── cli # Command-line interface (CLI) tools and scripts
│   ├── domains # Business logic and domain models
│   │   ├── admin # Admin-related domain components (models, services, exceptions)
│   │   └── ecg # ECG-related domain components (models, services, exceptions)
│   └── sql # SQL queries, schema, and migration scripts
└── tests # Test suite for the application
├── api # Tests for API components
│   ├── dependencies # Tests for API dependency implementations
│   └── routers # Tests for API route handlers
└── domains # Tests for business logic and domain models
├── admin # Tests for admin-related domain components
└── ecg # Tests for ECG-related domain components
```

## Assumptions
- For the ECG sample I've assumed that the values can be zero

## Design decisions
- I've decided to use FastAPI as the framework for the API because it's a modern framework that is easy to use and has a lot of features out of the box.
- I've not used an ORM because I don't think it's necessary for this project. I've used the `asyncpg` library for the database connection and raw sql queries.
- I've implemented the authentication using OAuth2 with JWT tokens.
- I've separated the business logic from the API. The business logic is in the `domains` package. The API is in the `api` package.
- I've created a small `cli` package for the CLI tools and scripts.

## API
The api documentation can be found in `http://localhost:8000/docs` after running the application.

The app comes preloaded with a user with the following credentials:
- email: `test@test.com`
- password: `test`

and the following admin credentials:
- email: `admin@test.com`
- password: `admin`

also there is a preloaded ecg with the following id:
`testid`

The endpoints are:
### API/V1
- `POST /api/v1/ecg/` - Upload an ECG
- `GET /api/v1/ecg/{id}` - Get an ECG output
### ADMIN
- `POST /admin/user/` - Create a new user
- `DELETE /admin/user/{email}` - Delete a user
### AUTH
- `POST /auth/token` - Get a new access token


## Prerequisites
- [Docker](https://docs.docker.com/engine/install/) Install for building and running the Docker containers
- [Docker compose](https://docs.docker.com/compose/install/) Install for orchestrating the Docker containers
- [Make](https://www.gnu.org/software/make/) Install for running common tasks

Optionally if you want to run the project locally:
- Python 3.10
- [Poetry](https://python-poetry.org/) for managing dependencies


## Commands
You have to have all the prerequisites installed to run the commands.

### test
Run tests for the project.

```bash
make test
```

This command builds the Docker environment, runs the tests using pytest, and then brings the environment down.

### build
Build the Docker image for the project.

```bash
make build
```

This command builds the Docker image using the docker-compose configuration.

### run
Run the application in Docker.

```bash
make run
```

This command starts the Docker environment using the docker-compose configuration.

### run-new
Build and run the application in a new Docker environment.

```bash
make run-new
```

This command brings down the current Docker environment, builds a new Docker image, and starts the new environment using the docker-compose configuration.

### clean
Clean up generated files.

```bash
make clean
```

This command removes generated files, such as *.pyc, __pycache__, .pytest_cache, .mypy_cache, .coverage, and .ruff_cache.
