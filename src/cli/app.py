"""Main CLI application with menu routing."""

from src.cli.commands.add import add_task_interactive
from src.cli.commands.toggle import toggle_status_interactive
from src.cli.commands.update import update_task_interactive
from src.cli.commands.view import view_all_tasks
from src.cli.display.formatters import console, show_info, show_welcome_banner
from src.cli.display.messages import INFO_GOODBYE, PROMPT_MAIN_MENU
from src.cli.utils.styles import select_fullwidth
from src.services.task_service import TaskService


class TodoApp:
    """Main CLI application."""

    def __init__(self, service: TaskService) -> None:
        """Initialize the app.

        Args:
            service: TaskService instance
        """
        self.service = service

    def run(self) -> None:
        """Run the main application loop."""
        try:
            # Show welcome banner
            show_welcome_banner()

            # Show task statistics
            stats = self.service.count_tasks()
            if stats["total"] > 0:
                stats_msg = (
                    f"[cyan]📊 Current Status:[/cyan] "
                    f"{stats['total']} total • "
                    f"[yellow]{stats['pending']} pending[/yellow] • "
                    f"[green]{stats['completed']} completed[/green]"
                )
                console.print(stats_msg)
            console.print()

            while True:
                # Show main menu with extra spacing
                console.print()
                choice = select_fullwidth(
                    PROMPT_MAIN_MENU,
                    choices=[
                        "📝 Add task",
                        "👀 View all tasks",
                        "✏️  Update task",
                        "✅ Toggle task status",
                        "🗑️  Delete tasks",
                        "🚪 Exit",
                    ],
                    use_shortcuts=False,
                )

                # User cancelled (Ctrl+C or Esc)
                if choice is None:
                    break

                # Route to command
                if choice == "📝 Add task":
                    console.print()
                    add_task_interactive(self.service)
                elif choice == "👀 View all tasks":
                    view_all_tasks(self.service)
                elif choice == "✏️  Update task":
                    console.print()
                    update_task_interactive(self.service)
                elif choice == "✅ Toggle task status":
                    console.print()
                    toggle_status_interactive(self.service)
                elif choice == "🗑️  Delete tasks":
                    console.print()
                    from src.cli.commands.delete import delete_tasks_interactive

                    delete_tasks_interactive(self.service)
                elif choice == "🚪 Exit":
                    break

                # Add spacing between operations
                console.print()

        except KeyboardInterrupt:
            pass
        finally:
            # Show goodbye message
            console.print()
            show_info(INFO_GOODBYE)
