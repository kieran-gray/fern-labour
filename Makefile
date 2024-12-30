# Makefile variables
SRC_DIR := app
TEST_DIR := tests
PYPROJECT_TOML := $(shell grep 'PYPROJECT_TOML' config.toml | sed 's/.*= *//')

# Project building
.PHONY: build-dev \
		build-prod \
		build-keycloak \
		build-frontend \
		build \
		clean

build-dev:
	docker build --target dev -t $(DOCKER_IMAGE_BACKEND)-dev .

build-prod:
	docker build --target production -t $(DOCKER_IMAGE_BACKEND) .

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
		stop

run-deps:
	docker compose --profile auth --profile events up

run-backend:
	docker compose --profile backend --profile consumer up

run-frontend:
	docker compose --profile frontend up --build

stop:
	docker compose down

# Source code formatting and linting
.PHONY: format \
		lint \
		test \
		test-debug \
		check

format:
	uv run ruff check $(SRC_DIR) $(TEST_DIR) --fix
	uv run ruff format $(SRC_DIR) $(TEST_DIR)

lint:
	uv run mypy $(SRC_DIR)
	uv run ruff check $(SRC_DIR)
	uv run ruff format $(SRC_DIR) --check
	uv run bandit -r $(SRC_DIR) -c $(PYPROJECT_TOML)

# Testing
.PHONY: test \
		test-debug \
		check

test:
	uv run pytest --cov

# Use 'Attach Local' VSCode launch profile
test-debug:
	uv run debugpy --listen 0.0.0.0:5678 --wait-for-client -m pytest tests -v

check: lint test
