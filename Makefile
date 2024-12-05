# Makefile variables
SRC_DIR := app
PWD = $(shell pwd)
PYPROJECT_TOML := $(shell grep 'PYPROJECT_TOML' config.toml | sed 's/.*= *//')

DEV_IMAGE := backend-dev:latest
DEV_COMMAND_CONTAINER := docker run --rm $(DEV_IMAGE) sh -c

install:
	docker compose build

run:
	docker compose up

stop:
	docker compose down

# Source code formatting, linting and testing
.PHONY: format \
		lint \
		test \
		coverage \
		check

lint:
	$(DEV_COMMAND_CONTAINER) '\
		mypy $(SRC_DIR) & \
		ruff check $(SRC_DIR) & \
		ruff format $(SRC_DIR) --check & \
		bandit -r $(SRC_DIR) -c $(PYPROJECT_TOML)'

format:
	ruff check $(SRC_DIR) --fix
	ruff format $(SRC_DIR)
	isort $(SRC_DIR)

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
