# Labour Tracker Backend

A FastAPI-based backend service for tracking labour-related data, built as a first attempt to use Domain-Driven Design principles and clean architecture.

## Setup

To install the necessary dependencies, run the command:
`make deps`


Test that all of the dependencies have been install correctly by running the tests with the command:
`make test`

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

## Usage

To login:
1. Navigate to [Keycloak](localhost:8080/realms/labour_tracker/account) and register
![preview](./docs/images/login.png)
2. With your credentials, login with the swagger endpoint `/api/v1/auth/login`
3. Click the `Authorize` button in the top right and copy in the token string from the login response

The flow for a Birthing Person is as follows:
1. Sign in through Keycloak
2. Register at: `/api/v1/birthing-person/register`
3. Begin Labour at: `/api/v1/labour/begin`
4. Start Contractions at: `/api/v1/labour/contraction/start`
5. End Contractions at: `/api/v1/labour/contraction/end`
6. Complete Labour at: `/api/v1/labour/complete`

The flow for a subscriber is as follows:
1. Sign in through Keycloak
2. Register at: `/api/v1/subscriber/register`
3. Have a Birthing Person provide you with their ID and token
    1. Birthing Person ID can be found here: `/api/v1/birthing-person`
    2. Tokens can be generated here: `/api/v1/birthing-person/subscription-token`
4. Subscribe to them here: `/api/v1/subscriber/subscribe_to/{birthing_person_id}`
    1. Valid contact methods are:
        1. "sms"
        2. "email"
    2. Use email for testing purposes
5. Now if the Birthing Person Begins or Completes Labour a notification will be sent to that user
6. You will see the event handled in the consumer logs
7. The email can be viewed in MailCatcher here: http://localhost:1080/
