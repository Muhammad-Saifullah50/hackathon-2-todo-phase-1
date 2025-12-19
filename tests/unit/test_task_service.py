"""Unit tests for TaskService."""

import pytest

from src.exceptions import TaskNotFoundError, TaskValidationError


class TestTaskServiceAddTask:
    """Tests for TaskService.add_task() method."""

    def test_add_task_generates_unique_id(self, mock_storage) -> None:
        """Test that add_task() generates a unique 8-char hex ID."""
        pytest.skip("Waiting for TaskService implementation")

    def test_add_task_sets_timestamps(self, mock_storage) -> None:
        """Test that add_task() sets created_at and updated_at timestamps."""
        pytest.skip("Waiting for TaskService implementation")

    def test_add_task_validates_title(self, mock_storage) -> None:
        """Test that add_task() validates title (empty should fail)."""
        pytest.skip("Waiting for TaskService implementation")

    def test_add_task_validates_description(self, mock_storage) -> None:
        """Test that add_task() validates description (>500 chars should fail)."""
        pytest.skip("Waiting for TaskService implementation")

    def test_add_task_strips_title_whitespace(self, mock_storage) -> None:
        """Test that add_task() strips leading/trailing whitespace from title."""
        pytest.skip("Waiting for TaskService implementation")

    def test_add_task_saves_to_storage(self, mock_storage) -> None:
        """Test that add_task() calls storage.save()."""
        pytest.skip("Waiting for TaskService implementation")

    def test_add_task_returns_task_object(self, mock_storage) -> None:
        """Test that add_task() returns a Task object."""
        pytest.skip("Waiting for TaskService implementation")

    def test_add_task_collision_detection(self, mock_storage) -> None:
        """Test that add_task() handles UUID collision by regenerating."""
        pytest.skip("Waiting for TaskService implementation")


class TestTaskServiceGetAllTasks:
    """Tests for TaskService.get_all_tasks() method."""

    def test_get_all_tasks_empty(self, mock_storage) -> None:
        """Test that get_all_tasks() returns empty list when no tasks exist."""
        pytest.skip("Waiting for TaskService implementation")

    def test_get_all_tasks_sorted_newest_first(self, mock_storage) -> None:
        """Test that get_all_tasks() returns tasks sorted by created_at (newest first)."""
        pytest.skip("Waiting for TaskService implementation")

    def test_get_all_tasks_returns_task_objects(self, mock_storage) -> None:
        """Test that get_all_tasks() returns list of Task objects."""
        pytest.skip("Waiting for TaskService implementation")


class TestTaskServiceGetTask:
    """Tests for TaskService.get_task() method."""

    def test_get_task_returns_task(self, mock_storage) -> None:
        """Test that get_task() returns the correct task by ID."""
        pytest.skip("Waiting for TaskService implementation")

    def test_get_task_nonexistent_returns_none(self, mock_storage) -> None:
        """Test that get_task() returns None for nonexistent task."""
        pytest.skip("Waiting for TaskService implementation")

    def test_get_task_validates_id_format(self, mock_storage) -> None:
        """Test that get_task() validates ID format."""
        pytest.skip("Waiting for TaskService implementation")


class TestTaskServiceUpdateTask:
    """Tests for TaskService.update_task() method."""

    def test_update_title_only(self, mock_storage) -> None:
        """Test updating only the title."""
        pytest.skip("Waiting for update_task implementation")

    def test_update_description_only(self, mock_storage) -> None:
        """Test updating only the description."""
        pytest.skip("Waiting for update_task implementation")

    def test_update_both(self, mock_storage) -> None:
        """Test updating both title and description."""
        pytest.skip("Waiting for update_task implementation")

    def test_update_nonexistent_task_raises_error(self, mock_storage) -> None:
        """Test that updating nonexistent task raises TaskNotFoundError."""
        pytest.skip("Waiting for update_task implementation")

    def test_update_empty_title_raises_error(self, mock_storage) -> None:
        """Test that updating with empty title raises TaskValidationError."""
        pytest.skip("Waiting for update_task implementation")
