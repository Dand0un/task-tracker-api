# Task Tracker API

A small learning REST API for tracking tasks built with FastAPI and Pydantic. The service uses an in-memory repository (no database) so state is ephemeral and lost when the process restarts.

**Highlights**
- CRUD endpoints for tasks (`/tasks`)
- Query filters for listing tasks (status, priority, title, assignee, due_date)
- Overdue filter: `overdue=true` returns tasks with a past due date that are not `Done`
- Interactive Swagger UI at `/docs`

## Quick setup

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. (Optional) Copy environment template if you use env vars:

```powershell
Copy-Item .env.example .env
```

## Run the server

Start the app with uvicorn:

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Health check

Verify the service is up:

```powershell
curl http://127.0.0.1:8000/health
```

Sample response:

```json
{
  "status": "ok",
  "timestamp": "2026-07-03T12:34:56.789012+00:00"
}
```

## Swagger / OpenAPI

Interactive API docs are available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Use the UI to explore endpoints, try requests, and see model schemas.

## New features: Overdue and Filters

This project supports a number of query filters on the `GET /tasks` endpoint. Filters are provided as query parameters and include:

**API Endpoints**

- **`GET /health`**: Health check — returns service status and UTC timestamp (200).
- **`POST /tasks`**: Create a new task. Request body: `TaskCreate` (JSON). Returns the created `TaskResponse` (201).
- **`GET /tasks`**: List tasks with optional query filters. Supported query params: `status`, `priority`, `title`, `assignee`, `due_date` (dd/MM/YYYY), `overdue` (true/false). Returns `List[TaskResponse]` (200).
- **`GET /tasks/{task_id}`**: Retrieve a task by id. Returns `TaskResponse` (200) or 404 if not found.
- **`PATCH /tasks/{task_id}`**: Update a task. Request body: `TaskUpdate` (JSON). Validates status transitions; returns updated `TaskResponse` (200) or 404.
- **`DELETE /tasks/{task_id}`**: Delete a task by id. Returns 204 on success or 404 if not found.

Use the Swagger UI at `/docs` to view request/response schemas and to try these endpoints interactively.

- `status` — exact match; allowed values: `ToDo`, `InProgress`, `Done`
- `priority` — exact match: `Low`, `Medium`, `High`
- `title` — case-insensitive substring match
- `assignee` — case-insensitive exact match
- `due_date` — exact date match in `dd/MM/YYYY` format
- `overdue` — boolean flag; when `true` returns tasks with a past `due_date` and `status != Done`

Examples:

- Create a task (with `due_date` in `dd/MM/YYYY`):

```powershell
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Pay invoices\", \"due_date\": \"01/01/2020\", \"priority\": \"High\", \"assignee\": \"alice\"}"
```

- List overdue tasks:

```powershell
curl "http://127.0.0.1:8000/tasks?overdue=true"
```

- Filter by status and assignee:

```powershell
curl "http://127.0.0.1:8000/tasks?status=ToDo&assignee=alice"
```

- Search by title substring (case-insensitive):

```powershell
curl "http://127.0.0.1:8000/tasks?title=invoices"
```

- Filter by due date (exact match, `dd/MM/YYYY`):

```powershell
curl "http://127.0.0.1:8000/tasks?due_date=01/01/2020"
```

Tip: use the Swagger UI at `/docs` to compose and test these queries interactively — enums and date formats are shown on the model schemas.

## Notes

- The storage is in-memory; restart of the server clears all tasks.
- Due dates must be provided in `dd/MM/YYYY` format (e.g. `31/12/2026`).
- The `overdue` filter returns tasks whose `due_date` is before today and whose `status` is not `Done`.

