SRC_DIR=app
TEST_DIR=tests
PYPROJECT_TOML=pyproject.toml

# Source code formatting and linting
.PHONY: format \
		lint 

format:
	uv run ruff format $(SRC_DIR) $(TEST_DIR)
	uv run ruff check $(SRC_DIR) $(TEST_DIR) --fix

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
	uv run debugpy --listen 0.0.0.0:5678 --wait-for-client -m pytest $(TEST_DIR) -v

check: lint test

pycache-del:
	./scripts/pycache_del.sh
