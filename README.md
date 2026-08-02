# Task Tracker API

A REST API for tracking tasks, built with FastAPI and Pydantic as a learning project. It uses a simple in-memory (optionally JSON-backed) repository layer, keeping the stack lightweight and easy to run locally.

## Setup

### 1. Create and activate a virtual environment (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

```powershell
Copy-Item .env.example .env
```

## Running the server

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs are at `http://127.0.0.1:8000/docs`.

## Testing the health endpoint

```powershell
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2026-07-03T12:34:56.789012+00:00"
}
```

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker API remains within the intended course scope.
- CI runs the pytest suite on pushes and pull requests.
- The Docker image builds and its `/health` endpoint returns HTTP 200.
- AI review, security, ownership, and release evidence are recorded in `docs/`.

### How to run locally

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
py -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

To view the Kanban frontend, open `frontend/index.html` with VS Code Live Server at `http://127.0.0.1:5500` while the API is running.

### How to run tests

```powershell
py -m pytest -v
```

### How to run with Docker

```powershell
docker build --tag task-tracker-api:final .
docker run --rm --name task-tracker-api-final --publish 8000:8000 task-tracker-api:final
```

In a second PowerShell window:

```powershell
curl.exe http://127.0.0.1:8000/health
```

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### AI assistance summary

AI helped draft or review the CI workflow, Docker configuration, release documentation, and security findings. I verified the work through pytest, a `/health` check, Docker build/run verification, and manual inspection of the workflow and Dockerfile. I did not accept an AI claim that Docker verification was complete until the image had built and the running container returned HTTP 200 from `/health`.
