# Project building
.PHONY: build-dev \
		build-prod \
		build-keycloak \
		build-frontend \
		build \
		clean

build-dev:
	docker build --target dev -t ${DOCKER_IMAGE_BACKEND}-dev ./backend

build-prod:
	docker build --target production -t ${DOCKER_IMAGE_BACKEND} ./backend

build-keycloak:
	docker build -t ${DOCKER_IMAGE_BACKEND}-keycloak ./keycloak -f ./keycloak/Dockerfile --no-cache

build-frontend:
	docker build -t ${DOCKER_IMAGE_FRONTEND} ./frontend -f ./frontend/Dockerfile --build-arg VITE_API_URL="http://localhost:8000"

build: build-dev build-prod build-keycloak build-frontend

clean: 
	docker system prune -a && docker volume prune -a

# Project running
.PHONY: run \
		stop

run:
	docker compose up

stop:
	docker compose down

