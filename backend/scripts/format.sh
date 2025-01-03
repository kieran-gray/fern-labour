#!/bin/bash

SRC_DIR="../app"
TEST_DIR="../tests"

uv run ruff check ${SRC_DIR} ${TEST_DIR} --fix
uv run ruff format ${SRC_DIR} ${TEST_DIR}