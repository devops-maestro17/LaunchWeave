# 🧵 LaunchWeave

[![CI — Test Suite](https://github.com/devops-maestro17/LaunchWeave/actions/workflows/ci.yml/badge.svg)](https://github.com/devops-maestro17/LaunchWeave/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)

LaunchWeave is a production-engineered Task Management REST API designed as a realistic practice target for mastering **GitHub Actions, Kubernetes, Helm, Terraform, Karpenter, and GitOps (ArgoCD)** on AWS (`ap-south-1`).

---

## 🏗️ Architecture Overview

- **Web Framework:** FastAPI (Asynchronous Python ASGI)
- **Production Server:** Gunicorn + Uvicorn Workers
- **Database:** PostgreSQL (SQLAlchemy ORM + connection pooling with `pool_pre_ping`)
- **Cloud Database:** Neon Serverless PostgreSQL (ephemeral test branches + pooled production)
- **Containerization:** Multi-stage, non-root Docker runtime with healthchecks
- **CI/CD & GitOps:** GitHub Actions, Helm OCI, Kind (CI/Dev), AWS EKS with Karpenter (Staging/Prod), ArgoCD

---

## 📡 API Endpoints & Kubernetes Probes

| Endpoint | Method | Purpose | Kubernetes Role |
| :--- | :--- | :--- | :--- |
| `/healthz` | `GET` | Process liveness probe | Liveness Probe (Restarts container if stalled) |
| `/readyz` | `GET` | Database connectivity probe | Readiness Probe (Removes pod from service endpoints if DB fails) |
| `/tasks` | `GET` | List all tasks | Application API |
| `/tasks` | `POST` | Create a new task | Application API |
| `/tasks/{id}` | `PATCH` | Update task fields (completed, title, desc) | Application API |
| `/tasks/{id}` | `DELETE` | Delete a task | Application API |

---

## 🚀 Quickstart

### Option 1: Docker Compose (Recommended for local dev)

Starts both the PostgreSQL database and the LaunchWeave API with hot reload:

```bash
docker compose up -d
```

- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health probe: [http://localhost:8000/healthz](http://localhost:8000/healthz)
- Readiness probe: [http://localhost:8000/readyz](http://localhost:8000/readyz)

Stop services:
```bash
docker compose down -v
```

### Option 2: Local Python Virtual Environment

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate    # Linux / macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env

# 4. Run application
make run
# or: uvicorn app.main:app --reload --port 8000
```

---

## 🧪 Testing

```bash
# Run pytest test suite
make test

# Run manual API verification checks
make test-neon
```

---

## 📚 Learning Documentation

All architectural decisions, phase implementations, troubleshooting runbooks, and cheatsheets are stored in the [`docs/`](docs/) directory:

- [Documentation Index](docs/README.md)
- [DevOps Glossary](docs/glossary.md)
- [Phase 0: Foundations & App Readiness](docs/phases/00-foundations.md)
- [GitHub Actions Expressions & Contexts Cheatsheet](docs/cheatsheets/gha-expressions-and-contexts.md)