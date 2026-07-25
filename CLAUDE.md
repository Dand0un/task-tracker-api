# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Task Tracker API — a learning project REST API for tracking tasks, built with FastAPI + Pydantic v2. Storage is a plain in-memory dict (`app/storage.py`); there is no database or ORM, so all state is lost on process restart. A static HTML/JS frontend (`app/frontend/index.html`) consumes the API directly.

## Commands

```powershell
# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env

# Run the dev server (reload enabled)
uvicorn app.main:app --reload

# Run all tests
pytest

# Run a single test
pytest tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422
```

The API runs at `http://127.0.0.1:8000`; interactive docs at `/docs`. `pytest.ini` sets `pythonpath = .` so `from app...` imports resolve without installing the package.

## Architecture

Everything currently lives in a flat set of modules under `app/`, not the `app/api`, `app/repositories`, `app/schemas`, `app/services` subpackages (those exist but are empty scaffolding, unused):

- `app/main.py` — the single FastAPI app instance and all route handlers (`/health`, `/tasks` CRUD). Routes call directly into `app/storage.py` and `app/business_rules.py`; there is no router/service layer indirection yet.
- `app/models.py` — Pydantic models/enums shared across the app: `TaskStatus`, `TaskPriority`, `TaskCreate`, `TaskUpdate`, `TaskResponse`, `TaskFilter`. Validation (title length/blank, due-date parsing/format) lives in field validators here, not in route handlers.
- `app/business_rules.py` — status transition state machine (`VALID_TRANSITIONS`). `TaskStatus` transitions are constrained: `ToDo -> InProgress -> Done -> InProgress`; anything else raises `HTTPException(422)`. This is enforced in `main.update_task` before calling storage.
- `app/storage.py` — module-level `_tasks: dict[str, TaskResponse]` plus CRUD + filtering functions (`add_task`, `get_all_tasks`, `get_task_by_id`, `update_task`, `delete_task`). `get_all_tasks` implements all query-filter semantics (status/priority exact match, title/assignee case-insensitive match, `overdue` = due_date in the past and status != Done). `_reset()` clears state and is used by tests, not production code.
- `app/core/config.py` — loads `.env` via `python-dotenv`, exposes `PORT` and `APP_ENV`.
- `app/schemas/health.py` — response schema for `/health`.

### Due dates

Due dates are transported as strings in `dd/MM/yyyy` format (not ISO), both on input (`TaskCreate`/`TaskUpdate`/`TaskFilter` validators call `_parse_due_date`/`_validate_due_date` in `app/models.py`) and on output (`TaskResponse.serialize_due_date`). New due dates must be strictly in the future (`> date.today()`) on create/update; this rule is not applied when filtering (`TaskFilter` just parses the date).

### Tests

`tests/conftest.py` provides a `client` fixture (`TestClient(app)`) and a `created_task` fixture (a task created with a due date 7 days out). An autouse fixture calls `storage._reset()` before and after every test, so tests don't need to manage state isolation manually. All tests live in `tests/test_tasks.py`.
