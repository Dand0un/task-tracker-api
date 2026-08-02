"""
Pydantic v2 models and enums for the Task Tracker API (in-memory module).
Defines task status/priority enums plus the create/update/response schemas.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


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


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Validate and normalize the `title` field.

        Args:
            value: The raw title string.

        Returns:
            str: The title with leading/trailing whitespace stripped.

        Raises:
            ValueError: If the stripped title is empty, or longer than
                200 characters.
        """
        return _validate_title(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        """Validate and normalize the `title` field when provided.

        Args:
            value: The raw title string, or the raw value supplied for
                the field in the request payload.

        Returns:
            Optional[str]: The title with leading/trailing whitespace
            stripped when a non-null string is provided.

        Raises:
            ValueError: If `value` is `None` (explicit null), or if the
                stripped title is empty, or longer than 200 characters.
        """
        if value is None:
            raise ValueError("Title must not be null.")
        return _validate_title(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    created_at: datetime
    updated_at: datetime
