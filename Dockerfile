# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Install system dependencies required for Poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Set the working directory to /app
WORKDIR /app

# Copy the poetry files to the working directory
COPY pyproject.toml poetry.lock README.md ./

# Copy the rest of the application code to the working directory
COPY ecg/ ecg/

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi


## Expose the port your application will run on
EXPOSE 8000

## Run the application using uvicorn
CMD ["uvicorn", "ecg.main:app", "--host", "0.0.0.0", "--port", "8000"]
