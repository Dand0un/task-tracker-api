# Task Tracker API — Agent Instructions

## Project summary

Task Tracker API is a small learning REST API for creating, listing, retrieving, updating, and deleting tasks. It uses in-memory storage only, so all task state is lost when the process restarts. The API exposes health and task endpoints, with interactive API documentation at `/docs`.

Sources: `README.md`, `app/main.py`, `app/storage.py`.

## Tech stack

- Python
- FastAPI
- Pydantic v2
- Uvicorn
- python-dotenv
- In-memory Python dictionary storage; no database or ORM is present.

Declared dependencies: `requirements.txt`.

## Confirmed setup and run commands

Create and activate a Windows PowerShell virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install declared dependencies:

```powershell
pip install -r requirements.txt
```

Run the API:

```powershell
uvicorn app.main:app --reload
```

The API is documented as running at `http://127.0.0.1:8000`; health is available at `/health` and Swagger UI at `/docs`.

`python -m app.main` is also supported by `app/main.py`.

## Tests

The repository contains pytest-style tests in `tests/`, so the expected test command is:

```powershell
pytest
```

However, pytest is not declared in `requirements.txt`; a reproducible test-install command is **not confirmed**. Do not claim the test environment is fully specified until the dependency declaration is verified or updated with explicit approval.

## Confirmed business rules

### Task fields and defaults

- `title` is required, is trimmed, must not be blank, and must be at most 200 characters.
- `description` defaults to an empty string.
- `status` values are `ToDo`, `InProgress`, and `Done`; the default is `ToDo`.
- `priority` values are `Low`, `Medium`, and `High`; the default is `Medium`.
- `assignee` is optional.
- `due_date` is optional and, when provided as a string, must be a valid calendar date in `dd/MM/YYYY` format.
- Request models reject undeclared fields.
- Tasks receive UUID string IDs and UTC `created_at` and `updated_at` timestamps.

Sources: `app/models.py`, `app/storage.py`.

### Status transitions

An update that retains the current status is allowed. The allowed status transitions are:

- `ToDo` → `InProgress`
- `InProgress` → `Done`
- `Done` → `InProgress`

Other status transitions return HTTP 422.

Source: `app/business_rules.py`.

### List filtering

`GET /tasks` supports:

- Exact `status` and `priority` filtering.
- Case-insensitive substring matching for `title`.
- Case-insensitive exact matching for `assignee`.
- Exact `due_date` matching.
- `overdue=true`, which returns tasks with a due date before today and a status other than `Done`.

Sources: `app/models.py`, `app/storage.py`.

## Module 5 guardrails

- Treat this module as AI-assisted coding governance and grading work, not feature development.
- Work docs-first: prefer analysis, review notes, evidence, and documentation changes.
- Default to read-only inspection.
- Keep one bounded task per Codex thread.
- Do not modify `app/` unless the user explicitly approves one specific minimal fix.
- Unless explicitly authorized otherwise, restrict edits to `docs/`.
- Before reporting repository facts, inspect and cite the supporting file paths.
- If a command, behavior, or rule is not visible in the repository, mark it **not confirmed**. Do not infer or invent findings.

## Security and governance

- Never paste, expose, log, or commit secrets, tokens, credentials, `.env` contents, or private configuration.
- Do not run destructive commands or irreversible repository operations without explicit user approval and verified targets.
- Preserve existing user changes; do not discard, reset, or overwrite unrelated work.
- Clearly separate confirmed evidence from assumptions, recommendations, and items requiring verification.
- Keep changes narrowly scoped to the task and report the files changed.
