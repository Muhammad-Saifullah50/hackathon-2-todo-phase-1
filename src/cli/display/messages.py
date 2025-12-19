"""Message constants for CLI display."""

from typing import Final

# Success messages
SUCCESS_TASK_ADDED: Final[str] = "✅ Task added successfully!"
SUCCESS_TASK_UPDATED: Final[str] = "✅ Task updated successfully!"
SUCCESS_TASK_DELETED: Final[str] = "✅ Task deleted successfully!"
SUCCESS_TASKS_DELETED: Final[str] = "✅ {count} task(s) deleted successfully!"
SUCCESS_TASK_COMPLETED: Final[str] = "✅ Task marked as completed!"
SUCCESS_TASK_PENDING: Final[str] = "✅ Task marked as pending!"
SUCCESS_TASKS_COMPLETED: Final[str] = "✅ {count} task(s) marked as completed!"
SUCCESS_TASKS_PENDING: Final[str] = "✅ {count} task(s) marked as pending!"

# Error messages
ERROR_TITLE_EMPTY: Final[str] = "❌ Title cannot be empty"
ERROR_TITLE_TOO_LONG: Final[str] = "❌ Title too long ({words} words, max 10 words)"
ERROR_DESCRIPTION_TOO_LONG: Final[str] = (
    "❌ Description too long ({chars} characters, max 500 characters)"
)
ERROR_TASK_NOT_FOUND: Final[str] = "❌ Task not found: {task_id}"
ERROR_NO_TASKS: Final[str] = "⚠️  No tasks exist yet. Create your first task!"
ERROR_NO_SELECTION: Final[str] = "❌ No tasks selected. Please select at least one task."
ERROR_STORAGE: Final[str] = "❌ Storage error: {message}"
ERROR_VALIDATION: Final[str] = "❌ Validation error: {message}"

# Info messages
INFO_GOODBYE: Final[str] = "👋 Thanks for using Todo CLI! Goodbye."
INFO_SHOWING_TASKS: Final[str] = "Showing {start}-{end} of {total} tasks"
INFO_TERMINAL_TOO_NARROW: Final[str] = (
    "⚠️  Terminal too narrow. Please resize to at least 80 columns."
)

# Prompts
PROMPT_TASK_TITLE: Final[str] = "Enter task title (1-10 words):"
PROMPT_TASK_DESCRIPTION: Final[str] = "Enter task description (optional, max 500 chars):"
PROMPT_UPDATE_CHOICE: Final[str] = "What would you like to update?"
PROMPT_CONFIRM_DELETE: Final[str] = "Delete {count} selected task(s)?"
PROMPT_SELECT_TASK: Final[str] = "Select a task:"
PROMPT_MAIN_MENU: Final[str] = "What would you like to do?"
