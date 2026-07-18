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