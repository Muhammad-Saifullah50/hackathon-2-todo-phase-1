"""Main entry point for CLI Todo application."""

import argparse
import sys
from pathlib import Path

from src.cli.app import TodoApp
from src.exceptions import TerminalError
from src.services.task_service import TaskService
from src.storage.json_storage import JSONStorage


def main() -> None:
    """Initialize and run the CLI Todo application."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="CLI Todo Application")
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Run in simple mode (no colors, plain text)",
    )
    args = parser.parse_args()

    # Check terminal width (skip in simple mode)
    if not args.simple:
        try:
            from src.cli.utils.terminal import check_terminal_width

            check_terminal_width()
        except TerminalError as e:
            print(f"\n{str(e)}")
            print("Tip: Run with --simple flag for narrow terminals\n")
            sys.exit(1)

    # Initialize storage with tasks.json in current directory
    storage_path = Path("tasks.json")
    storage = JSONStorage(storage_path)

    # Initialize service
    service = TaskService(storage)

    # Initialize and run app
    app = TodoApp(service)
    app.run()


if __name__ == "__main__":
    main()
