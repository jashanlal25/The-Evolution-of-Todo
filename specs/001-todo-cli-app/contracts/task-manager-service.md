# TaskManager Service Contract

**Date**: 2026-01-02
**Feature**: 001-todo-cli-app
**Purpose**: Define the internal service interface for task management operations

## Service Overview

The `TaskManager` service provides business logic for task CRUD operations and status management. It abstracts in-memory storage and enforces business rules.

**Location**: `src/services/task_manager.py`

**Responsibilities**:
- Task creation with ID generation
- Task retrieval by ID
- Task updates (title, description)
- Task status toggling (complete/incomplete)
- Task deletion
- Task listing and filtering

**Not Responsible For**:
- User input validation (handled by CLI layer)
- Output formatting (handled by CLI layer)
- CLI argument parsing (handled by CLI layer)

---

## Class Interface

### TaskManager

```python
from dataclasses import dataclass
from typing import Optional

class TaskManager:
    """
    Manages in-memory task storage and business operations.

    Thread Safety: Not thread-safe (single-threaded CLI application).
    Persistence: In-memory only, data lost on application exit.
    """

    def __init__(self) -> None:
        """
        Initialize TaskManager with empty task storage.

        Post-conditions:
        - Internal storage is empty dictionary
        - ID counter initialized to 1
        """

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

        Post-conditions:
        - Task added to storage with unique ID
        - ID counter incremented
        - Task.completed initialized to False

        Performance: O(1)
        """

    def get(self, task_id: int) -> Task:
        """
        Retrieve task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: The task with the specified ID

        Raises:
            TaskNotFoundError: If task_id doesn't exist in storage

        Performance: O(1)
        """

    def update(self, task_id: int, title: Optional[str] = None,
               description: Optional[str] = None) -> Task:
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

        Pre-conditions:
        - At least one of title or description must be provided (validated by CLI)

        Post-conditions:
        - Task in storage updated with new values
        - Unchanged fields remain the same
        - Task.id and Task.completed unchanged

        Performance: O(1)
        """

    def mark_complete(self, task_id: int) -> Task:
        """
        Mark task as complete.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: The updated task with completed=True

        Raises:
            TaskNotFoundError: If task_id doesn't exist

        Post-conditions:
        - Task.completed set to True
        - Other task attributes unchanged

        Performance: O(1)

        Note: Idempotent - marking already complete task has no effect
        """

    def mark_incomplete(self, task_id: int) -> Task:
        """
        Mark task as incomplete.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: The updated task with completed=False

        Raises:
            TaskNotFoundError: If task_id doesn't exist

        Post-conditions:
        - Task.completed set to False
        - Other task attributes unchanged

        Performance: O(1)

        Note: Idempotent - marking already incomplete task has no effect
        """

    def delete(self, task_id: int) -> Task:
        """
        Delete task from storage.

        Args:
            task_id: Unique task identifier

        Returns:
            Task: The deleted task (for confirmation message)

        Raises:
            TaskNotFoundError: If task_id doesn't exist

        Post-conditions:
        - Task removed from storage
        - ID not reused (counter not decremented)

        Performance: O(1)

        Note: Not idempotent - second delete raises TaskNotFoundError
        """

    def list_all(self) -> list[Task]:
        """
        Retrieve all tasks sorted by ID.

        Returns:
            list[Task]: All tasks in ascending ID order

        Post-conditions:
        - Return value is a new list (not internal storage reference)
        - Tasks sorted by ID (lowest to highest)

        Performance: O(n log n) due to sorting
        """

    def list_completed(self) -> list[Task]:
        """
        Retrieve completed tasks sorted by ID.

        Returns:
            list[Task]: Completed tasks in ascending ID order

        Post-conditions:
        - Return value contains only tasks with completed=True
        - Tasks sorted by ID

        Performance: O(n log n)
        """

    def list_incomplete(self) -> list[Task]:
        """
        Retrieve incomplete tasks sorted by ID.

        Returns:
            list[Task]: Incomplete tasks in ascending ID order

        Post-conditions:
        - Return value contains only tasks with completed=False
        - Tasks sorted by ID

        Performance: O(n log n)
        """

    def count(self) -> int:
        """
        Get total number of tasks.

        Returns:
            int: Total task count

        Performance: O(1)
        """
```

