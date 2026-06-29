install:
	uv sync

make run:
	uv run uvicorn main:app --reload --port 8080