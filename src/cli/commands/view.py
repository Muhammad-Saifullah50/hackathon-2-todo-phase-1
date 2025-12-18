"""View tasks command implementation."""

import math

import questionary

from src.cli.display.formatters import console, create_task_table, show_empty_state, show_info
from src.services.task_service import TaskService


def view_all_tasks(service: TaskService) -> None:
    """Display tasks with filtering and pagination.

    Args:
        service: TaskService instance
    """
    try:
        # Show filter menu
        filter_choice = questionary.select(
            "Select view:",
            choices=[
                "All tasks",
                "Pending tasks",
                "Completed tasks",
                "← Back to main menu",
            ],
        ).ask()

        if filter_choice is None or filter_choice == "← Back to main menu":
            return

        # Get tasks based on filter
        if filter_choice == "All tasks":
            tasks = service.get_all_tasks()
        elif filter_choice == "Pending tasks":
            tasks = service.filter_by_status("pending")
        else:  # Completed tasks
            tasks = service.filter_by_status("completed")

        # Handle empty state
        if not tasks:
            show_empty_state()
            return

        # Pagination
        page_size = 10
        total_pages = math.ceil(len(tasks) / page_size)
        current_page = 0

        while True:
            # Get current page tasks
            page_tasks = service.paginate(tasks, current_page, page_size)

            # Show header
            start_idx = current_page * page_size + 1
            end_idx = min(start_idx + len(page_tasks) - 1, len(tasks))
            console.print()
            show_info(f"Showing {start_idx}-{end_idx} of {len(tasks)} tasks (Page {current_page + 1}/{total_pages})")

            # Create and display table
            table = create_task_table(page_tasks)
            console.print()
            console.print(table)
            console.print()

            # Navigation menu
            nav_choices = []
            if current_page > 0:
                nav_choices.append("← Previous page")
            if current_page < total_pages - 1:
                nav_choices.append("Next page →")
            nav_choices.append("← Back to filter menu")

            if len(nav_choices) == 1:
                # Only back option, just return
                return

            nav = questionary.select("Navigation:", choices=nav_choices).ask()

            if nav is None or nav == "← Back to filter menu":
                return
            elif nav == "← Previous page":
                current_page -= 1
            elif nav == "Next page →":
                current_page += 1

    except KeyboardInterrupt:
        # Let the main app handle KeyboardInterrupt
        raise
    except Exception as e:
        from src.cli.display.formatters import show_error

        show_error(f"Error loading tasks: {str(e)}", exception=e)