---

## Data Types

### Task (Dataclass)

```python
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

    Immutability: Frozen dataclass prevents attribute modification after creation.
                  Updates create new Task instances.

    Memory: Uses __slots__ for memory efficiency.
    """
    id: int
    title: str
    description: str
    completed: bool
```

**Note**: Task is immutable. Update operations create new Task instances internally.

---

## Exception Types

### TaskNotFoundError

```python
class TaskNotFoundError(Exception):
    """Raised when operation references non-existent task ID."""

    def __init__(self, task_id: int):
        super().__init__(f"Task with ID {task_id} not found")
        self.task_id = task_id
```

### InvalidTaskError

```python
class InvalidTaskError(Exception):
    """Raised when task data violates validation rules."""
    pass
```

### EmptyTitleError

```python
class EmptyTitleError(InvalidTaskError):
    """Raised when task title is empty or whitespace-only."""

    def __init__(self):
        super().__init__("Task title cannot be empty")
```

---

## Business Rules

### ID Generation

1. **Monotonic Increment**: IDs start at 1 and increment by 1 for each new task
2. **No Reuse**: Deleted task IDs are never reused within the session
3. **Uniqueness**: Each task has exactly one unique ID
4. **Immutability**: Task ID cannot be changed after creation

**Example**:
```python
manager = TaskManager()
task1 = manager.add("Task 1")  # ID: 1
task2 = manager.add("Task 2")  # ID: 2
manager.delete(1)              # Delete task 1
task3 = manager.add("Task 3")  # ID: 3 (not 1, ID not reused)
```

### Title Validation

1. **Required**: Title must be provided (cannot be None)
2. **Non-Empty**: Title cannot be empty string or whitespace-only after `.strip()`
3. **Max Length**: Title cannot exceed 200 characters
4. **Unicode**: Title may contain any valid Unicode characters

**Valid Examples**:
- `"Buy groceries"`
- `"学习中文"`
- `"Task #42: Fix bug"`
- `"A" * 200` (exactly 200 chars)

**Invalid Examples**:
- `""` → EmptyTitleError
- `"   "` → EmptyTitleError (whitespace-only)
- `"A" * 201` → InvalidTaskError (too long)

### Description Validation

1. **Optional**: Description can be empty string or None (converted to empty string)
2. **Max Length**: Description cannot exceed 1000 characters
3. **Unicode**: Description may contain any valid Unicode characters

**Valid Examples**:
- `""` (empty, valid)
- `"Detailed task description"`
- `"你好世界"`
- `"B" * 1000` (exactly 1000 chars)

**Invalid Examples**:
- `"B" * 1001` → InvalidTaskError (too long)

### Status Toggling

1. **Boolean**: completed is strictly boolean (True or False)
2. **Default**: New tasks default to `completed=False`
3. **Idempotent**: Marking complete task as complete has no effect
4. **Reversible**: Tasks can toggle between complete and incomplete unlimited times

---

## State Management

### Internal Storage

**Implementation**: `dict[int, Task]`

**Invariants**:
1. All keys are positive integers (task IDs)
2. All values are valid Task instances
3. Every task in storage has unique ID
4. ID counter is always > max(storage.keys()) or 1 if storage empty

**Example State**:
```python
{
    1: Task(id=1, title="Task 1", description="", completed=False),
    2: Task(id=2, title="Task 2", description="Details", completed=True),
    5: Task(id=5, title="Task 5", description="", completed=False)
}
# ID counter: 6 (next task will get ID 6)
```

### State Transitions

**Add Operation**:
```
Initial: storage = {}, counter = 1
add("Task")
Final: storage = {1: Task(...)}, counter = 2
```

