# Task Tracker — Architecture (Strategy C)

## 1. What the app does

Task Tracker is a FastAPI REST API for creating, listing, retrieving, updating, and deleting tasks. It includes a health endpoint and stores tasks in process memory, so task data is lost when the API process restarts.

## 2. Data model

- **Task** (`TaskResponse`): `id`, `title`, `description`, `status`, `priority`, `assignee`, `created_at`, and `updated_at`.
- **Task creation input** (`TaskCreate`): `title` (required), with optional/defaulted `description`, `status`, `priority`, and `assignee`.
- **Task update input** (`TaskUpdate`): all task-editable fields are optional; only explicitly supplied fields are changed.
- **Status values**: `ToDo`, `InProgress`, `Done`.
- **Priority values**: `Low`, `Medium`, `High`.

## 3. Request flow — create a task

1. A client sends `POST /tasks` with a task payload.
2. FastAPI/Pydantic validates it as `TaskCreate`; invalid input returns an automatic 422 response before the handler runs.
3. `create_task` calls `storage.add_task`.
4. Storage generates a UUID, sets UTC `created_at` and `updated_at` timestamps, builds a `TaskResponse`, and saves it in a module-level dictionary.
5. The API returns the created task with HTTP 201.

## 4. Key files

- `app/main.py` — FastAPI application, CORS configuration, health endpoint, and task CRUD routes.
- `app/models.py` — task request/response schemas, status/priority enums, and title validation.
- `app/storage.py` — in-memory task dictionary and CRUD helper functions.
- `app/core/config.py` — imported for `APP_ENV`; implementation is not visible from the files I read.
- `app/business_rules.py` — imported for status-transition validation; implementation is not visible from the files I read.
- `app/schemas/health.py` — imported for the health response schema; implementation is not visible from the files I read.

## 5. Conventions

- **Validation:** unknown fields are forbidden on task schemas; titles are trimmed, cannot be blank, and are limited to 200 characters. Enum fields constrain status and priority.
- **Storage:** a module-level `dict[str, TaskResponse]` provides insertion-ordered in-memory storage; IDs are UUIDs and timestamps use UTC.
- **Error handling:** missing tasks produce HTTP 404 responses; request-model validation produces automatic HTTP 422 responses. Status-transition error behavior is not visible from the files I read.
- **Frontend/backend interaction:** CORS permits `http://localhost:5500` and `http://127.0.0.1:5500`, with GET, POST, PATCH, DELETE, and OPTIONS methods. The frontend implementation is not visible from the files I read.

## 6. Not visible or assumptions

- Authentication, authorization, users, and ownership are not visible from the files I read.
- Persistent database, ORM, migrations, and backup/recovery are not visible from the files I read.
- Deployment, environment configuration behavior beyond the imported `APP_ENV`, logging, tests, API documentation usage, and frontend code are not visible from the files I read.
- Status-transition rules are not visible from the files I read.
