FROM python:3.12-slim AS base
ARG UID=1001
ARG GID=1001

# Create a non-root user and group with fixed IDs
RUN groupadd --gid $GID nonroot && \
    useradd --uid $UID --gid $GID --shell /bin/bash --create-home nonroot

WORKDIR /app

# Creating a separate directory for venvs allows to easily
# copy them from the builder and to mount the application
# for local development
RUN mkdir /venv && chown nonroot:nonroot /app /venv

# Add venv to PATH here, so it's available in all subsequent stages
ENV PATH="/venv/bin:$PATH"

# Install necessary runtime libraries
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked  \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends curl

# ---- Stage 1: Base Builder ----
# Installs build tools and uv. Used as a base for specific dependency builders.
FROM base AS base_builder
ENV UV_PROJECT_ENVIRONMENT=/venv

# Install build-time system dependencies (needed for compiling some Python packages)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /bin/uv

# Set uv environment variables
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copy project definition files needed by all builders
COPY --chown=nonroot:nonroot pyproject.toml uv.lock config.toml ./

# Switch to non-root user for dependency installation from now on
USER nonroot

# ---- Stage 2a: HTTP Builder ----
# Installs core + http dependencies
FROM base_builder AS http_builder
RUN --mount=type=cache,target=/home/nonroot/.cache/uv,sharing=locked,uid=$UID,gid=$GID \
    uv sync --frozen --no-dev --group app --group http --no-install-project

# ---- Stage 2b: Migrations Builder ----
# Installs core + migrations dependencies
FROM base_builder AS migrations_builder
RUN --mount=type=cache,target=/home/nonroot/.cache/uv,sharing=locked,uid=$UID,gid=$GID \
    uv sync --frozen --no-dev --group migrations --no-install-project

# ---- Stage 3a: Production - HTTP ----
# Final minimal production image for the HTTP server
FROM base AS http

ARG UVICORN_PORT=8001

# Copy the virtual environment with core + http dependencies
COPY --from=http_builder --chown=nonroot:nonroot /venv /venv

# Copy the application code
COPY --chown=nonroot:nonroot app app
COPY --chown=nonroot:nonroot pyproject.toml config.toml ./

USER nonroot
EXPOSE ${UVICORN_PORT}

# Run the HTTP application
CMD [ "python", "-m", "app.run" ]

# ---- Stage 3b: Production - Migrations ----
# Final minimal production image for running migrations
FROM base AS migrations

# Copy the virtual environment with core + migrations dependencies
COPY --from=migrations_builder --chown=nonroot:nonroot /venv /venv

# Copy the application code (including alembic.ini, migration scripts)
COPY --chown=nonroot:nonroot app app
COPY --chown=nonroot:nonroot alembic.ini ./

USER nonroot

# Run Alembic migrations
# Assumes alembic.ini is in the root project directory
CMD ["alembic", "upgrade", "head"]

# ---- Stage 4: Development ----
# Development image with ALL dependencies and potentially dev tools/settings
FROM base_builder AS development

# Install ALL dependencies (core + http + consumer + migrations + dev)
RUN --mount=type=cache,target=/home/nonroot/.cache/uv,sharing=locked,uid=$UID,gid=$GID \
    uv sync --frozen --all-groups

# Copy application code
COPY --chown=nonroot:nonroot . .

USER nonroot
