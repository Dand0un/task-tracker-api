"""
Pydantic v2 models and enums for the Task Tracker API (in-memory module).
Defines task status/priority enums plus the create/update/response schemas.
"""
from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator

_DUE_DATE_FORMAT = "%d/%m/%Y"


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def _validate_title(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("Title must not be blank.")
    if len(stripped) > 200:
        raise ValueError("Title must be at most 200 characters.")
    return stripped


def _validate_due_date(value: object) -> date:
    if isinstance(value, datetime):
        parsed = value.date()
    elif isinstance(value, date):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = datetime.strptime(value, _DUE_DATE_FORMAT).date()
        except ValueError as exc:
            raise ValueError(
                "due_date must be a valid calendar date in dd/MM/yyyy format."
            ) from exc
    else:
        raise ValueError(
            "due_date must be a valid calendar date in dd/MM/yyyy format."
        )

    if parsed <= date.today():
        raise ValueError("due_date must be greater than now.")
    return parsed


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: date

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return _validate_title(value)

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, value: object) -> date:
        return _validate_due_date(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _validate_title(value)

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, value: object) -> Optional[date]:
        if value is None:
            return None
        return _validate_due_date(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: date
    created_at: datetime
    updated_at: datetime

    @field_serializer("due_date")
    def serialize_due_date(self, value: date) -> str:
        return value.strftime(_DUE_DATE_FORMAT)


class TaskFilter(BaseModel):
    """Query filters for listing tasks (in-memory).

    Matching semantics when applied:
    - status / priority: exact enum match
    - title: case-insensitive substring match on task.title
    - assignee: case-insensitive exact match on task.assignee
    - due_date: exact match (task.due_date == due_date)
    - overdue: when True, task.due_date < date.today() and status != Done
    """

    model_config = ConfigDict(extra="forbid")

    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    title: Optional[str] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    overdue: Optional[bool] = None
