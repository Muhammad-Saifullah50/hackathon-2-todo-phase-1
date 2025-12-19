"""Custom styles for questionary prompts."""

import shutil
from typing import Any, Callable, List, Optional, Union

import questionary
from questionary import Style
from rich.console import Console
from rich.panel import Panel

# Initialize console for rich output
console = Console()

# Custom style for all menus with better spacing and colors
# Using background colors to create full-width visual effect
menu_style = Style(
    [
        ("qmark", "fg:#5f5fff bold"),  # Question mark - bright blue
        ("question", "fg:#ffffff bold"),  # Question text - white bold
        ("answer", "fg:#5fff5f bold"),  # User answer - bright green
        ("pointer", "fg:#5fff5f bold"),  # Pointer (>) - bright green
        ("highlighted", "fg:#5fff5f bold bg:#262626"),  # Highlighted option - green on dark gray
        ("selected", "fg:#5fff5f bold"),  # Selected items in checkbox - bright green
        ("separator", "fg:#444444"),  # Separator lines - dark gray
        ("instruction", "fg:#888888"),  # Instructions - medium gray
        ("text", "fg:#ffffff"),  # Normal text - white
        ("disabled", "fg:#666666 italic"),  # Disabled items - gray italic
        ("answer-input", "fg:#5fff5f"),  # Text input cursor area - bright green
    ]
)


def _print_box_border(char: str = "─", style: str = "dim cyan") -> None:
    """Print a full-width horizontal border line.

    Args:
        char: Character to use for the border
        style: Rich style for the border
    """
    term_width = shutil.get_terminal_size().columns
    console.print(f"[{style}]{char * term_width}[/{style}]")


def select_fullwidth(
    message: str,
    choices: List[Union[str, dict]],
    **kwargs: Any,
) -> Optional[Any]:
    """Full-width select menu with visual box borders.

    Args:
        message: The question to ask
        choices: List of choices
        **kwargs: Additional questionary arguments

    Returns:
        Selected value or None if cancelled
    """
    _print_box_border("─", "dim cyan")
    result = questionary.select(message, choices=choices, style=menu_style, **kwargs).ask()
    _print_box_border("─", "dim cyan")
    return result


def checkbox_fullwidth(
    message: str,
    choices: List[Union[str, dict]],
    **kwargs: Any,
) -> Optional[List[Any]]:
    """Full-width checkbox menu with visual box borders.

    Args:
        message: The question to ask
        choices: List of choices
        **kwargs: Additional questionary arguments

    Returns:
        List of selected values or None if cancelled
    """
    _print_box_border("─", "dim cyan")
    result = questionary.checkbox(message, choices=choices, style=menu_style, **kwargs).ask()
    _print_box_border("─", "dim cyan")
    return result


def text_fullwidth(
    message: str,
    **kwargs: Any,
) -> Optional[str]:
    """Full-width text input with visual box borders.

    Args:
        message: The question/prompt to show
        **kwargs: Additional questionary arguments

    Returns:
        User input string or None if cancelled
    """
    _print_box_border("─", "dim cyan")
    result = questionary.text(message, style=menu_style, **kwargs).ask()
    _print_box_border("─", "dim cyan")
    return result


def confirm_fullwidth(
    message: str,
    **kwargs: Any,
) -> Optional[bool]:
    """Full-width confirmation prompt with visual box borders.

    Args:
        message: The question to ask
        **kwargs: Additional questionary arguments

    Returns:
        True/False or None if cancelled
    """
    _print_box_border("─", "dim cyan")
    result = questionary.confirm(message, style=menu_style, **kwargs).ask()
    _print_box_border("─", "dim cyan")
    return result
