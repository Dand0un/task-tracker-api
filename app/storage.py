"""
In-memory storage layer for tasks.
Holds tasks in a module-level dict and exposes CRUD helpers used by the API.
No database or ORM is involved; state is lost when the process restarts.
"""
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and persist a new task from validated input.

    Args:
        payload: Validated task-creation data.

    Returns:
        TaskResponse: The stored task, with a generated `id` and
        `created_at`/`updated_at` set to the current UTC time.
        `description` defaults to an empty string if not provided.
    """
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    """Return all stored tasks, optionally filtered.

    Args:
        status: If provided, only tasks with this exact status are
            included.
        priority: If provided, only tasks with this exact priority are
            included.

    Returns:
        list[TaskResponse]: Matching tasks, in insertion order. Empty
        list if none match or no tasks exist.
    """
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Look up a single task by id.

    Args:
        task_id: The task's unique id.

    Returns:
        Optional[TaskResponse]: The matching task, or None if no task
        with `task_id` exists.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply a partial update to a stored task.

    Only fields explicitly set on `payload` are applied; unset fields
    are left unchanged. If `payload` has no fields set, the existing
    task is returned unchanged (its `updated_at` is not modified).

    Args:
        task_id: The task's unique id.
        payload: Fields to update.

    Returns:
        Optional[TaskResponse]: The updated task, or None if no task
        with `task_id` exists. When at least one field changes,
        `updated_at` is set to the current UTC time.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        return task

    updated = task.model_copy(update=changes)
    updated.updated_at = datetime.now(timezone.utc)
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: str) -> bool:
    """Delete a task by id.

    Args:
        task_id: The task's unique id.

    Returns:
        bool: True if a task was deleted, False if no task with
        `task_id` existed.
    """
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def _reset() -> None:
    _tasks.clear()
