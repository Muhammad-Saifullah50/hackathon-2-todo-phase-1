"""Task service implementation with business logic."""

import uuid
from datetime import datetime

from src.models.task import Task
from src.services.validators import TIMESTAMP_FORMAT, validate_id
from src.storage.interface import StorageInterface


class TaskService:
    """Service layer for task management operations."""

    def __init__(self, storage: StorageInterface) -> None:
        """Initialize task service.

        Args:
            storage: Storage implementation conforming to StorageInterface
        """
        self._storage = storage

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
        # Load existing tasks to check for ID collision
        data = self._storage.load()
        existing_ids = set(data["tasks"].keys())

        # Generate unique ID
        task_id = self._generate_unique_id(existing_ids)

        # Generate timestamps
        now = self._current_timestamp()

        # Create task (validation happens in __post_init__)
        task = Task(
            id=task_id,
            title=title,
            description=description,
            status="pending",
            created_at=now,
            updated_at=now,
        )

        # Save to storage
        data["tasks"][task_id] = task.to_dict()
        self._storage.save(data)

        return task

    def get_task(self, task_id: str) -> Task | None:
        """Get a task by ID.

        Args:
            task_id: 8-character hex task ID

        Returns:
            Task object if found, None otherwise

        Raises:
            TaskValidationError: If task_id format is invalid
        """
        validate_id(task_id)

        data = self._storage.load()

        if task_id not in data["tasks"]:
            return None

        return Task.from_dict(data["tasks"][task_id])

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks sorted by created_at (newest first).

        Returns:
            List of Task objects
        """
        data = self._storage.load()

        tasks = [Task.from_dict(task_data) for task_data in data["tasks"].values()]

        # Sort by created_at descending (newest first)
        tasks.sort(key=lambda t: t.created_at, reverse=True)

        return tasks

    def _generate_unique_id(self, existing_ids: set[str]) -> str:
        """Generate a unique 8-character hex ID.

        Uses UUID4 and slices to 8 characters. Handles collisions by regenerating.

        Args:
            existing_ids: Set of existing task IDs

        Returns:
            Unique 8-character hex ID
        """
        while True:
            task_id = uuid.uuid4().hex[:8]
            if task_id not in existing_ids:
                return task_id

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
        from src.exceptions import TaskNotFoundError

        validate_id(task_id)

        # Load current data
        data = self._storage.load()

        if task_id not in data["tasks"]:
            raise TaskNotFoundError(f"Task not found: {task_id}")

        # Get task
        task = Task.from_dict(data["tasks"][task_id])

        # Update fields
        if new_title is not None:
            task.update_title(new_title)

        if new_description is not None:
            task.update_description(new_description)

        # Save updated task
        data["tasks"][task_id] = task.to_dict()
        self._storage.save(data)

        return task

    def mark_completed(self, task_id: str) -> Task:
        """Mark a task as completed."""
        from src.exceptions import TaskNotFoundError

        validate_id(task_id)
        data = self._storage.load()

        if task_id not in data["tasks"]:
            raise TaskNotFoundError(f"Task not found: {task_id}")

        task = Task.from_dict(data["tasks"][task_id])
        task.mark_completed()

        data["tasks"][task_id] = task.to_dict()
        self._storage.save(data)

        return task

    def mark_pending(self, task_id: str) -> Task:
        """Mark a task as pending."""
        from src.exceptions import TaskNotFoundError

        validate_id(task_id)
        data = self._storage.load()

        if task_id not in data["tasks"]:
            raise TaskNotFoundError(f"Task not found: {task_id}")

        task = Task.from_dict(data["tasks"][task_id])
        task.mark_pending()

        data["tasks"][task_id] = task.to_dict()
        self._storage.save(data)

        return task

    def mark_tasks_completed(self, task_ids: list[str]) -> list[Task]:
        """Mark multiple tasks as completed (bulk operation)."""
        from src.exceptions import TaskNotFoundError

        data = self._storage.load()
        updated_tasks = []

        for task_id in task_ids:
            validate_id(task_id)
            if task_id not in data["tasks"]:
                raise TaskNotFoundError(f"Task not found: {task_id}")

            task = Task.from_dict(data["tasks"][task_id])
            task.mark_completed()
            data["tasks"][task_id] = task.to_dict()
            updated_tasks.append(task)

        # Save once after all updates
        self._storage.save(data)
        return updated_tasks

    def mark_tasks_pending(self, task_ids: list[str]) -> list[Task]:
        """Mark multiple tasks as pending (bulk operation)."""
        from src.exceptions import TaskNotFoundError

        data = self._storage.load()
        updated_tasks = []

        for task_id in task_ids:
            validate_id(task_id)
            if task_id not in data["tasks"]:
                raise TaskNotFoundError(f"Task not found: {task_id}")

            task = Task.from_dict(data["tasks"][task_id])
            task.mark_pending()
            data["tasks"][task_id] = task.to_dict()
            updated_tasks.append(task)

        # Save once after all updates
        self._storage.save(data)
        return updated_tasks

    def filter_by_status(self, status: str) -> list[Task]:
        """Filter tasks by status."""
        from src.services.validators import validate_status

        validate_status(status)
        data = self._storage.load()

        tasks = [
            Task.from_dict(task_data)
            for task_data in data["tasks"].values()
            if task_data["status"] == status
        ]

        # Sort by created_at descending
        tasks.sort(key=lambda t: t.created_at, reverse=True)
        return tasks

    def delete_task(self, task_id: str) -> bool:
        """Delete a single task."""
        validate_id(task_id)
        data = self._storage.load()

        if task_id not in data["tasks"]:
            return False

        del data["tasks"][task_id]
        self._storage.save(data)
        return True

    def delete_tasks(self, task_ids: list[str]) -> int:
        """Delete multiple tasks (bulk operation)."""
        data = self._storage.load()
        deleted_count = 0

        for task_id in task_ids:
            validate_id(task_id)
            if task_id in data["tasks"]:
                del data["tasks"][task_id]
                deleted_count += 1

        # Save once after all deletions
        self._storage.save(data)
        return deleted_count

    def paginate(self, tasks: list[Task], page: int, page_size: int = 10) -> list[Task]:
        """Paginate a list of tasks."""
        start = page * page_size
        end = start + page_size
        return tasks[start:end]

    def count_tasks(self) -> dict[str, int]:
        """Count tasks by status."""
        data = self._storage.load()

        total = len(data["tasks"])
        pending = sum(1 for t in data["tasks"].values() if t["status"] == "pending")
        completed = sum(1 for t in data["tasks"].values() if t["status"] == "completed")

        return {
            "total": total,
            "pending": pending,
            "completed": completed,
        }

    def _current_timestamp(self) -> str:
        """Generate current timestamp in ISO 8601 format.

        Returns:
            Formatted timestamp string (YYYY-MM-DD HH:MM:SS)
        """
        return datetime.now().strftime(TIMESTAMP_FORMAT)
