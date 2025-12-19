"""Toggle task status command implementation."""

from src.cli.display.formatters import console, create_task_table, show_error, show_info
from src.cli.utils.styles import checkbox_fullwidth, confirm_fullwidth, select_fullwidth
from src.exceptions import TaskNotFoundError, ValidationError
from src.services.task_service import TaskService


def toggle_status_interactive(service: TaskService) -> None:
    """Interactive command to mark tasks as complete or incomplete.

    Args:
        service: TaskService instance
    """
    try:
        # Show action menu
        console.print()
        action = select_fullwidth(
            "What would you like to do?",
            choices=[
                "✅ Mark tasks as complete",
                "⏸️  Mark tasks as incomplete",
                "← Back to main menu",
            ],
        )

        if action is None or action == "← Back to main menu":
            return

        # Filter tasks based on action
        if action == "✅ Mark tasks as complete":
            target_status = "pending"
            tasks = service.filter_by_status("pending")
            success_msg = "✅ {count} task(s) marked as completed!"
        else:
            target_status = "completed"
            tasks = service.filter_by_status("completed")
            success_msg = "✅ {count} task(s) marked as pending!"

        if not tasks:
            show_info(f"No {target_status} tasks to update.")
            return

        # Show tasks table
        console.print()
        table = create_task_table(tasks)
        console.print(table)
        console.print()

        # Create checkbox choices
        task_choices = [
            {"name": f"[{task.id}] {task.title}", "value": task.id} for task in tasks
        ]

        # Select tasks
        selected_ids = checkbox_fullwidth(
            f"Select tasks to mark as {'completed' if action == '✅ Mark tasks as complete' else 'pending'}:",
            choices=task_choices,
        )

        if selected_ids is None or not selected_ids:
            return

        # Confirm action
        count = len(selected_ids)
        confirm = confirm_fullwidth(
            f"{'Complete' if action == '✅ Mark tasks as complete' else 'Mark as pending'} {count} selected task(s)?",
        )

        if not confirm:
            return

        # Perform bulk update
        if action == "✅ Mark tasks as complete":
            service.mark_tasks_completed(selected_ids)
        else:
            service.mark_tasks_pending(selected_ids)

        # Show success
        show_info(success_msg.format(count=count))

    except TaskNotFoundError as e:
        show_error(f"❌ Task not found: {str(e)}")
    except ValidationError as e:
        show_error(f"❌ Validation error: {str(e)}")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        show_error(f"Unexpected error: {str(e)}", exception=e)
