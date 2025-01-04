# Labour Tracker
 
## Setup

### Prerequisites

Docker and Docker Compose

### Installation

Installation on mac/linux is as follows:

```bash
make build
```

This command builds all of the necessary images.

```bash
make run
```

This command runs the longer running docker compose services:
- db (The postgres database, `app` and `keycloak` databases will be created on startup)
- keycloak (The `labour_tracker` realm will be imported on startup)
- kafka
- zookeeper
- kafka-ui

It is necessary to reset the `labour_tracker_backend` client secret by:
- Logging into the [keycloak admin console](http://localhost:8080).
  - username: admin
  - password: password
- Navigating to:
  - `labour_tracker` realm
  - `labour_tracker_backend` client
  - Credentials
  - Click `Regenerate` for the client secret
  - Copy into the env var: `KEYCLOAK_CLIENT_SECRET`

In a new terminal

```bash
make run-backend
```
To run the rest of the backend services.

The Swagger UI is avaliable at http://localhost:8000

![preview](./docs/images/swagger-ui.png)

To login:
1. Navigate to [Keycloak](localhost:8080/realms/labour_tracker/account) and register
![preview](./docs/images/login.png)
2. With your credentials, login with the swagger endpoint `/api/v1/auth/login`
3. Click the `Authorize` button in the top right and copy in the token string from the login response



## Usage

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


## Acknowledgements

This project's structure was inspired by and built upon the following template repositories:

[fastapi-clean-example by Ivan Borovets](https://github.com/ivan-borovets/fastapi-clean-example)

[full-stack-fastapi-template by FastAPI](https://github.com/fastapi/full-stack-fastapi-template)

Please checkout the first repo, firstly for the brilliant README, but mainly for a better example of using clean architecture and DDD than this repo.
