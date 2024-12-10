# Contraction Tracker Backend

contraction-tracker-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                     # Entry point for the FastAPI app
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Configuration settings
│   │   ├── errors.py               # Custom error definitions
│   │   └── dependencies.py         # Shared dependencies (e.g., database, authentication)
|   |
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                 # User aggregate root
│   │   │   ├── contraction.py          # Contraction entity
│   │   │   └── labor_session.py        # LaborSession aggregate root
│   │   │
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   ├── email.py
│   │   │   ├── password.py
│   │   │   └── duration.py             # For contraction duration
│   │   │
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── user_repository.py
│   │       └── labor_session_repository.py
|   |
│   ├── application/
│   │   ├── __init__.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py         # Authentication service
│   │   │   ├── labor_tracker_service.py # Core labor tracking logic
│   │   │   └── notification_service.py  # Hospital notification service
│   │   │
│   │   └── dtos/
│   │       ├── __init__.py
│   │       ├── user_dto.py
│   │       └── contraction_dto.py
|   |
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user_model.py
│   │   │   │   └── labor_session_model.py
│   │   │   │
│   │   │   └── repositories/
│   │   │       ├── __init__.py
│   │   │       ├── sqlalchemy_user_repository.py
│   │   │       └── sqlalchemy_labor_session_repository.py
│   │   │
│   │   ├── external_services/
│   │   |    ├── __init__.py
│   │   |    ├── email_service.py        # Email notification implementation
│   │   |    └── sms_service.py          # SMS notification implementation
|   |   |   
│   │   └── security/
│   │       ├── __init__.py
│   │       ├── auth.py             # Authentication logic
│   │       └── jwt.py              # JWT utilities
|   |
│   ├── presentation/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── contraction.py  # API routes for contractions
│   │   │   │   └── user.py         # API routes for users
│   │   │   └── middlewares.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── contraction.py      # Pydantic schemas for API input/output
│   │   │   └── user.py
│   │   └── controllers/
│   │       ├── __init__.py
│   │       ├── contraction_controller.py  # Coordinates use cases for contractions
│   │       └── user_controller.py         # Coordinates use cases for users
|   |
│   └── tests/
│       ├── __init__.py
│       ├── test_contraction.py     # Unit tests for contraction domain logic
│       ├── test_user.py            # Unit tests for user domain logic
│       ├── test_routes.py          # API endpoint tests
│       └── test_integration.py     # Integration tests
├── .env                            # Environment variables
├── .gitignore                      # Git ignore file
├── pyproject.toml                  # Project dependencies and settings
├── README.md                       # Project documentation
└── requirements.txt                # Python dependencies (if not using pyproject.toml)


contraction_tracker/
│
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                 # User aggregate root
│   │   │   ├── contraction.py          # Contraction entity
│   │   │   └── labor_session.py        # LaborSession aggregate root
│   │   │
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   ├── email.py
│   │   │   ├── password.py
│   │   │   └── duration.py             # For contraction duration
│   │   │
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── user_repository.py
│   │       └── labor_session_repository.py
│   │
│   ├── application/
│   │   ├── __init__.py
│   │   ├── interfaces/
│   │   │   ├── __init__.py
│   │   │   ├── iuser_repository.py
│   │   │   └── ilabor_session_repository.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py         # Authentication service
│   │   │   ├── labor_tracker_service.py # Core labor tracking logic
│   │   │   └── notification_service.py  # Hospital notification service
│   │   │
│   │   └── dtos/
│   │       ├── __init__.py
│   │       ├── user_dto.py
│   │       └── contraction_dto.py
│   │
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user_model.py
│   │   │   │   └── labor_session_model.py
│   │   │   │
│   │   │   └── repositories/
│   │   │       ├── __init__.py
│   │   │       ├── sqlalchemy_user_repository.py
│   │   │       └── sqlalchemy_labor_session_repository.py
│   │   │
│   │   └── external_services/
│   │       ├── __init__.py
│   │       ├── email_service.py        # Email notification implementation
│   │       └── sms_service.py          # SMS notification implementation
│   │
│   └── interfaces/
│       ├── __init__.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── middleware/
│       │   │   ├── __init__.py
│       │   │   └── auth_middleware.py
│       │   │
│       │   └── routes/
│       │       ├── __init__.py
│       │       ├── auth_routes.py
│       │       └── labor_routes.py
│       │
│       └── events/
│           ├── __init__.py
│           └── websocket_handler.py     # Real-time updates
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   │
│   └── integration/
│       ├── __init__.py
│       └── api/
│
├── alembic/                            # Database migrations
│   ├── versions/
│   └── env.py
│
├── config/
│   ├── __init__.py
│   └── settings.py                     # Configuration settings
│
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── main.py
