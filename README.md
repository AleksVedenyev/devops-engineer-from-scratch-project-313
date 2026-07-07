# URL Shortener App (DevOps Project)

A production-ready URL shortening service that allows users to create short, manageable links from long URLs.

The application includes:

- 🚀 FastAPI REST API backend
- 🎨 Frontend application
- 🌐 Nginx reverse proxy
- 🐳 Dockerized deployment
- 🗄️ PostgreSQL managed database on Render
- ⚙️ CI/CD pipeline with GitHub Actions

---

# CI/CD Status

### Hexlet Check

[![Actions Status](https://github.com/AleksVedenyev/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AleksVedenyev/devops-engineer-from-scratch-project-313/actions)

### CI Pipeline

[![CI](https://github.com/AleksVedenyev/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml/badge.svg)](https://github.com/AleksVedenyev/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml)

---

# Live Demo

[![Render](https://img.shields.io/badge/Render-Deployed-success?style=flat&logo=render&logoColor=white)](https://devops-engineer-from-scratch-project-313-94br.onrender.com)

Application URL:

https://devops-engineer-from-scratch-project-313-94br.onrender.com

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | REST API backend |
| **PostgreSQL** | Managed production database hosted on Render |
| **Nginx** | Reverse proxy and frontend static file server |
| **Docker** | Application containerization |
| **Node.js** | Frontend dependency installation and build |
| **uv** | Python package manager |
| **Uvicorn** | ASGI server |
| **Pytest** | Automated testing |
| **Ruff** | Code linting |

---

# Production Architecture

The application is deployed as a Docker container.

The container includes:

- FastAPI backend
- Uvicorn server
- Nginx reverse proxy
- Frontend static files

PostgreSQL runs as a separate managed database service on Render.

```
             Client
                │
                ▼
          Nginx (Port 80)
          ├──────────────► Frontend static files
          │
          ▼
        FastAPI
          │
          ▼
 PostgreSQL (Render Database)
```

Nginx serves frontend assets and proxies API requests to the FastAPI application.

---

# Local Development

## Prerequisites

Install:

- Python 3.13+
- uv
- Node.js
- Git

---

## Clone the repository

```bash
git clone https://github.com/AleksVedenyev/devops-engineer-from-scratch-project-313.git

cd devops-engineer-from-scratch-project-313
```

---

## Install dependencies

```bash
make install
```

---

## Run development mode

Starts frontend development server and FastAPI backend simultaneously.

```bash
make dev
```

Backend will be available at:

```
http://localhost:8080
```

---

## Run backend only

```bash
make run
```

---

## Run tests

```bash
make test
```

---

## Run linter

```bash
make lint
```

---

# Docker

## Build image

```bash
docker build -t url-shortener .
```

## Run container

```bash
docker run -p 80:80 url-shortener
```

Application will be available at:

```
http://localhost
```

---

# Environment Variables

Production environment variables are configured through Render.

The application uses environment variables for external services such as the PostgreSQL database connection.

For local development, create a `.env` file with required values.

Example:

```env
DATABASE_URL=your_database_connection_string
```

---

# Available Make Commands

| Command | Description |
|---------|-------------|
| `make install` | Install project dependencies |
| `make run` | Start FastAPI backend |
| `make dev` | Run frontend and backend in development mode |
| `make test` | Run test suite |
| `make lint` | Run Ruff linter |

---

# Deployment

The application is automatically tested and deployed using GitHub Actions.

Deployment platform:

- Application: Render
- Database: Render PostgreSQL

Production URL:

https://devops-engineer-from-scratch-project-313-94br.onrender.com
