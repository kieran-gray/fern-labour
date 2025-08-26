# Contact Service

## Overview

The Contact Service handles "Contact Us" form submissions and messaging functionality for the labour tracking application. It processes contact messages from users and sends alerts to the development team via Slack notifications. This service provides a secure, spam-protected interface for customer support and feedback collection.

**Key Responsibilities:**
- Process contact form submissions from marketing/frontend applications
- Store contact messages with proper data validation
- Send Slack alerts for new contact messages
- Cloudflare Turnstile verification for spam protection
- Event-driven notifications via PubSub messaging

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
- **Slack SDK** - Team alert notifications
- **Cloudflare Turnstile** - Spam protection verification
- **uvloop** - High-performance event loop

**Architecture Pattern:**
- **Domain-Driven Design (DDD)** with Clean Architecture
- **Event-Driven Architecture** for notification handling
- **Request verification** with Cloudflare integration

**Directory Structure:**
```
src/
├── domain/              # Contact message domain entities
├── application/         # Contact message services and event handlers
├── infrastructure/      # Persistence, Slack integration, security
├── api/                # FastAPI routes and request schemas
├── user/               # User management and authentication
└── setup/              # Application configuration and DI
```

## Setup Instructions

### Prerequisites

1. **Python 3.12+**
2. **UV package manager**
3. **PostgreSQL** (handled via Docker Compose)
4. **Google Cloud SDK** (for authentication to private package registry)
5. **Slack Bot Token** (for alert notifications)
6. **Cloudflare Turnstile** (for spam protection)

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

The service will be available at `http://localhost:8002`

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
| `SLACK_ALERT_BOT_TOKEN` | Slack bot token for notifications | `xoxb-...` |
| `SLACK_ALERT_BOT_CHANNEL` | Slack channel for alerts | `#support` |
| `CLOUDFLARE_SECRET_KEY` | Turnstile verification secret | Cloudflare secret |
| `DATABASE_ENCRYPTION_KEY` | Database field encryption | Secure random key |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `UVICORN_PORT` | HTTP server port | `8002` |
| `CLOUDFLARE_URL` | Turnstile verification URL | Cloudflare API endpoint |
| `KEYCLOAK_*` | Authentication service config | Optional for contact forms |
| `GCP_PROJECT_ID` | PubSub project ID | `test` (for emulator) |

See `.env.example` for complete configuration reference.

## API Documentation

### Core Endpoints

**Contact Management:**
- `POST /api/v1/contact-us/` - Submit contact form
  - Requires Cloudflare Turnstile token
  - Validates email, name, message, and category
  - Triggers Slack notification event

**Authentication (Optional):**
- `POST /api/v1/auth/token` - Get access token
- `POST /api/v1/auth/refresh` - Refresh token

**Health Check:**
- `GET /api/v1/health` - Service health status

### Contact Form Schema

```json
{
  "category": "general|bug_report|feature_request|support",
  "email": "user@example.com",
  "name": "User Name",
  "message": "Contact message content",
  "token": "cloudflare_turnstile_token",
  "data": {},  // Optional metadata
  "user_id": "optional_user_id"
}
```

### Response Codes
- `201 Created` - Message submitted successfully
- `400 Bad Request` - Invalid request data or verification failed
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### OpenAPI Documentation
- **Swagger UI:** `http://localhost:8002/docs`
- **ReDoc:** `http://localhost:8002/redoc`
- **OpenAPI JSON:** `http://localhost:8002/openapi.json`

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
1. Modify SQLAlchemy models in domain layer
2. Generate migration: `make revision`
3. Test migration in development environment
4. Include migration in pull request

### Event Integration
- Publish contact message events for notification processing
- Use type-safe event schemas from shared packages
- Handle event failures gracefully with retries
- Test event handlers in isolation

### Security Considerations
- Always validate Cloudflare Turnstile tokens
- Sanitize and validate all input data
- Use encrypted database fields for sensitive data
- Implement proper rate limiting for contact forms
- Monitor for spam and abuse patterns