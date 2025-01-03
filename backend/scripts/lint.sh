#!/bin/bash

PYPROJECT_TOML="backend/pyproject.toml"
SRC_DIR="backend/app"
TEST_DIR="backend/tests"

uv run mypy ${SRC_DIR}
uv run ruff check ${SRC_DIR}
uv run ruff format ${SRC_DIR} --check
uv run bandit -r ${SRC_DIR} -c ${PYPROJECT_TOML}