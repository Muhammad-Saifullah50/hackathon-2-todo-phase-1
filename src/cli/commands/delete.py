"""Delete tasks command implementation."""

from src.cli.display.formatters import console, create_task_table, show_error, show_info
from src.cli.utils.styles import checkbox_fullwidth, confirm_fullwidth
from src.exceptions import ValidationError
from src.services.task_service import TaskService


def delete_tasks_interactive(service: TaskService) -> None:
    """Interactive command to delete tasks.

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

        # Show tasks table
        table = create_task_table(tasks)
        console.print(table)
        console.print()

        # Create checkbox choices
        task_choices = [
            {"name": f"[{task.id}] {task.title}", "value": task.id} for task in tasks
        ]

        # Select tasks to delete
        selected_ids = checkbox_fullwidth("Select tasks to delete:", choices=task_choices)

        if selected_ids is None or not selected_ids:
            return

        # Confirm deletion
        count = len(selected_ids)
        confirm = confirm_fullwidth(
            f"⚠️  Delete {count} selected task(s)? This cannot be undone."
        )

        if not confirm:
            show_info("Deletion cancelled.")
            return

        # Perform deletion
        deleted_count = service.delete_tasks(selected_ids)

        # Show success
        show_info(f"✅ {deleted_count} task(s) deleted successfully!")

        # Show remaining tasks
        remaining_tasks = service.get_all_tasks()
        if remaining_tasks:
            console.print()
            console.print(create_task_table(remaining_tasks))
            console.print()

    except ValidationError as e:
        show_error(f"❌ Validation error: {str(e)}")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        show_error(f"Unexpected error: {str(e)}", exception=e)
