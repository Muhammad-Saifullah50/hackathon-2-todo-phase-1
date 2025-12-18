"""Task data model for CLI Todo application."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.services.validators import (
    TIMESTAMP_FORMAT,
    validate_description,
    validate_id,
    validate_status,
    validate_timestamp,
    validate_title,
)


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: 8-character unique hexadecimal identifier
        title: 1-10 words describing the task
        description: Optional details (0-500 characters)
        status: Current status ("pending" or "completed")
        created_at: ISO 8601 timestamp when task was created
        updated_at: ISO 8601 timestamp when task was last modified
    """

    id: str
    title: str
    description: str
    status: str
    created_at: str
    updated_at: str

    def __post_init__(self) -> None:
        """Validate all fields after initialization."""
        validate_id(self.id)
        validate_title(self.title)
        validate_description(self.description)
        validate_status(self.status)
        validate_timestamp(self.created_at)
        validate_timestamp(self.updated_at)

        # Strip title whitespace
        self.title = self.title.strip()

    def to_dict(self) -> dict[str, Any]:
        """Convert Task to dictionary for JSON serialization.

        Returns:
            Dictionary with all task fields
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Create Task instance from dictionary.

        Args:
            data: Dictionary with task fields

        Returns:
            Task instance

        Raises:
            TaskValidationError: If any field is invalid
        """
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            status=data["status"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    def mark_completed(self) -> None:
        """Mark task as completed and update timestamp."""
        self.status = "completed"
        self.updated_at = self._current_timestamp()

    def mark_pending(self) -> None:
        """Mark task as pending and update timestamp."""
        self.status = "pending"
        self.updated_at = self._current_timestamp()

    def update_title(self, new_title: str) -> None:
        """Update task title with validation.

        Args:
            new_title: New title for the task

        Raises:
            TaskValidationError: If new title is invalid
        """
        validate_title(new_title)
        self.title = new_title.strip()
        self.updated_at = self._current_timestamp()

    def update_description(self, new_description: str) -> None:
        """Update task description with validation.

        Args:
            new_description: New description for the task

        Raises:
            TaskValidationError: If new description is invalid
        """
        validate_description(new_description)
        self.description = new_description
        self.updated_at = self._current_timestamp()

    def _current_timestamp(self) -> str:
        """Generate current timestamp in ISO 8601 format.

        Returns:
            Formatted timestamp string (YYYY-MM-DD HH:MM:SS)
        """
        return datetime.now().strftime(TIMESTAMP_FORMAT)
