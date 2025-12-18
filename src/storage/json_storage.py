"""JSON file storage implementation with atomic writes."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from src.exceptions import FileCorruptionError, StorageError


class JSONStorage:
    """JSON file-based storage with atomic write operations.

    Uses temp file + rename pattern for atomic writes to prevent corruption.
    """

    def __init__(self, file_path: Path) -> None:
        """Initialize JSON storage.

        Args:
            file_path: Path to JSON storage file
        """
        self._file_path = file_path

    @property
    def file_path(self) -> Path:
        """Get the storage file path.

        Returns:
            Path to storage file
        """
        return self._file_path

    def load(self) -> dict[str, Any]:
        """Load data from JSON file.

        If file doesn't exist, creates it with default structure.
        If file is corrupted, creates backup and returns default structure.

        Returns:
            Dictionary with tasks and metadata

        Raises:
            FileCorruptionError: If JSON is invalid and cannot be recovered
        """
        # Create file with default structure if it doesn't exist
        if not self._file_path.exists():
            default_data = self._default_structure()
            self.save(default_data)
            return default_data

        try:
            with open(self._file_path, encoding="utf-8") as f:
                data = json.load(f)

            # Validate schema
            self._validate_schema(data)

            return data

        except json.JSONDecodeError as e:
            # Create backup of corrupted file
            self.create_backup()
            raise FileCorruptionError(
                f"JSON file corrupted: {e}. Backup created at {self._file_path}.backup"
            ) from e

        except OSError as e:
            raise StorageError(f"Failed to load storage file: {e}") from e

    def save(self, data: dict[str, Any]) -> None:
        """Save data to JSON file using atomic write pattern.

        Uses temp file + rename for atomicity to prevent corruption.

        Args:
            data: Dictionary with tasks and metadata

        Raises:
            StorageError: If save operation fails
        """
        try:
            # Ensure parent directory exists
            self._file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to temporary file first
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self._file_path.parent, suffix=".tmp"
            )

            try:
                with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                # Atomic rename
                os.replace(temp_path, self._file_path)

                # Set file permissions to user read/write only (600)
                os.chmod(self._file_path, 0o600)

            except Exception:
                # Clean up temp file if something went wrong
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                raise

        except OSError as e:
            raise StorageError(f"Failed to save storage file: {e}") from e

    def create_backup(self) -> Path | None:
        """Create a backup of the current storage file.

        Returns:
            Path to backup file, or None if no file exists

        Raises:
            StorageError: If backup operation fails
        """
        if not self._file_path.exists():
            return None

        backup_path = Path(str(self._file_path) + ".backup")

        try:
            import shutil

            shutil.copy2(self._file_path, backup_path)
            return backup_path

        except OSError as e:
            raise StorageError(f"Failed to create backup: {e}") from e

    def _default_structure(self) -> dict[str, Any]:
        """Get default storage structure.

        Returns:
            Dictionary with empty tasks and metadata
        """
        return {"tasks": {}, "metadata": {"version": "1.0.0"}}

    def _validate_schema(self, data: dict[str, Any]) -> None:
        """Validate JSON schema.

        Args:
            data: Data to validate

        Raises:
            FileCorruptionError: If schema is invalid
        """
        if not isinstance(data, dict):
            raise FileCorruptionError("Storage data must be a dictionary")

        if "tasks" not in data:
            raise FileCorruptionError("Storage data missing 'tasks' key")

        if "metadata" not in data:
            raise FileCorruptionError("Storage data missing 'metadata' key")

        if not isinstance(data["tasks"], dict):
            raise FileCorruptionError("'tasks' must be a dictionary")

        if not isinstance(data["metadata"], dict):
            raise FileCorruptionError("'metadata' must be a dictionary")
