"""Custom exception classes for CLI Todo application."""


class TaskValidationError(ValueError):
    """Raised when task data validation fails (title, description, status, etc.)."""

    pass


class StorageError(Exception):
    """Raised when storage operations fail (load, save, backup)."""

    pass


class TaskNotFoundError(KeyError):
    """Raised when a task with the given ID does not exist."""

    pass


class FilePermissionError(PermissionError):
    """Raised when file permissions prevent read/write operations."""

    pass


class FileCorruptionError(Exception):
    """Raised when JSON file is corrupted or has invalid schema."""

    pass


class TerminalError(Exception):
    """Raised when terminal requirements are not met (e.g., too narrow)."""

    pass


class PaginationError(ValueError):
    """Raised when pagination parameters are invalid."""

    pass


class ValidationError(ValueError):
    """Raised when general input validation fails."""

    pass
