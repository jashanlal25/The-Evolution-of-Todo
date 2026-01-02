"""Task data model for the Todo CLI application."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Task:
    """
    Immutable task entity.

    Attributes:
        id: Unique identifier (positive integer)
        title: Task title (non-empty, max 200 chars)
        description: Task description (max 1000 chars, can be empty)
        completed: Completion status (True/False)
    """

    id: int
    title: str
    description: str
    completed: bool
