"""Update task command implementation."""

import questionary

from src.cli.display.formatters import show_error, show_success
from src.cli.display.messages import ERROR_VALIDATION, PROMPT_TASK_DESCRIPTION, PROMPT_TASK_TITLE
from src.exceptions import TaskNotFoundError, TaskValidationError
from src.services.task_service import TaskService


def update_task_interactive(service: TaskService) -> None:
    """Interactive command to update an existing task.

    Args:
        service: TaskService instance
    """
    try:
        # Get all tasks
        tasks = service.get_all_tasks()

        if not tasks:
            from src.cli.display.formatters import show_empty_state

            show_empty_state()
            return

        # Create task choices for selection
        task_choices = [
            {
                "name": f"[{task.id}] {task.title}",
                "value": task.id,
            }
            for task in tasks
        ]
        task_choices.append({"name": "← Back to main menu", "value": None})

        # Select task
        selected_id = questionary.select(
            "Select a task to update:", choices=task_choices
        ).ask()

        if selected_id is None:
            return

        # Show update options
        update_choice = questionary.select(
            "What would you like to update?",
            choices=[
                "Title only",
                "Description only",
                "Both title and description",
                "← Cancel",
            ],
        ).ask()

        if update_choice is None or update_choice == "← Cancel":
            return

        new_title = None
        new_description = None

        # Get new values based on choice
        if update_choice in ["Title only", "Both title and description"]:
            new_title = questionary.text(
                PROMPT_TASK_TITLE,
                validate=lambda text: len(text.strip()) > 0 or "Title cannot be empty",
            ).ask()

            if new_title is None:
                return

        if update_choice in ["Description only", "Both title and description"]:
            new_description = questionary.text(
                PROMPT_TASK_DESCRIPTION,
                default="",
            ).ask()

            if new_description is None:
                return

        # Update task
        updated_task = service.update_task(
            task_id=selected_id, new_title=new_title, new_description=new_description
        )

        # Show success
        show_success("✅ Task updated successfully!", task=updated_task)

    except TaskNotFoundError as e:
        show_error(f"❌ Task not found: {str(e)}")
    except TaskValidationError as e:
        show_error(ERROR_VALIDATION.format(message=str(e)))
    except KeyboardInterrupt:
        raise
    except Exception as e:
        show_error(f"Unexpected error: {str(e)}", exception=e)
