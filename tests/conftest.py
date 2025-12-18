"""Pytest fixtures for CLI Todo application tests."""

from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest


@pytest.fixture
def tmp_storage_file(tmp_path: Path) -> Path:
    """Provide a temporary storage file path for tests.

    Args:
        tmp_path: Pytest's temporary directory fixture

    Returns:
        Path to temporary tasks.json file
    """
    return tmp_path / "tasks.json"


@pytest.fixture
def mock_storage() -> Mock:
    """Provide a mock storage object for unit tests.

    Returns:
        Mock storage with load() and save() methods
    """
    storage = Mock()
    storage.load.return_value = {"tasks": {}, "metadata": {"version": "1.0.0"}}
    storage.save.return_value = None
    storage.file_path = Path("tasks.json")
    return storage


@pytest.fixture
def sample_tasks() -> dict[str, Any]:
    """Provide sample task data for tests.

    Returns:
        Dictionary with sample tasks in storage format
    """
    return {
        "tasks": {
            "abc123de": {
                "id": "abc123de",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "status": "pending",
                "created_at": "2025-12-18 10:00:00",
                "updated_at": "2025-12-18 10:00:00",
            },
            "def456gh": {
                "id": "def456gh",
                "title": "Write report",
                "description": "Q4 financial summary",
                "status": "completed",
                "created_at": "2025-12-18 09:00:00",
                "updated_at": "2025-12-18 11:00:00",
            },
            "ghi789jk": {
                "id": "ghi789jk",
                "title": "Team meeting",
                "description": "",
                "status": "pending",
                "created_at": "2025-12-18 08:00:00",
                "updated_at": "2025-12-18 08:00:00",
            },
        },
        "metadata": {"version": "1.0.0"},
    }
