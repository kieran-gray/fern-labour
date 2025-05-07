TOKEN_CMD = gcloud auth application-default print-access-token
CRED_FILE = $(CURDIR)/.artifact-registry-token
SHELL = /bin/bash

define generate_token
$(shell $(TOKEN_CMD) > $(CRED_FILE) 2>/dev/null; cat $(CRED_FILE))
endef

ifneq ("$(wildcard $(CRED_FILE))","")
	# File exists. Check if empty or expired.
	CRED_FILE_CONTENTS = $(shell cat $(CRED_FILE))
	CRED_FILE_ISEMPTY = $(shell [[ -z "$(CRED_FILE_CONTENTS)" ]] && echo 1 || echo 0)

	ifeq ("$(CRED_FILE_ISEMPTY)", "1")
		# Token file exists, but is empty
		TOKEN = $(call generate_token)
	else

		# File exists, check the expiry time of the token file.
		CRED_FILE_TIME_STR = $(shell stat -c "%Y" $(CRED_FILE) 2>/dev/null)
		# Use Linux 'date -d "1 hour ago"' for expiry time (seconds since epoch)
		CRED_EXPIRY_STR = $(shell date -d '1 hour ago' "+%s" 2>/dev/null)

		ifeq ($(CRED_FILE_TIME_STR),)
			TOKEN = $(call generate_token)
		else ifeq ($(CRED_EXPIRY_STR),)
			TOKEN = $(call generate_token)
		else
			# Both times retrieved, perform comparison
			CRED_IS_EXPIRED = $(shell [ "$(CRED_FILE_TIME_STR)" -lt "$(CRED_EXPIRY_STR)" ] && echo 1 || echo 0)

			ifeq ("$(CRED_IS_EXPIRED)","1")
				# Token expired. Generate.
				TOKEN = $(call generate_token)
			else
				# Token is valid. Use cached token from contents read earlier.
				TOKEN = $(CRED_FILE_CONTENTS)
			endif
		endif
	endif
else
	# Token file does not exist yet.
	TOKEN = $(call generate_token)
endif

ensure-token:
	@echo "Token check/generation occurred during Makefile parsing."
	@if [ -z "$(TOKEN)" ]; then \
		echo "ERROR: TOKEN variable is empty after parsing logic!" >&2; \
		exit 1; \
	else \
		echo "TOKEN variable appears to be set."; \
	fi

SRC_DIR=src
TEST_DIR=tests
PYPROJECT_TOML=pyproject.toml

revision:
	POSTGRES_DB=app POSTGRES_HOST=0.0.0.0 POSTGRES_PORT=5432 \
	POSTGRES_USER=postgres POSTGRES_PASSWORD=changeme PYTHONPATH=. \
	uv run alembic revision --autogenerate

add: ensure-token
	UV_INDEX_FERN_LABOUR_PACKAGES_USERNAME=oauth2accesstoken \
	UV_INDEX_FERN_LABOUR_PACKAGES_PASSWORD=${TOKEN} \
	uv add $(dep)

remove: ensure-token
	UV_INDEX_FERN_LABOUR_PACKAGES_USERNAME=oauth2accesstoken \
	UV_INDEX_FERN_LABOUR_PACKAGES_PASSWORD=${TOKEN} \
	uv remove $(dep)

deps: ensure-token
	UV_INDEX_FERN_LABOUR_PACKAGES_USERNAME=oauth2accesstoken \
	UV_INDEX_FERN_LABOUR_PACKAGES_PASSWORD=${TOKEN} \
	uv sync --all-groups --frozen

update: ensure-token
	UV_INDEX_FERN_LABOUR_PACKAGES_USERNAME=oauth2accesstoken \
	UV_INDEX_FERN_LABOUR_PACKAGES_PASSWORD=${TOKEN} \
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
