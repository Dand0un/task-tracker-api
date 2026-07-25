"""
Application entry point.
Creates the FastAPI app instance and wires up the /health endpoint.
Run with: uvicorn app.main:app --reload
"""
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_ENV
from app.models import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority
from app import storage
from app.business_rules import validate_status_transition
from app.schemas.health import HealthResponse

# Create the FastAPI application instance.
app = FastAPI(
    title="Task Tracker API",
    description="A learning project REST API for tracking tasks, built with FastAPI.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, status_code=200, tags=["Health"])
def get_health() -> HealthResponse:
    """Health check endpoint.

    Returns a simple status flag and the current UTC timestamp in
    ISO 8601 format, so uptime/monitoring tools can verify the API
    process is alive and responding.

    Returns:
        HealthResponse: `status="ok"` and the current UTC timestamp.

    Example:
        GET /health -> 200 {"status": "ok", "timestamp": "2026-07-26T12:00:00+00:00"}
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload: Task fields to create. Validated against the
            TaskCreate schema by FastAPI/Pydantic before this handler
            runs (e.g. a blank or overlong `title` results in an
            automatic 422 response, never reaching this function).

    Returns:
        TaskResponse: The newly created task, including its generated
        `id` and `created_at`/`updated_at` timestamps.

    Example:
        POST /tasks
        {"title": "Write docs", "priority": "High"}
        -> 201 {"id": "...", "title": "Write docs", "status": "ToDo", ...}
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by status and/or priority.

    Args:
        status: If provided, only tasks with this exact status are
            returned.
        priority: If provided, only tasks with this exact priority are
            returned.

    Returns:
        list[TaskResponse]: Matching tasks. Empty list if none match
        or no tasks exist.

    Example:
        GET /tasks?status=InProgress&priority=High
    """
    return storage.get_all_tasks(status=status, priority=priority)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by id.

    Args:
        task_id: The task's unique id.

    Returns:
        TaskResponse: The matching task.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.

    Example:
        GET /tasks/{task_id}
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task.

    Only fields explicitly set in `payload` are changed; unset fields
    are left as-is. If `payload.status` is set, the task must
    currently exist and the status transition must be valid (see
    `validate_status_transition`).

    [VERIFY] If `payload.status` is not set, a nonexistent `task_id`
    is only caught later via the `storage.update_task` return value,
    not via an explicit existence check up front.

    Args:
        task_id: The task's unique id.
        payload: Fields to update. Unset fields are left unchanged.

    Returns:
        TaskResponse: The updated task.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.
        HTTPException: 422 if `payload.status` is set and the
            transition from the task's current status to it is not
            allowed.

    Example:
        PATCH /tasks/{task_id}
        {"status": "InProgress"}
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing.status, payload.status)

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task by id.

    Args:
        task_id: The task's unique id.

    Returns:
        None.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.

    Example:
        DELETE /tasks/{task_id} -> 204 No Content
    """
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")


# Convenience: allow `python -m app.main` to also start the server,
# in addition to the standard `uvicorn app.main:app --reload` command.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=(APP_ENV == "development"))
