"""Custom exceptions for the Todo CLI application."""


class TaskNotFoundError(Exception):
    """Raised when operation references non-existent task ID."""

    def __init__(self, task_id: int) -> None:
        super().__init__(f"Task with ID {task_id} not found")
        self.task_id = task_id


class InvalidTaskError(Exception):
    """Raised when task data violates validation rules."""

    pass


class EmptyTitleError(InvalidTaskError):
    """Raised when task title is empty or whitespace-only."""

    def __init__(self) -> None:
        super().__init__("Task title cannot be empty")
