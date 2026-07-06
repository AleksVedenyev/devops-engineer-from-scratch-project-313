FROM python:3.14-slim

# Install only required packages, avoid recommended ones and clean up lists to reduce image size
RUN apt-get update \
	&& apt-get install -y --no-install-recommends curl ca-certificates gnupg2 ca-certificates lsb-release \
	&& curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
	&& apt-get install -y --no-install-recommends nodejs \
    && apt-get install -y --no-install-recommends nginx \
	&& rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="$PATH:/root/.local/bin"

WORKDIR /app

COPY package*.json ./
COPY uv.lock ./
COPY pyproject.toml ./
RUN uv sync

RUN npm ci --only=production

COPY . .
COPY ./node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/. /app/public/

CMD ["start", "nginx", "uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]