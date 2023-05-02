FROM python:3.9-alpine3.13
LABEL maintainer="safuente"

# Don´t buffer the output, you can see directly the output
ENV PYTHONUNBUFFERED 1

# Copy requirements file
COPY ./requirements.txt /tmp/requirements.txt

COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Create virtual env avoid dependencies conflicts inside the image
# Upgrade pip in virtual env
# Install requirements in virtual env
# Remove tmp once the requirements are installed
# Install dev requirements if it is required
# Create a not root user with no password and no home dir
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Add virtual env to PATH
ENV PATH="/py/bin:$PATH"

# Define the user to switch and is going to execute the app
USER django-user