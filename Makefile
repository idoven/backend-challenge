DOCKER_COMPOSE := $(shell which docker-compose)
DOCKER := $(shell which docker)

# Start container
up:
	$(DOCKER_COMPOSE) up

# Start container (detached mode)
upd:
	$(DOCKER_COMPOSE) up -d

# Down container
down:
	$(DOCKER_COMPOSE) down

# Stop container
stop:
	$(DOCKER_COMPOSE) stop

# Build container
build:
	$(DOCKER_COMPOSE) build

# Delete container
rm:
	$(DOCKER_COMPOSE) rm

# Pull docker image
pull:
	$(DOCKER_COMPOSE) pull

# Run flake8 linting
lint:
	$(DOCKER_COMPOSE) run --rm app sh -c "flake8"

# Access to container´s shell
bash:
	$(DOCKER) exec -it app sh

# Run unit tests
test:
	$(DOCKER_COMPOSE) run --rm app sh -c "python manage.py test"

# Create test superuser (only for testing)
superuser:
	$(DOCKER_COMPOSE) run --rm app python manage.py shell -c "from django.contrib.auth import get_user_model; user = get_user_model().objects.create_superuser('admin@idoven.com', 'supersegura')"

# Create test user (only for testing)
user:
	$(DOCKER_COMPOSE) run --rm app python manage.py shell -c "from django.contrib.auth import get_user_model; user = get_user_model().objects.create_user('user@idoven.com', 'supersegura')"