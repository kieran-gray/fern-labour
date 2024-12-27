# Makefile variables
SRC_DIR := app
TEST_DIR := tests
PWD = $(shell pwd)
PYPROJECT_TOML := $(shell grep 'PYPROJECT_TOML' config.toml | sed 's/.*= *//')

DEV_IMAGE := $(DOCKER_IMAGE_BACKEND)-dev:latest
DEV_COMMAND_CONTAINER := docker run --rm $(DEV_IMAGE) sh -c


build-dev:
	docker build --target dev -t $(DOCKER_IMAGE_BACKEND)-dev .

build-prod:
	docker build --target production -t $(DOCKER_IMAGE_BACKEND) .

build-keycloak:
	docker build -t $(DOCKER_IMAGE_BACKEND)-keycloak ./keycloak -f ./keycloak/Dockerfile --no-cache

build: build-dev build-prod build-keycloak

run-static:
	docker compose --profile auth --profile events up

run-backend:
	docker compose --profile backend --profile consumer up

stop:
	docker compose down

# Source code formatting, linting and testing
.PHONY: format \
		lint \
		test \
		coverage \
		check

lint:
	mypy $(SRC_DIR) & \
	ruff check $(SRC_DIR) & \
	ruff format $(SRC_DIR) --check & \
	bandit -r $(SRC_DIR) -c $(PYPROJECT_TOML)

format:
	ruff check $(SRC_DIR) $(TEST_DIR) --fix
	ruff format $(SRC_DIR) $(TEST_DIR)
	isort $(SRC_DIR) $(TEST_DIR)

test:
	$(DEV_COMMAND_CONTAINER) 'pytest tests -v'

test.debug:
	docker container run -p 5678:5678 --rm $(DEV_IMAGE) sh -c '\
		debugpy --listen 0.0.0.0:5678 --wait-for-client -m pytest tests -v'

coverage:
	$(DEV_COMMAND_CONTAINER) 'coverage run -m pytest & coverage report'

coverage.html:
	$(DEV_COMMAND_CONTAINER) 'coverage run -m pytest & coverage html'

check: lint test

# Dishka
.PHONY: plot-data

plot-data:
	python scripts/dishka/plot_dependencies_data.py
