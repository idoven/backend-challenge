# ECG Monitoring Microservice

The ECG Monitoring Microservice is designed to handle electrocardiograms (ECG) and provide various insights about them.
It offers endpoints for performing CRUD operations on ECG records, as well as calculating the number of zero crossings
of the ECG signal. Additionally, the microservice includes user login and registration endpoints.

## Usage

To run the microservice, use the following Docker Compose command:

```bash
docker-compose up ecg --build
```

## Access

- The service will be accessible at *http://ecg.localhost:8000/swagger/* 
- To access the admin panel, visit *http://ecg.localhost:8000/admin/* 

## Authentication

To interact with the microservice endpoints, a user token is required.
After a user logs in, the token is generated and should be included in the request header as follows:

**Authorization: Token {*generated_token*}**

## User Access

Users can only access ECG data they have created.
Admin users, registered in the admin panel,
have the authority to register new users but cannot create new ECG data.
Other than admin registration, users can also be registerd with **registration** endpoint

## Running Tests

To run tests and generate coverage reports, use the following command:

```bash
docker-compose run --no-deps ecg bash -c "coverage run manage.py test connector; coverage report -m; coverage html; coverage xml"
```

## Pre-commit Checks

Ensure code quality and formatting by running pre-commit checks:

```bash
pre-commit run --all-files
```

## Environment Configuration

### Setting up Environment Variables

For local development, setting up environment variables is necessary. Copy the provided `.env.ecg.sample` file to
create your own `.env.ecg` file. Update the values according to your configuration.

#### Step 1: Copy the Sample Environment File

Copy the contents of `.env.ecg.sample`:

```bash
cp .env.ecg.sample .env.ecg
```

#### Step 2: Update Environment Variables

Open the newly created .env.ecg file and update the values based on your specific configuration.
This file contains essential settings for the database, Django, and other environment-specific variables.

## Files

- **docker-compose.yml**: Docker Compose configuration file.
- **Dockerfile**: Docker configuration file for building the microservice image.
- **config/requirements.txt**: List of Python dependencies.
- **pre-commit.yml**: Configuration file for pre-commit hooks.
- **pyproject.toml**: TOML configuration file for the project.
- **.env.ecg.sample**: sample for environment variables