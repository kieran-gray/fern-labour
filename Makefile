include .env

run:
	@echo "Starting all services..."
	npm run dev;
	@echo "Services started."

stop:
	@echo "Stopping services..."
	docker compose down
	@echo "Services stopped."
