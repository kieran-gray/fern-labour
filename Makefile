include .env

TOKEN_CMD = gcloud auth application-default print-access-token
CRED_FILE = $(CURDIR)/.artifact-registry-token
SHELL = /bin/zsh

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

run: ensure-token
	@echo "Starting all services..."
	docker compose up --build -d
	@echo "Services started."

stop:
	@echo "Stopping services..."
	docker compose down
	@echo "Services stopped."

ensure-token:
	@echo "Token check/generation occurred during Makefile parsing."
	@if [ -z "$(TOKEN)" ]; then \
		echo "ERROR: TOKEN variable is empty after parsing logic!" >&2; \
		exit 1; \
	else \
		echo "TOKEN variable appears to be set."; \
	fi
