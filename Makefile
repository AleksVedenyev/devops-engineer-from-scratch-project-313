install:
	uv sync

run:
	uv run uvicorn main:app --reload --port 8080

test:
	uv run python3 -m pytest

lint:
	uv run ruff check