"""Storage interface protocol for CLI Todo application."""

from pathlib import Path
from typing import Any, Protocol


class StorageInterface(Protocol):
    """Protocol defining the storage contract.

    Any storage implementation must conform to this interface.
    """

    def load(self) -> dict[str, Any]:
        """Load data from storage.

        Returns:
            Dictionary with tasks and metadata

        Raises:
            FileCorruptionError: If data is corrupted
            StorageError: If load operation fails
        """
        ...

    def save(self, data: dict[str, Any]) -> None:
        """Save data to storage using atomic write.

        Args:
            data: Dictionary with tasks and metadata

        Raises:
            StorageError: If save operation fails
        """
        ...

    def create_backup(self) -> Path | None:
        """Create a backup of the current storage file.

        Returns:
            Path to backup file, or None if no file exists

        Raises:
            StorageError: If backup operation fails
        """
        ...

    @property
    def file_path(self) -> Path:
        """Get the storage file path.

        Returns:
            Path to storage file
        """
        ...
