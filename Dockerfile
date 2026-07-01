FROM python:3.14-slim

RUN apt-get update && apt-get install curl -y
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="$PATH:/root/.local/bin"

WORKDIR /app

COPY uv.lock ./
COPY pyproject.toml ./
RUN uv sync

COPY . .

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]