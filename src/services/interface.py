"""Task service interface protocol."""

from typing import Protocol

from src.models.task import Task


class TaskServiceInterface(Protocol):
    """Protocol defining the task service contract."""

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task.

        Args:
            title: Task title (1-10 words)
            description: Optional task description (0-500 chars)

        Returns:
            Created Task object

        Raises:
            TaskValidationError: If title or description is invalid
        """
        ...

    def get_task(self, task_id: str) -> Task | None:
        """Get a task by ID.

        Args:
            task_id: 8-character hex task ID

        Returns:
            Task object if found, None otherwise

        Raises:
            TaskValidationError: If task_id format is invalid
        """
        ...

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks sorted by created_at (newest first).

        Returns:
            List of Task objects
        """
        ...

    def update_task(
        self, task_id: str, new_title: str | None = None, new_description: str | None = None
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: 8-character hex task ID
            new_title: Optional new title
            new_description: Optional new description

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
            TaskValidationError: If new values are invalid
        """
        ...

    def mark_completed(self, task_id: str) -> Task:
        """Mark a task as completed.

        Args:
            task_id: 8-character hex task ID

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        ...

    def mark_pending(self, task_id: str) -> Task:
        """Mark a task as pending.

        Args:
            task_id: 8-character hex task ID

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        ...

    def mark_tasks_completed(self, task_ids: list[str]) -> list[Task]:
        """Mark multiple tasks as completed (bulk operation).

        Args:
            task_ids: List of task IDs

        Returns:
            List of updated Task objects

        Raises:
            TaskNotFoundError: If any task doesn't exist
        """
        ...

    def mark_tasks_pending(self, task_ids: list[str]) -> list[Task]:
        """Mark multiple tasks as pending (bulk operation).

        Args:
            task_ids: List of task IDs

        Returns:
            List of updated Task objects

        Raises:
            TaskNotFoundError: If any task doesn't exist
        """
        ...

    def filter_by_status(self, status: str) -> list[Task]:
        """Filter tasks by status.

        Args:
            status: "pending" or "completed"

        Returns:
            List of Task objects matching the status

        Raises:
            TaskValidationError: If status is invalid
        """
        ...

    def delete_task(self, task_id: str) -> bool:
        """Delete a single task.

        Args:
            task_id: 8-character hex task ID

        Returns:
            True if task was deleted, False if not found
        """
        ...

    def delete_tasks(self, task_ids: list[str]) -> int:
        """Delete multiple tasks (bulk operation).

        Args:
            task_ids: List of task IDs

        Returns:
            Number of tasks successfully deleted
        """
        ...

    def paginate(self, tasks: list[Task], page: int, page_size: int = 10) -> list[Task]:
        """Paginate a list of tasks.

        Args:
            tasks: List of tasks to paginate
            page: Zero-indexed page number
            page_size: Number of tasks per page (default: 10)

        Returns:
            List of tasks for the specified page
        """
        ...

    def count_tasks(self) -> dict[str, int]:
        """Count tasks by status.

        Returns:
            Dictionary with counts: {"total": int, "pending": int, "completed": int}
        """
        ...
