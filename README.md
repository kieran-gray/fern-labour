# Labour Tracker

A FastAPI-based backend service for tracking labour-related data, built with Domain-Driven Design principles and clean architecture.

## Features

- REST API built with FastAPI
- Event-driven architecture using Apache Kafka
- Notification system integrated with:
  - Twilio for SMS
  - SFTP for email delivery
- PostgreSQL database for persistent storage
- Clean/layered architecture with dependency injection using Dishka

## Architecture

This project is a primitive attempt to follow Domain-Driven Design principles and clean architecture patterns. The application is structured in layers:

- **Domain Layer**: Contains business logic and domain models
- **Application Layer**: Orchestrates use cases and application flow
- **Infrastructure Layer**: Handles external concerns (database, messaging, etc.)
- **Presentation Layer**: API endpoints and request/response handling

### Event-Driven System

The application uses Apache Kafka for asynchronous event processing, primarily enabling the
decoupling of notification handling (sending emails and texts) from the triggers of the
notifications.

## Technical Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Message Broker**: Apache Kafka
- **Dependency Injection**: Dishka
- **Notifications**:
  - Twilio SDK for SMS
  - SFTP for email delivery
- **Development Tools**:
  - Ruff for linting and formatting
  - isort for import sorting
  - mypy for static type checking