**Update Operation**:
```
Initial: storage = {1: Task(id=1, title="Old", ...)}
update(1, title="New")
Final: storage = {1: Task(id=1, title="New", ...)}
```

**Delete Operation**:
```
Initial: storage = {1: Task(...), 2: Task(...)}, counter = 3
delete(1)
Final: storage = {2: Task(...)}, counter = 3 (unchanged)
```

**Complete Operation**:
```
Initial: storage = {1: Task(id=1, ..., completed=False)}
mark_complete(1)
Final: storage = {1: Task(id=1, ..., completed=True)}
```

---

## Contract Tests

TaskManager must have contract tests validating:

### Add Operation
- ✓ Creates task with auto-generated ID
- ✓ Sets completed=False by default
- ✓ Increments ID counter
- ✓ Raises EmptyTitleError for empty title
- ✓ Raises InvalidTaskError for title > 200 chars
- ✓ Raises InvalidTaskError for description > 1000 chars
- ✓ Handles Unicode characters correctly

### Get Operation
- ✓ Returns task for valid ID
- ✓ Raises TaskNotFoundError for non-existent ID
- ✓ Returned task matches added task

### Update Operation
- ✓ Updates title only when description=None
- ✓ Updates description only when title=None
- ✓ Updates both when both provided
- ✓ Preserves unchanged fields
- ✓ Raises TaskNotFoundError for invalid ID
- ✓ Raises EmptyTitleError for empty title
- ✓ Raises InvalidTaskError for title/description too long

### Mark Complete/Incomplete
- ✓ Toggles completed status correctly
- ✓ Idempotent (no error on repeat)
- ✓ Raises TaskNotFoundError for invalid ID
- ✓ Preserves other task attributes

### Delete Operation
- ✓ Removes task from storage
- ✓ Returns deleted task for confirmation
- ✓ Raises TaskNotFoundError for invalid ID
- ✓ Not idempotent (second delete raises error)
- ✓ Does not reuse deleted ID

### List Operations
- ✓ list_all() returns all tasks sorted by ID
- ✓ list_completed() returns only completed tasks
- ✓ list_incomplete() returns only incomplete tasks
- ✓ Returns new list (not storage reference)
- ✓ Returns empty list when no tasks match

### Count Operation
- ✓ Returns 0 for empty storage
- ✓ Returns correct count after add/delete

---

## Performance Guarantees

| Operation | Complexity | Max Time (1000 tasks) |
|-----------|-----------|----------------------|
| add | O(1) | < 1ms |
| get | O(1) | < 1ms |
| update | O(1) | < 1ms |
| mark_complete | O(1) | < 1ms |
| mark_incomplete | O(1) | < 1ms |
| delete | O(1) | < 1ms |
| list_all | O(n log n) | < 10ms |
| list_completed | O(n log n) | < 10ms |
| list_incomplete | O(n log n) | < 10ms |
| count | O(1) | < 1ms |

---

## Thread Safety

**Not Thread-Safe**: TaskManager is designed for single-threaded CLI use.

**Rationale**: Phase I is a CLI application with sequential command execution. No concurrent access is possible.

**Phase II Consideration**: If web application requires concurrent access, TaskManager interface remains the same but implementation may add locking or use thread-safe storage.

---

## Migration Notes (Phase I → Phase II)

### Preserved Interface

All methods signatures remain unchanged:
- Same method names
- Same parameter types
- Same return types
- Same exceptions

### Implementation Changes

Phase II `DatabaseTaskManager` will:
- Replace `dict[int, Task]` with SQLModel database queries
- Use database transactions for consistency
- Generate UUIDs instead of integer IDs (type change)
- Add timestamp fields (created_at, updated_at)

### Compatibility Strategy

```python
# Phase I
task_manager = TaskManager()  # In-memory

# Phase II
task_manager = DatabaseTaskManager(db_session)  # Database-backed

# Both implement same interface, CLI code unchanged
```

**No Breaking Changes**: Business logic tests remain valid for both implementations.
