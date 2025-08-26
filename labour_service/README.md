# Labour Service

## Overview

The Labour Service is the core backend service for the labour tracking application. It manages all labour-related activities including labour sessions, contractions, subscriptions, and user management. This service handles the primary business logic for tracking pregnancy labour progress and coordinating with other services via event-driven messaging.

**Key Responsibilities:**
- Labour session management (start, stop, updates)
- Contraction tracking and timing
- Subscription management for birth partners
- User authentication and authorization
- Payment processing integration (Stripe)
- Event publishing for cross-service communication

## Architecture & Dependencies

**Framework & Technologies:**
- **FastAPI** - High-performance async web framework
- **SQLAlchemy 2.0** - Database ORM with async support
- **Dishka** - Dependency injection container
- **Alembic** - Database migration management
- **Pydantic** - Data validation and serialization
- **PostgreSQL** - Primary database
- **Keycloak** - Authentication and authorization
- **Google Cloud PubSub** - Event messaging (emulated locally)
- **Stripe** - Payment processing
- **uvloop** - High-performance event loop

**Architecture Pattern:**
- **Domain-Driven Design (DDD)** with Clean Architecture
- **Event-Driven Architecture** for service communication
- **CQRS patterns** with separate command/query handlers

**Directory Structure:**
```
src/
├── labour/          # Labour domain (sessions, contractions)
├── subscription/    # Subscription management domain  
├── user/           # User management and authentication
├── payments/       # Stripe payment integration
├── core/           # Shared domain infrastructure
├── api/            # FastAPI routes and schemas
└── setup/          # Application configuration and DI
```

## Setup Instructions

### Prerequisites

1. **Python 3.12+**
2. **UV package manager**
3. **PostgreSQL** (handled via Docker Compose)
4. **Google Cloud SDK** (for authentication to private package registry)

### Authentication Setup

```bash
# Required for accessing private package registry
gcloud auth login
gcloud init  
gcloud auth application-default login
```

### Installation

1. **Install Dependencies:**
   ```bash
   make deps
   ```

2. **Environment Configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration values
   ```

3. **Database Setup:**
   ```bash
   # Generate new migration (if schema changes made)
   make revision
   
   # Database migrations run automatically on service startup
   ```

### Running Locally

**Via Docker Compose (Recommended):**
```bash
# From project root
make run
```

**Direct Development:**
```bash
# Install dependencies
make deps

# Run with hot reload
python -m src.run
```

The service will be available at `http://localhost:8000`

## Deployment

### Docker Build
The service uses multi-stage Docker builds:
- `migrations` stage - Runs Alembic database migrations
- `http` stage - Production HTTP server

### Environment-Specific Configuration
Configuration is managed through:
- `config.toml` - Default configuration values
- `.env` files - Environment-specific overrides
- Environment variables - Runtime overrides

### Health Checks
The service exposes health check endpoints:
- `GET /api/v1/health` - Service health status

## Testing

### Running Tests
```bash
# Run full test suite with coverage
make test

# Run tests with debugging support
make test-debug

# Run all quality checks (lint + test)
make check
```

### Test Structure
- **Location:** `tests/unit/`
- **Framework:** pytest with async support
- **Coverage:** 100% required (enforced)
- **Mocking:** Uses pytest fixtures and dependency injection overrides

### Code Quality
```bash
# Format code
make format

# Run linting, type checking, and security scans
make lint
```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment | `local`, `staging`, `production` |
| `POSTGRES_*` | Database connection settings | See `.env.example` |
| `KEYCLOAK_*` | Authentication service config | See `.env.example` |
| `SUBSCRIBER_TOKEN_SALT` | Token generation salt | Random string |
| `DATABASE_ENCRYPTION_KEY` | Database field encryption | Secure random key |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `UVICORN_PORT` | HTTP server port | `8000` |
| `STRIPE_API_KEY` | Payment processing | Required for payments |
| `GCP_PROJECT_ID` | PubSub project ID | `test` (for emulator) |

See `.env.example` for complete configuration reference.

## API Documentation

### Core Endpoints

**Authentication:**
- `POST /api/v1/auth/token` - Get access token
- `POST /api/v1/auth/refresh` - Refresh token

**Labour Management:**
- `GET /api/v1/labour` - List user's labour sessions
- `POST /api/v1/labour` - Create new labour session
- `PUT /api/v1/labour/{id}` - Update labour session
- `POST /api/v1/labour/{id}/complete` - Complete labour session

**Contractions:**
- `GET /api/v1/labour/{id}/contractions` - Get contractions
- `POST /api/v1/labour/{id}/contractions` - Record contraction

**Subscriptions:**
- `GET /api/v1/subscriptions` - List subscriptions
- `POST /api/v1/subscriptions/{id}/invite` - Invite subscriber
- `PUT /api/v1/subscriptions/{id}/subscribers/{subscriber_id}` - Manage subscribers

**Payments:**
- `POST /api/v1/payments/create-checkout-session` - Create Stripe checkout
- `POST /api/v1/payments/webhook` - Handle payment webhooks

### OpenAPI Documentation
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

## Contributing Notes

### Code Standards
- **100% test coverage** required for all new code
- **Type hints** mandatory for all functions
- **Async/await** patterns for all I/O operations
- **Domain-driven design** principles for business logic

### Development Workflow
1. Create feature branch from `main`
2. Implement changes following DDD patterns
3. Add comprehensive unit tests
4. Run `make check` to validate code quality
5. Submit pull request with descriptive commits

### Database Changes
1. Modify SQLAlchemy models in appropriate domain
2. Generate migration: `make revision`
3. Test migration in development environment
4. Include migration in pull request

### Event Integration
- Publish domain events for cross-service communication
- Use type-safe event schemas from shared packages
- Handle event failures gracefully with retries
- Test event handlers in isolation

### Performance Considerations
- Use SQLAlchemy async patterns for database operations
- Implement proper database connection pooling
- Consider caching strategies for frequently accessed data
- Monitor and optimize query performance