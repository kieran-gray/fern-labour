# Labour Tracker
 
## Setup

### Prerequisites

Docker and Docker Compose

### Environment variable setup

cp .env.example .env

in root, labour_service, and notification_service.

### Installation

First we need to login to GCP and setup some application-default credentials for pulling project dependencies from the private package repository.

1. Login

    `gcloud auth login`

2. Initialise (follow all steps in terminal)

    `gcloud init`

3. Login to application-default

    `gcloud auth application-default login`


Add 127.0.0.1 keycloak to `/etc/hosts` to enable keycloak to work properl on the frontend.

```bash
make run
```

This command builds and runs the full stack.

The frontend is available at http://localhost:5173
The backend is avaliable at http://localhost:8000

![preview](./docs/images/swagger-ui.png)

### TODO the rest of the docs