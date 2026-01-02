"""TaskManager service for task CRUD operations."""

from typing import Optional

from src.models.exceptions import EmptyTitleError, InvalidTaskError, TaskNotFoundError
from src.models.task import Task


class TaskManager:
    """
    Manages in-memory task storage and business operations.

    Thread Safety: Not thread-safe (single-threaded CLI application).
    Persistence: In-memory only, data lost on application exit (Phase I Constitution).
    """

    def __init__(self) -> None:
        """Initialize TaskManager with empty task storage."""
        self._storage: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, title: str, description: str = "") -> Task:
        """
        Create a new task with auto-generated ID.

        Args:
            title: Task title (required, non-empty after strip)
            description: Task description (optional, defaults to empty string)

        Returns:
            Task: The newly created task with assigned ID

        Raises:
            EmptyTitleError: If title is empty or whitespace-only
            InvalidTaskError: If title > 200 chars or description > 1000 chars
        """
        # Validate title
        title_stripped = title.strip()
        if not title_stripped:
            raise EmptyTitleError()
        if len(title_stripped) > 200:
            raise InvalidTaskError("Task title cannot exceed 200 characters")

        # Validate description
        if len(description) > 1000:
            raise InvalidTaskError("Task description cannot exceed 1000 characters")

        # Create task
        task = Task(
            id=self._next_id, title=title_stripped, description=description, completed=False
        )

        # Store and increment counter
        self._storage[self._next_id] = task
        self._next_id += 1

        return task

    def get(self, task_id: int) -> Task:
        """
        Retrieve task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: The task with the specified ID

        Raises:
            TaskNotFoundError: If task_id doesn't exist in storage
        """
        if task_id not in self._storage:
            raise TaskNotFoundError(task_id)
        return self._storage[task_id]

    def list_all(self) -> list[Task]:
        """
        Retrieve all tasks sorted by ID.

        Returns:
            list[Task]: All tasks in ascending ID order
        """
        return sorted(self._storage.values(), key=lambda t: t.id)

    def update(
        self, task_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> Task:
        """
        Update task title and/or description.

        Args:
            task_id: Unique task identifier
            title: New title (if provided)
            description: New description (if provided)

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundError: If task_id doesn't exist
            EmptyTitleError: If new title is empty or whitespace-only
            InvalidTaskError: If new title > 200 chars or new description > 1000 chars
        """
        # Get existing task
        existing_task = self.get(task_id)

        # Determine new values
        new_title = title if title is not None else existing_task.title
        new_description = description if description is not None else existing_task.description

        # Validate new title
        if title is not None:
            title_stripped = title.strip()
            if not title_stripped:
                raise EmptyTitleError()
            if len(title_stripped) > 200:
                raise InvalidTaskError("Task title cannot exceed 200 characters")
            new_title = title_stripped

        # Validate new description
        if description is not None and len(description) > 1000:
            raise InvalidTaskError("Task description cannot exceed 1000 characters")

        # Create updated task (frozen dataclass, must create new instance)
        updated_task = Task(
            id=existing_task.id,
            title=new_title,
            description=new_description,
            completed=existing_task.completed,
        )

        # Store updated task
        self._storage[task_id] = updated_task

        return updated_task

    def mark_complete(self, task_id: int) -> Task:
        """
        Mark task as complete.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: The updated task with completed=True

        Raises:
            TaskNotFoundError: If task_id doesn't exist
        """
        existing_task = self.get(task_id)

        # Create updated task with completed=True
        updated_task = Task(
            id=existing_task.id,
            title=existing_task.title,
            description=existing_task.description,
            completed=True,
        )

        # Store updated task
        self._storage[task_id] = updated_task

        return updated_task

    def mark_incomplete(self, task_id: int) -> Task:
        """
        Mark task as incomplete.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: The updated task with completed=False

        Raises:
            TaskNotFoundError: If task_id doesn't exist
        """
        existing_task = self.get(task_id)

        # Create updated task with completed=False
        updated_task = Task(
            id=existing_task.id,
            title=existing_task.title,
            description=existing_task.description,
            completed=False,
        )

        # Store updated task
        self._storage[task_id] = updated_task

        return updated_task

    def delete(self, task_id: int) -> Task:
        """
        Delete task from storage.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: The deleted task (for confirmation message)

        Raises:
            TaskNotFoundError: If task_id doesn't exist
        """
        # Get task before deletion (will raise if not found)
        task = self.get(task_id)

        # Remove from storage
        del self._storage[task_id]

        return task

    def count(self) -> int:
        """
        Get total number of tasks.

        Returns:
            int: Total task count
        """
        return len(self._storage)

    def clear_all(self) -> int:
        """
        Clear all tasks from memory.

        Returns:
            int: Number of tasks deleted
        """
        count = len(self._storage)
        self._storage.clear()
        self._next_id = 1
        return count
