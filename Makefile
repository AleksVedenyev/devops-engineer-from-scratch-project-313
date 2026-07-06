install:
	uv sync

run:
	uv run --env-file .env uvicorn main:app --port 8080

dev:
	npx concurrently "npx start-hexlet-devops-deploy-crud-frontend" "uv run uvicorn main:app --port 8080"

test:
	uv run python3 -m pytest

lint:
	uv run ruff check