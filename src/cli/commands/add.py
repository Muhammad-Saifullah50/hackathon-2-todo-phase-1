"""Add task command implementation."""

import questionary

from src.cli.display.formatters import show_error, show_success
from src.cli.display.messages import (
    ERROR_VALIDATION,
    PROMPT_TASK_DESCRIPTION,
    PROMPT_TASK_TITLE,
    SUCCESS_TASK_ADDED,
)
from src.exceptions import TaskValidationError
from src.services.task_service import TaskService


def add_task_interactive(service: TaskService) -> None:
    """Interactive command to add a new task.

    Prompts user for title and optional description, then creates the task.

    Args:
        service: TaskService instance
    """
    try:
        # Prompt for title
        title = questionary.text(
            PROMPT_TASK_TITLE,
            validate=lambda text: len(text.strip()) > 0 or "Title cannot be empty",
        ).ask()

        # User cancelled
        if title is None:
            return

        # Prompt for description (optional)
        description = questionary.text(
            PROMPT_TASK_DESCRIPTION,
            default="",
        ).ask()

        # User cancelled
        if description is None:
            return

        # Create task
        task = service.add_task(title=title, description=description)

        # Show success with task details
        show_success(SUCCESS_TASK_ADDED, task=task)

    except TaskValidationError as e:
        show_error(ERROR_VALIDATION.format(message=str(e)))
    except KeyboardInterrupt:
        # Let the main app handle KeyboardInterrupt
        raise
    except Exception as e:
        show_error(f"Unexpected error: {str(e)}", exception=e)
