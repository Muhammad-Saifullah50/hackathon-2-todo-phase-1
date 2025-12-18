"""Unit tests for Task model."""

import pytest

from src.exceptions import TaskValidationError
from src.models.task import Task


class TestTaskCreation:
    """Tests for Task model creation."""

    def test_create_task_with_all_fields(self) -> None:
        """Test creating a task with all fields."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="Milk, eggs, bread",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        assert task.id == "abc123de"
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.status == "pending"
        assert task.created_at == "2025-12-18 10:00:00"
        assert task.updated_at == "2025-12-18 10:00:00"

    def test_create_task_with_empty_description(self) -> None:
        """Test creating a task with empty description."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        assert task.description == ""

    def test_invalid_title_raises_error(self) -> None:
        """Test that invalid title raises TaskValidationError."""
        with pytest.raises(TaskValidationError, match="Title cannot be empty"):
            Task(
                id="abc123de",
                title="",
                description="",
                status="pending",
                created_at="2025-12-18 10:00:00",
                updated_at="2025-12-18 10:00:00",
            )

    def test_invalid_id_raises_error(self) -> None:
        """Test that invalid ID raises TaskValidationError."""
        with pytest.raises(TaskValidationError, match="Invalid ID format"):
            Task(
                id="invalid",
                title="Buy groceries",
                description="",
                status="pending",
                created_at="2025-12-18 10:00:00",
                updated_at="2025-12-18 10:00:00",
            )

    def test_invalid_status_raises_error(self) -> None:
        """Test that invalid status raises TaskValidationError."""
        with pytest.raises(TaskValidationError, match="Invalid status"):
            Task(
                id="abc123de",
                title="Buy groceries",
                description="",
                status="done",
                created_at="2025-12-18 10:00:00",
                updated_at="2025-12-18 10:00:00",
            )

    def test_invalid_timestamp_raises_error(self) -> None:
        """Test that invalid timestamp raises TaskValidationError."""
        with pytest.raises(TaskValidationError, match="Invalid timestamp format"):
            Task(
                id="abc123de",
                title="Buy groceries",
                description="",
                status="pending",
                created_at="invalid",
                updated_at="2025-12-18 10:00:00",
            )


class TestTaskToDictMethod:
    """Tests for Task.to_dict() method."""

    def test_to_dict_returns_all_fields(self) -> None:
        """Test that to_dict returns dictionary with all fields."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="Milk, eggs, bread",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        result = task.to_dict()

        assert result == {
            "id": "abc123de",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "status": "pending",
            "created_at": "2025-12-18 10:00:00",
            "updated_at": "2025-12-18 10:00:00",
        }

    def test_to_dict_with_empty_description(self) -> None:
        """Test to_dict with empty description."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        result = task.to_dict()

        assert result["description"] == ""


class TestTaskFromDictMethod:
    """Tests for Task.from_dict() method."""

    def test_from_dict_creates_task(self) -> None:
        """Test that from_dict creates a valid Task instance."""
        data = {
            "id": "abc123de",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "status": "pending",
            "created_at": "2025-12-18 10:00:00",
            "updated_at": "2025-12-18 10:00:00",
        }

        task = Task.from_dict(data)

        assert task.id == "abc123de"
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.status == "pending"
        assert task.created_at == "2025-12-18 10:00:00"
        assert task.updated_at == "2025-12-18 10:00:00"

    def test_from_dict_validates_data(self) -> None:
        """Test that from_dict validates the input data."""
        data = {
            "id": "invalid",
            "title": "Buy groceries",
            "description": "",
            "status": "pending",
            "created_at": "2025-12-18 10:00:00",
            "updated_at": "2025-12-18 10:00:00",
        }

        with pytest.raises(TaskValidationError, match="Invalid ID format"):
            Task.from_dict(data)


class TestMarkCompletedMethod:
    """Tests for Task.mark_completed() method."""

    def test_mark_completed_changes_status(self) -> None:
        """Test that mark_completed changes status to 'completed'."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        task.mark_completed()

        assert task.status == "completed"

    def test_mark_completed_updates_timestamp(self) -> None:
        """Test that mark_completed updates the updated_at timestamp."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        initial_updated_at = task.updated_at
        task.mark_completed()

        assert task.updated_at != initial_updated_at


class TestMarkPendingMethod:
    """Tests for Task.mark_pending() method."""

    def test_mark_pending_changes_status(self) -> None:
        """Test that mark_pending changes status to 'pending'."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="completed",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 11:00:00",
        )

        task.mark_pending()

        assert task.status == "pending"

    def test_mark_pending_updates_timestamp(self) -> None:
        """Test that mark_pending updates the updated_at timestamp."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="completed",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 11:00:00",
        )

        initial_updated_at = task.updated_at
        task.mark_pending()

        assert task.updated_at != initial_updated_at


class TestUpdateTitleMethod:
    """Tests for Task.update_title() method."""

    def test_update_title_changes_title(self) -> None:
        """Test that update_title changes the task title."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        task.update_title("Buy vegetables")

        assert task.title == "Buy vegetables"

    def test_update_title_strips_whitespace(self) -> None:
        """Test that update_title strips leading/trailing whitespace."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        task.update_title("  Buy vegetables  ")

        assert task.title == "Buy vegetables"

    def test_update_title_validates_new_title(self) -> None:
        """Test that update_title validates the new title."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        with pytest.raises(TaskValidationError, match="Title cannot be empty"):
            task.update_title("")

    def test_update_title_updates_timestamp(self) -> None:
        """Test that update_title updates the updated_at timestamp."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        initial_updated_at = task.updated_at
        task.update_title("Buy vegetables")

        assert task.updated_at != initial_updated_at


class TestUpdateDescriptionMethod:
    """Tests for Task.update_description() method."""

    def test_update_description_changes_description(self) -> None:
        """Test that update_description changes the task description."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="Milk, eggs",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        task.update_description("Milk, eggs, bread, butter")

        assert task.description == "Milk, eggs, bread, butter"

    def test_update_description_allows_empty_string(self) -> None:
        """Test that update_description allows empty string."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="Milk, eggs",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        task.update_description("")

        assert task.description == ""

    def test_update_description_validates_new_description(self) -> None:
        """Test that update_description validates the new description."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        with pytest.raises(TaskValidationError, match="Description too long"):
            task.update_description("a" * 501)

    def test_update_description_updates_timestamp(self) -> None:
        """Test that update_description updates the updated_at timestamp."""
        task = Task(
            id="abc123de",
            title="Buy groceries",
            description="Milk, eggs",
            status="pending",
            created_at="2025-12-18 10:00:00",
            updated_at="2025-12-18 10:00:00",
        )

        initial_updated_at = task.updated_at
        task.update_description("Milk, eggs, bread")

        assert task.updated_at != initial_updated_at
