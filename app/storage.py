"""
In-memory storage layer for tasks.
Holds tasks in a module-level dict and exposes CRUD helpers used by the API.
No database or ORM is involved; state is lost when the process restarts.
"""
from datetime import date, datetime, timezone
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
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    title: Optional[str] = None,
    assignee: Optional[str] = None,
    due_date: Optional[date] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if title is not None:
        needle = title.casefold()
        tasks = [task for task in tasks if needle in task.title.casefold()]
    if assignee is not None:
        needle = assignee.casefold()
        tasks = [
            task
            for task in tasks
            if task.assignee is not None and task.assignee.casefold() == needle
        ]
    if due_date is not None:
        tasks = [task for task in tasks if task.due_date == due_date]
    if overdue is True:
        today = date.today()
        tasks = [
            task
            for task in tasks
            if task.due_date < today and task.status != TaskStatus.DONE
        ]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
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
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def _reset() -> None:
    _tasks.clear()
