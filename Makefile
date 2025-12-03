include .env

run:
	@echo "Starting all services..."
	docker compose up --build -d;
	npm run dev:admin;
	@echo "Services started."

stop:
	@echo "Stopping services..."
	docker compose down
	@echo "Services stopped."
