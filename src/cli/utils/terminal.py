"""Terminal utility functions."""

import shutil

from src.services.validators import validate_terminal_width


def get_terminal_width() -> int:
    """Get current terminal width in columns.

    Returns:
        Terminal width in columns
    """
    size = shutil.get_terminal_size()
    return size.columns


def check_terminal_width() -> None:
    """Check if terminal width meets minimum requirement.

    Raises:
        TerminalError: If terminal is too narrow
    """
    width = get_terminal_width()
    validate_terminal_width(width)
