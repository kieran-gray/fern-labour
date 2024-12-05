# Contraction Tracker Backend

contraction-tracker-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   ├── core/                        # Core configurations and utilities
│   │   ├── __init__.py
│   │   ├── config.py                # Application settings and configurations
│   │   ├── dependencies.py          # Dependency injection setup
│   │   ├── exceptions.py            # Custom exceptions
│   │   ├── security.py              # Authentication and authorization utilities
│   ├── domain/                      # Domain layer (business rules)
│   │   ├── __init__.py
│   │   ├── models/                  # Domain models/entities
│   │   │   ├── __init__.py
│   │   │   ├── contraction.py       # Contraction entity definition
│   │   │   ├── user.py              # User entity definition
│   │   ├── repositories/            # Abstract repository interfaces
│   │       ├── __init__.py
│   │       ├── contraction_repo.py  # Contraction repository interface
│   │       ├── user_repo.py         # User repository interface
│   ├── application/                 # Application layer (use cases/interactors)
│   │   ├── __init__.py
│   │   ├── use_cases/               # Business logic for use cases
│   │       ├── __init__.py
│   │       ├── track_contraction.py # Use case to track a contraction
│   │       ├── get_contractions.py  # Use case to fetch contractions
│   │   ├── services/                # Domain services
│   │       ├── __init__.py
│   │       ├── notification_service.py  # Notify users (e.g., alert on frequent contractions)
│   ├── infrastructure/              # Infrastructure layer (database, external APIs)
│   │   ├── __init__.py
│   │   ├── database/                # Database setup and models
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # SQLAlchemy base model
│   │   │   ├── contraction_model.py # Contraction database model
│   │   │   ├── user_model.py        # User database model
│   │   ├── repositories/            # Repository implementations
│   │       ├── __init__.py
│   │       ├── contraction_repo_impl.py  # Contraction repository implementation
│   │       ├── user_repo_impl.py         # User repository implementation
│   │   ├── external_services/       # Communication with external APIs
│   │       ├── __init__.py
│   │       ├── sms_service.py       # Service to send SMS notifications
│   ├── interfaces/                  # Presentation layer (API endpoints)
│   │   ├── __init__.py
│   │   ├── api_v1/                  # API versioning
│   │       ├── __init__.py
│   │       ├── endpoints/           # API route handlers
│   │       │   ├── __init__.py
│   │       │   ├── contraction.py   # Endpoints for contraction tracking
│   │       │   ├── user.py          # Endpoints for user management
│   │       ├── schemas/             # Pydantic models for request/response
│   │           ├── __init__.py
│   │           ├── contraction.py   # Schemas for contractions
│   │           ├── user.py          # Schemas for user data
│   ├── tests/                       # Test cases
│       ├── __init__.py
│       ├── test_main.py             # Tests for main FastAPI app
│       ├── unit/                    # Unit tests
│       │   ├── __init__.py
│       │   ├── test_contraction.py  # Unit tests for contractions
│       ├── integration/             # Integration tests
│           ├── __init__.py
│           ├── test_contraction_api.py  # Tests for contraction-related API endpoints
├── alembic/                         # Database migration tool configuration
│   ├── env.py
│   ├── script.py.mako
│   ├── versions/
├── .env                             # Environment variables
├── .gitignore                       # Git ignore file
├── Dockerfile                       # Docker configuration
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation