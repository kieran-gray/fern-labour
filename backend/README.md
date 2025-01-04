# Labour Tracker Backend

A FastAPI-based backend service for tracking labour-related data, built as a first attempt to use Domain-Driven Design principles and clean architecture.

## Features

- REST API built with FastAPI
- Event-driven architecture using Apache Kafka
- Notification system integrated with:
  - Twilio for SMS
  - SMTP for email delivery
- PostgreSQL database for persistent storage
- Clean/layered architecture with dependency injection using Dishka

## Architecture

The application is structured in the following layers:

- **Domain Layer**: Contains business logic and domain models
- **Application Layer**: Orchestrates use cases and application flow
- **Infrastructure Layer**: Handles external concerns (database, messaging, etc.)
- **Presentation Layer**: API endpoints and request/response handling

## Domain Model

A simplified domain model is as follows:
![preview](./docs/images/domain_model.svg)

- **Generic Domain**: Contains the identity and access bounded context. Interactions with other bounded contexts should go through an Anti-Corruption Layer (ACL) which translates the auth providier specific User implementation into the domain User implementation.

- **Core Domain**: Contains the labour tracking and subscriptions bounded contexts. Interactions between these bounded contexts take place through a messaging mechanism.

### Event-Driven System

The application uses Kafka for asynchronous event processing, for two different reasons:
- Decoupling notification handling (sending emails and texts) from the triggers of the notifications (endpoints).
  - The event types used for this purpose are:
    - `labour.begun`
    - `labour.completed`
    - `contraction.ended`
<br>

- Triggering side-effects across multiple aggregates.
  - The event types used for this purpose are:
    - `subscriber.subscribed_to`
    - `subscriber.unsubscribed_from`
  - These events are triggered in the `Subscriber` aggregate, and cause additional logic to run on the `BirthingPerson` aggregate.

## Technical Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Message Broker**: Kafka
- **Dependency Injection**: Dishka
- **Notifications**:
  - Twilio SDK for SMS
  - SMTP for email delivery
- **Development Tools**:
  - Ruff for linting and formatting
  - isort for import sorting
  - mypy for static type checking