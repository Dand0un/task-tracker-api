# Task Tracker Architecture

## What the app does

Task Tracker is a small FastAPI REST API with a standalone browser UI for creating, viewing, editing, moving, and deleting tasks across To Do, In Progress, and Done states. Task data is held in process memory, so it is lost on restart.

## Data model

`Task`: `id` (UUID string), `title` (required, trimmed, 1–200 chars), `description` (default `""`), `status` (`ToDo` | `InProgress` | `Done`, default `ToDo`), `priority` (`Low` | `Medium` | `High`, default `Medium`), optional `assignee`, and UTC `created_at` / `updated_at` timestamps.

## Request flow — create task

1. The browser form sends `POST http://localhost:8000/tasks` as JSON.
2. FastAPI parses the request into `TaskCreate`; Pydantic validates fields.
3. `create_task` calls `storage.add_task`.
4. Storage generates a UUID and UTC timestamps, stores a `TaskResponse` in the module-level dictionary, and returns it.
5. The API responds `201 Created`; the UI closes the modal and reloads the task list.

## Key files

- `app/main.py` — FastAPI app, CORS setup, health endpoint, and task CRUD routes.
- `app/models.py` — task enums and Pydantic create/update/response schemas.
- `app/storage.py` — in-memory dictionary and CRUD operations.
- `app/business_rules.py` — permitted task-status transitions.
- `frontend/index.html` — standalone task-board UI and API calls.
- `app/core/config.py` — `.env` loading and basic runtime settings.
- `app/schemas/health.py` — health-check response schema.
- `tests/test_tasks.py` — API behavior coverage.
- `tests/conftest.py` — test client and storage-reset fixtures.
- `requirements.txt` — pinned Python dependencies.

## Conventions

- **Validation:** Pydantic rejects unknown fields and invalid enum values with `422`; titles are normalized and validated before route logic.
- **Storage:** In-memory `dict[str, TaskResponse]`, preserving insertion order; no database or ORM is implemented.
- **Errors:** Missing tasks produce `404`; invalid status changes produce `422`. Allowed changes are `ToDo → InProgress → Done`, with `Done → InProgress` also allowed; no-op status updates are allowed.
- **Frontend/backend:** The static HTML uses `fetch` against a hard-coded localhost API URL. CORS permits local port-5500 origins; the UI refreshes after creates and rolls back optimistic drag-and-drop status changes on failure.

## Not visible or assumptions

- `app/main.py` does not serve the frontend file; it appears intended to be opened or hosted separately.
- Authentication, authorization, multi-user ownership, persistence, migrations, observability, and deployment configuration are not implemented or not confirmed.
- The README mentions optional JSON-backed storage, but the current source contains only in-memory storage; JSON persistence is not confirmed.
