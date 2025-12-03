SHELL = /bin/bash

SRC_DIR=src
TEST_DIR=tests
PYPROJECT_TOML=pyproject.toml

revision:
	POSTGRES_DB=app POSTGRES_HOST=0.0.0.0 POSTGRES_PORT=5432 \
	POSTGRES_USER=postgres POSTGRES_PASSWORD=changeme PYTHONPATH=. \
	uv run alembic revision --autogenerate

add:
	uv add $(dep)

remove:
	uv remove $(dep)

deps:
	uv sync --all-groups --frozen

update:
	uv lock --upgrade

# Source code formatting and linting
.PHONY: format \
		lint 

format:
	uv run ruff format $(SRC_DIR) $(TEST_DIR)
	uv run ruff check $(SRC_DIR) $(TEST_DIR) --fix

lint:
	uv lock --check
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
	uv run debugpy --listen 0.0.0.0:5678 --wait-for-client -m pytest $(TEST_DIR) -v

check: lint test

# Dishka

plot:
	PYTHONPATH="." uv run python scripts/plot_dependencies.py

tree:
	PYTHONPATH="." uv run python scripts/print_tree.py

# clean

pycache-del:
	./scripts/pycache_del.sh
