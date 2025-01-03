# Makefile variables
DOCKER_IMAGE_BACKEND=labour-tracker-backend
DOCKER_IMAGE_FRONTEND=labour-tracker-frontend
DEV_IMAGE := $(DOCKER_IMAGE_BACKEND)-dev:latest
DEV_COMMAND_CONTAINER := docker run --rm $(DEV_IMAGE) sh -c

# Project building
.PHONY: build-dev \
		build-prod \
		build-keycloak \
		build-frontend \
		build \
		clean

build-dev:
	docker build --target dev -t $(DOCKER_IMAGE_BACKEND)-dev ./backend

build-prod:
	docker build --target production -t $(DOCKER_IMAGE_BACKEND) ./backend

build-keycloak:
	docker build -t $(DOCKER_IMAGE_BACKEND)-keycloak ./keycloak -f ./keycloak/Dockerfile --no-cache

build-frontend:
	docker build -t $(DOCKER_IMAGE_FRONTEND) ./frontend -f ./frontend/Dockerfile

build: build-dev build-prod build-keycloak build-frontend

clean: 
	docker system prune -a && docker volume prune -a

# Project running
.PHONY: run-deps \
		run-backend \
		run-frontend \
		run-app \
		stop

run-deps:
	docker compose --profile auth --profile events up

run-backend:
	docker compose --profile backend --profile consumer up

run-frontend:
	docker compose --profile frontend up --build

run-app:
	docker compose --profile backend --profile consumer --profile frontend up

stop:
	docker compose down

# Source code formatting and linting
.PHONY: format \
		lint 

format:
	$(DEV_COMMAND_CONTAINER) 'ls -l && ./scripts/format.sh'

lint:
	$(DEV_COMMAND_CONTAINER) './scripts/lint.sh'

# Testing
.PHONY: test \
		test-debug \
		check

test:
	uv run pytest --cov

# Use 'Attach Local' VSCode launch profile
test-debug:
	uv run debugpy --listen 0.0.0.0:5678 --wait-for-client -m pytest $(TEST_DIR) -v

check: lint test
