# 🔍 Repo Analyzer

> Submit a GitHub repository URL, get an AI-powered analysis of it.

A backend portfolio project built with **FastAPI**, combining async task processing, GitHub API integration, and AI-driven code analysis.

---

## ✨ How It Works

### 1. Two-Step Signup
- User submits initial credentials (username, email, password).
- A verification code is sent to their email **asynchronously** via Celery.
- User confirms the code → account is created.

### 2. Login
- User logs in with username/password.
- On success, receives a **JWT** access token.

### 3. Repository Analysis
- Authenticated user submits a GitHub repo URL.
- Repo metadata is fetched from the **GitHub API**.
- Content is sent to an AI model (via **OpenRouter**) for analysis.
- Result is returned to the user.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| Async Tasks | Celery + Redis |
| Migrations | Alembic |
| Auth | JWT |
| AI Analysis | OpenRouter API |
| External Data | GitHub API |
| Deployment | Docker Compose |

---

## 🏗️ Architecture

Clean three-layer architecture for separation of concerns:

```
Router  →  Service  →  Repository
(HTTP)     (Logic)     (Database)
```

- **Router** — HTTP gateway, request/response validation
- **Service** — business logic, orchestration
- **Repository** — direct database operations

---

## 🚀 Getting Started

### Local Development

```bash
docker compose up -d db redis
uvicorn app.main:app --reload
celery -A app.core.celery:celery_app worker --loglevel=info --pool=solo
```

### Production

```bash
docker compose up -d --build
```

---

## ⚙️ Environment Variables

```dotenv
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/app
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
MAIL_USERNAME=...
MAIL_PASSWORD=...
MAIL_SERVER=...
MAIL_PORT=...
REDIS_HOST=...
REDIS_PORT=...
```

---

## 📌 Roadmap

- [ ] Rate limiting on signup/login endpoints
- [ ] Pagination for repo history
- [ ] Caching analysis results