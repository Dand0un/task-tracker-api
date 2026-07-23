"""
Application entry point.
Creates the FastAPI app instance and wires up the /health endpoint.
Run with: uvicorn app.main:app --reload
"""
from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_ENV
from app.models import TaskCreate, TaskFilter, TaskResponse, TaskUpdate
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
    """
    Health check endpoint.
    Returns a simple status flag and the current UTC timestamp in
    ISO 8601 format, so uptime/monitoring tools can verify the API
    process is alive and responding.
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(filters: Annotated[TaskFilter, Depends()]) -> list[TaskResponse]:
    return storage.get_all_tasks(**filters.model_dump(exclude_none=True))


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
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
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")


# Convenience: allow `python -m app.main` to also start the server,
# in addition to the standard `uvicorn app.main:app --reload` command.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=(APP_ENV == "development"))
