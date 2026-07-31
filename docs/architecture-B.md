# Task Tracker Architecture

## What it does

Task Tracker is a small FastAPI REST API with a static browser board for
creating, listing, retrieving, updating, and deleting tasks. The API exposes
`/health` and task endpoints under `/tasks`; FastAPI also supplies interactive
API documentation at `/docs`. The frontend organizes tasks into To Do, In
Progress, and Done columns, and can create, edit, and move tasks.

Task data is held only in process memory. Restarting the API clears all tasks;
there is no database, ORM, authentication, or persistence layer.

## Data model

`TaskCreate` accepts `title`, `description`, `status`, `priority`, and
`assignee`; unknown fields are rejected. `title` is required, trimmed, cannot
be blank, and is limited to 200 characters. Defaults are an empty description,
`ToDo` status, and `Medium` priority. `assignee` is optional.

`TaskResponse` adds a UUID string `id` plus UTC `created_at` and `updated_at`
timestamps. Status values are `ToDo`, `InProgress`, and `Done`; priority
values are `Low`, `Medium`, and `High`. `TaskUpdate` makes the mutable task
fields optional so PATCH requests can be partial.

## Request flow when a user creates a task

1. The browser form in `app/frontend/index.html` trims the title, builds JSON,
   and sends `POST http://localhost:8000/tasks`.
2. FastAPI routes the request to `create_task` in `app/main.py` and validates
   the body as `TaskCreate`. Invalid input receives FastAPI's 422 response
   before the handler runs.
3. The handler calls `storage.add_task`. It creates a UUID and UTC timestamps,
   builds a `TaskResponse`, and saves it in the module-level `_tasks` dictionary.
4. FastAPI serializes the response as `TaskResponse` and returns 201 Created.
   On success, the frontend closes the form and reloads the task list.

## Key files

| File | Role |
| --- | --- |
| `app/main.py` | Application setup, CORS, health endpoint, and task HTTP handlers. |
| `app/models.py` | Pydantic task schemas, enums, defaults, and title validation. |
| `app/storage.py` | In-memory dictionary and CRUD helpers; generates IDs and timestamps. |
| `app/business_rules.py` | Allows only `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress` status changes (same-status updates are allowed). |
| `app/schemas/health.py` | Pydantic response schema for `GET /health`. |
| `app/core/config.py` | Loads `.env` values and exposes `PORT` and `APP_ENV`. |
| `app/frontend/index.html` | Static task-board UI; fetches, creates, edits, and drag-updates tasks. |

## Conventions

- Keep routes thin: validate at the API/schema boundary and delegate storage
  operations to `app/storage.py`.
- Use Pydantic v2 models with `extra="forbid"` for task request and response
  shapes; use enums for status and priority values.
- Store timestamps as timezone-aware UTC datetimes and generate task IDs with
  UUIDs.
- Enforce status-transition policy in `app/business_rules.py` before updates.
- The frontend expects the API at `http://localhost:8000`; CORS permits the
  local development origins configured in `app/main.py`.
