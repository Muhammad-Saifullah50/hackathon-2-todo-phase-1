"""Contract tests for StorageInterface protocol.

These tests verify that any storage implementation conforms to the StorageInterface contract.
"""

from pathlib import Path

import pytest


class TestStorageInterfaceContract:
    """Contract tests that all storage implementations must pass."""

    def test_load_creates_file_if_missing(self, tmp_storage_file: Path) -> None:
        """Test that load() creates the file if it doesn't exist.

        This test will be implemented once we have a concrete storage implementation.
        For now, this is a placeholder for the contract requirement.
        """
        pytest.skip("Waiting for StorageInterface implementation")

    def test_save_atomic_write(self, tmp_storage_file: Path) -> None:
        """Test that save() uses atomic write pattern (temp + rename).

        This test will verify that save operations are atomic to prevent corruption.
        """
        pytest.skip("Waiting for StorageInterface implementation")

    def test_create_backup(self, tmp_storage_file: Path) -> None:
        """Test that create_backup() creates a backup file.

        This test will verify backup functionality works correctly.
        """
        pytest.skip("Waiting for StorageInterface implementation")

    def test_file_path_property(self, tmp_storage_file: Path) -> None:
        """Test that file_path property returns correct path.

        This test will verify the file_path property works correctly.
        """
        pytest.skip("Waiting for StorageInterface implementation")
