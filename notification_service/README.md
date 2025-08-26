# Notification Service

## Overview

The Notification Service handles all outbound communications for the labour tracking application, including emails, SMS, and WhatsApp notifications. This service processes notification requests from other services and manages delivery through multiple channels with retry logic, status tracking, and template management.

**Key Responsibilities:**
- Multi-channel notification delivery (Email, SMS, WhatsApp)
- Template-based message generation with Jinja2
- Delivery status tracking and retry mechanisms
- Event-driven notification processing via PubSub
- CLI tools for notification management and monitoring
- Integration with Twilio for SMS/WhatsApp and SMTP for email

## Architecture & Dependencies

**Framework & Technologies:**
- **FastAPI** - High-performance async web framework
- **SQLAlchemy 2.0** - Database ORM with async support
- **Dishka** - Dependency injection container
- **Alembic** - Database migration management
- **Pydantic** - Data validation and serialization
- **PostgreSQL** - Primary database
- **Google Cloud PubSub** - Event messaging (emulated locally)
- **Jinja2** - Template engine for notification content
- **Twilio SDK** - SMS and WhatsApp delivery
- **Emails Library** - SMTP email delivery
- **uvloop** - High-performance event loop

**Architecture Pattern:**
- **Domain-Driven Design (DDD)** with Clean Architecture
- **Event-Driven Architecture** for notification processing
- **Gateway Pattern** for multi-channel delivery abstraction
- **Template Engine Integration** for dynamic content generation

**Directory Structure:**
```
src/
├── notification/           # Notification domain
│   ├── domain/            # Notification entities, enums, events
│   ├── application/       # Services and event handlers
│   └── infrastructure/    # SMTP, Twilio, template gateways
├── core/                  # Shared domain infrastructure
├── api/                   # FastAPI routes and schemas
├── user/                  # User management and authentication
├── cli.py                 # Command-line tools
└── setup/                 # Application configuration and DI
```

## Setup Instructions

### Prerequisites

1. **Python 3.12+**
2. **UV package manager**
3. **PostgreSQL** (handled via Docker Compose)
4. **Google Cloud SDK** (for authentication to private package registry)
5. **Twilio Account** (for SMS/WhatsApp delivery)
6. **SMTP Server** (for email delivery - uses MailCatcher locally)

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

The service will be available at `http://localhost:8001`

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

### Background Jobs
- **Notification Consumer** - Processes PubSub notification events
- **Status Update Job** - Periodically fetches delivery statuses from providers

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
| `DATABASE_ENCRYPTION_KEY` | Database field encryption | Secure random key |

### Email Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `SMTP_HOST` | SMTP server hostname | `mailcatcher` (dev), `smtp.gmail.com` (prod) |
| `SMTP_PORT` | SMTP server port | `1025` (dev), `587` (prod) |
| `SMTP_USER` | SMTP authentication username | Email address |
| `SMTP_PASSWORD` | SMTP authentication password | App password |
| `EMAILS_FROM_EMAIL` | Sender email address | `noreply@fernlabour.com` |
| `EMAILS_FROM_NAME` | Sender display name | `Fern Labour` |
| `SMTP_SSL` | Use SSL encryption | `true`, `false` |
| `SMTP_TLS` | Use TLS encryption | `true`, `false` |

### SMS/WhatsApp Configuration (Twilio)

| Variable | Description | Example |
|----------|-------------|---------|
| `TWILIO_ACCOUNT_SID` | Twilio account identifier | `AC...` |
| `TWILIO_AUTH_TOKEN` | Twilio authentication token | Secret token |
| `SMS_FROM_NUMBER` | Twilio phone number for SMS | `+1234567890` |
| `MESSAGING_SERVICE_SID` | Twilio messaging service ID | `MG...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `UVICORN_PORT` | HTTP server port | `8001` |
| `GCP_PROJECT_ID` | PubSub project ID | `test` (for emulator) |
| `SUPPORT_EMAIL` | Support contact email | `support@fernlabour.com` |
| `TRACKING_LINK` | Email tracking base URL | Tracking service URL |

See `.env.example` for complete configuration reference.

## API Documentation

### Core Endpoints

**Health Check:**
- `GET /api/v1/health` - Service health status

**Authentication (Optional):**
- `POST /api/v1/auth/token` - Get access token
- `POST /api/v1/auth/refresh` - Refresh token

### Notification Channels

**Supported Channels:**
- `email` - SMTP email delivery
- `sms` - Twilio SMS delivery
- `whatsapp` - Twilio WhatsApp delivery

**Delivery Status:**
- `created` - Notification created but not sent
- `sent` - Notification sent to provider
- `success` - Delivery confirmed successful
- `failure` - Delivery failed

### Event Integration

The service listens for notification events via PubSub:
- Labour begun/completed events
- Subscription notifications
- Contact form alerts
- System notifications

### OpenAPI Documentation
- **Swagger UI:** `http://localhost:8001/docs`
- **ReDoc:** `http://localhost:8001/redoc`
- **OpenAPI JSON:** `http://localhost:8001/openapi.json`

## CLI Tools

The service includes command-line tools for notification management:

### Fetch Delivery Status
Updates notification delivery statuses from external providers:

```bash
python src/cli.py fetch-status
```

### Resend Notification
Resends a failed or unsent notification:

```bash
python src/cli.py resend --notification-id <notification-id>
```

### Running in Docker
CLI tools can be executed in the Docker container:

```bash
docker compose exec notification-service python src/cli.py fetch-status
```

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

### Adding New Notification Channels

1. **Create Gateway Implementation:**
   ```python
   # src/notification/infrastructure/gateways/new_gateway.py
   class NewChannelGateway(NotificationGateway):
       async def send(self, notification: Notification) -> NotificationResult:
           # Implement channel-specific delivery logic
   ```

2. **Update Enums:**
   ```python
   # src/notification/domain/enums.py
   class NotificationChannel(StrEnum):
       NEW_CHANNEL = "new_channel"
   ```

3. **Register in DI Container:**
   ```python
   # src/setup/ioc/di_providers/notification_providers.py
   # Add provider registration
   ```

4. **Add Templates:**
   Create Jinja2 templates for the new channel in infrastructure layer

### Template Management
- Templates use Jinja2 syntax
- Store templates in infrastructure layer
- Support both plain text and HTML formats for email
- Test templates with various data inputs

### Monitoring & Alerting
- Monitor delivery success rates by channel
- Set up alerts for high failure rates
- Track notification volume and performance metrics
- Log all delivery attempts with correlation IDs