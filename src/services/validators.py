"""Input validation functions and constants for CLI Todo application."""

import re
from datetime import datetime
from typing import Final

from src.exceptions import (
    PaginationError,
    TaskValidationError,
    TerminalError,
    ValidationError,
)

# Validation constants
MAX_TITLE_WORDS: Final[int] = 10
MAX_DESCRIPTION_CHARS: Final[int] = 500
ID_LENGTH: Final[int] = 8
ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{8}$")
ALLOWED_STATUSES: Final[set[str]] = {"pending", "completed"}
TIMESTAMP_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
MIN_TERMINAL_WIDTH: Final[int] = 80


def validate_title(title: str) -> None:
    """Validate task title.

    Rules:
    - Not empty after stripping whitespace
    - 1-10 words (space-separated)
    - Leading/trailing whitespace is stripped

    Args:
        title: Task title to validate

    Raises:
        TaskValidationError: If title is invalid
    """
    stripped = title.strip()
    if not stripped:
        raise TaskValidationError("Title cannot be empty (min 1 character required)")

    word_count = len(stripped.split())
    if word_count > MAX_TITLE_WORDS:
        raise TaskValidationError(
            f"Title too long ({word_count} words, max {MAX_TITLE_WORDS} words allowed)"
        )


def validate_description(description: str) -> None:
    """Validate task description.

    Rules:
    - 0-500 characters
    - Empty string is valid (optional field)
    - Multiline allowed

    Args:
        description: Task description to validate

    Raises:
        TaskValidationError: If description is invalid
    """
    if len(description) > MAX_DESCRIPTION_CHARS:
        raise TaskValidationError(
            f"Description too long ({len(description)} characters, max {MAX_DESCRIPTION_CHARS} characters allowed)"
        )


def validate_id(task_id: str) -> None:
    """Validate task ID format.

    Rules:
    - Exactly 8 characters
    - Lowercase hexadecimal (0-9, a-f only)

    Args:
        task_id: Task ID to validate

    Raises:
        TaskValidationError: If ID is invalid
    """
    if not ID_PATTERN.match(task_id):
        raise TaskValidationError(
            f"Invalid ID format: '{task_id}' (must be 8 hex characters)"
        )


def validate_status(status: str) -> None:
    """Validate task status.

    Rules:
    - Must be exactly "pending" or "completed"
    - Case-sensitive

    Args:
        status: Task status to validate

    Raises:
        TaskValidationError: If status is invalid
    """
    if status not in ALLOWED_STATUSES:
        raise TaskValidationError(
            f"Invalid status: '{status}' (must be 'pending' or 'completed')"
        )


def validate_timestamp(timestamp: str) -> None:
    """Validate ISO 8601 timestamp format.

    Rules:
    - Format: YYYY-MM-DD HH:MM:SS
    - Must be parseable as datetime
    - No timezone suffix

    Args:
        timestamp: Timestamp string to validate

    Raises:
        TaskValidationError: If timestamp is invalid
    """
    try:
        datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    except ValueError:
        raise TaskValidationError(
            f"Invalid timestamp format: '{timestamp}' (expected YYYY-MM-DD HH:MM:SS)"
        )


def validate_terminal_width(width: int) -> None:
    """Validate terminal width meets minimum requirement.

    Rules:
    - Width must be >= 80 columns

    Args:
        width: Terminal width in columns

    Raises:
        TerminalError: If terminal is too narrow
    """
    if width < MIN_TERMINAL_WIDTH:
        raise TerminalError(
            "⚠️ Terminal too narrow. Please resize to at least 80 columns."
        )


def validate_page_number(page: int, max_page: int) -> None:
    """Validate pagination page number.

    Rules:
    - Page must be >= 0 (zero-indexed)
    - Page must be < max_page (if max_page > 0)

    Args:
        page: Zero-indexed page number
        max_page: Maximum valid page number (exclusive)

    Raises:
        PaginationError: If page is invalid
    """
    if page < 0 or (max_page > 0 and page >= max_page):
        raise PaginationError(f"Invalid page number: {page} (must be 0-{max_page - 1})")


def validate_non_empty_selection(selected_ids: list[str]) -> None:
    """Validate that at least one item is selected.

    Rules:
    - List must not be empty
    - Used for bulk operations (delete, mark complete)

    Args:
        selected_ids: List of selected task IDs

    Raises:
        ValidationError: If selection is empty
    """
    if not selected_ids:
        raise ValidationError("❌ No tasks selected. Please select at least one task.")


# Validation helper functions


def is_valid_id(task_id: str) -> bool:
    """Check if task ID format is valid (non-raising).

    Args:
        task_id: Task ID to check

    Returns:
        True if ID format is valid, False otherwise
    """
    return bool(ID_PATTERN.match(task_id))


def is_valid_status(status: str) -> bool:
    """Check if status value is valid (non-raising).

    Args:
        status: Status to check

    Returns:
        True if status is valid, False otherwise
    """
    return status in ALLOWED_STATUSES


def is_valid_timestamp(timestamp: str) -> bool:
    """Check if timestamp format is valid (non-raising).

    Args:
        timestamp: Timestamp to check

    Returns:
        True if timestamp is parseable, False otherwise
    """
    try:
        datetime.strptime(timestamp, TIMESTAMP_FORMAT)
        return True
    except ValueError:
        return False


def count_words(text: str) -> int:
    """Count words in text (space-separated).

    Args:
        text: Text to count words in

    Returns:
        Number of words (after stripping whitespace)
    """
    return len(text.strip().split())


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to maximum length with suffix.

    Args:
        text: Text to truncate
        max_length: Maximum length (including suffix)
        suffix: Suffix to add if truncated (default: "...")

    Returns:
        Truncated text with suffix if needed
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
