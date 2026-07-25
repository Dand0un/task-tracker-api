"""
Business rules for tasks.
Encodes the allowed status transitions and validation used by the API layer.
"""
from fastapi import HTTPException, status

from app.models import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Validate that a task status transition is allowed.

    A transition to the same status is always a no-op and allowed.
    Any other transition must be present in VALID_TRANSITIONS.

    Args:
        current: The task's current status.
        new: The requested new status.

    Returns:
        None.

    Raises:
        HTTPException: 422 Unprocessable Entity if the transition from
            `current` to `new` is not in VALID_TRANSITIONS.
    """
    if current == new:
        return

    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )
