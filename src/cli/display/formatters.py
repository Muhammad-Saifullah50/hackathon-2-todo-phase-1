"""Rich formatters for beautiful terminal output."""

import shutil

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

from src.models.task import Task
from src.services.validators import truncate_text

# Custom theme
custom_theme = Theme(
    {
        "success": "bold green",
        "error": "bold red",
        "warning": "bold yellow",
        "info": "bold blue",
        "pending": "yellow",
        "completed": "green",
    }
)

console = Console(theme=custom_theme)


def create_task_table(tasks: list[Task]) -> Table:
    """Create a rich Table with tasks.

    Args:
        tasks: List of Task objects

    Returns:
        Rich Table object
    """
    table = Table(title="📋 Todo List", show_header=True, header_style="bold cyan")

    table.add_column("ID", style="dim", width=10)
    table.add_column("Status", width=8)
    table.add_column("Title", style="bold")
    table.add_column("Description", style="dim")
    table.add_column("Created", style="dim", width=19)

    for task in tasks:
        # Status icon
        status_icon = "✓" if task.status == "completed" else "✗"
        status_style = "completed" if task.status == "completed" else "pending"

        # Truncate description
        desc_truncated = truncate_text(task.description, 40) if task.description else "-"

        table.add_row(
            task.id,
            f"[{status_style}]{status_icon}[/{status_style}]",
            task.title,
            desc_truncated,
            task.created_at,
        )

    return table


def create_single_task_panel(task: Task) -> Panel:
    """Create a rich Panel with task details.

    Args:
        task: Task object

    Returns:
        Rich Panel object
    """
    status_icon = "✓ Completed" if task.status == "completed" else "✗ Pending"
    status_style = "completed" if task.status == "completed" else "pending"

    content = f"""
[bold]ID:[/bold] {task.id}
[bold]Title:[/bold] {task.title}
[bold]Description:[/bold] {task.description if task.description else "(none)"}
[bold]Status:[/bold] [{status_style}]{status_icon}[/{status_style}]
[bold]Created:[/bold] {task.created_at}
[bold]Updated:[/bold] {task.updated_at}
    """.strip()

    return Panel(content, title="Task Details", border_style="cyan")


def show_success(message: str, task: Task | None = None) -> None:
    """Display success message with optional task details.

    Args:
        message: Success message to display
        task: Optional Task object to display
    """
    panel = Panel(message, style="success", border_style="green")
    console.print(panel)

    if task:
        console.print()
        console.print(create_single_task_panel(task))


def show_error(message: str, exception: Exception | None = None) -> None:
    """Display error message with optional exception details.

    Args:
        message: Error message to display
        exception: Optional exception object
    """
    if exception:
        content = f"{message}\n\n[dim]Details: {str(exception)}[/dim]"
    else:
        content = message

    panel = Panel(content, style="error", border_style="red")
    console.print(panel)


def show_info(message: str) -> None:
    """Display info message.

    Args:
        message: Info message to display
    """
    panel = Panel(message, style="info", border_style="blue")
    console.print(panel)


def show_empty_state() -> None:
    """Display empty state message when no tasks exist."""
    message = "⚠️  No tasks exist yet. Create your first task!"
    panel = Panel(message, style="warning", border_style="yellow")
    console.print(panel)


def show_welcome_banner() -> None:
    """Display welcome banner when app starts."""
    # Get terminal width and create full-width banner
    term_width = shutil.get_terminal_size().columns
    # Account for panel borders (2 chars on each side)
    content_width = term_width - 4

    # Create centered text
    title = "📋  TODO CLI APPLICATION  📋"
    subtitle = "Beautiful Task Management in Terminal"

    # Build banner content with proper centering
    banner_content = (
        f"\n{title.center(content_width)}\n"
        f"\n{subtitle.center(content_width)}\n"
    )

    # Use Rich Panel for full-width display
    panel = Panel(
        banner_content,
        style="bold cyan",
        border_style="bold cyan",
        expand=True,  # Make panel expand to full terminal width
        padding=(1, 2),
    )
    console.print(panel)

    # Show features and tips
    console.print(
        "[dim]✨ Features: Add • View • Update • Toggle • Delete ✨[/dim]".center(
            term_width
        )
    )
    console.print(
        "[dim]💡 Tip: Use arrow keys to navigate, Ctrl+C to exit[/dim]".center(term_width)
    )
