# Data Model: Phase I Todo CLI App

**Date**: 2026-01-02
**Feature**: 001-todo-cli-app
**Purpose**: Define data entities, their attributes, validation rules, and state transitions

## Entities

### Task

**Description**: Represents a single todo item with title, description, completion status, and unique identifier.

**Attributes**:

| Attribute | Type | Required | Constraints | Default | Description |
|-----------|------|----------|-------------|---------|-------------|
| id | int | Yes | Positive integer, unique within session | Auto-generated | Unique identifier assigned at creation, immutable |
| title | str | Yes | Non-empty after strip(), max 200 chars | None | Brief description of the task |
| description | str | No | Max 1000 chars | Empty string | Detailed information about the task |
| completed | bool | Yes | True or False | False | Completion status of the task |

**Validation Rules**:

1. **Title Validation**:
   - Must not be None
   - Must not be empty string after whitespace removal (`.strip()`)
   - Must not exceed 200 characters
   - May contain any Unicode characters including special characters
   - Error: Raise `EmptyTitleError` if empty, `InvalidTaskError` if too long

2. **Description Validation**:
   - May be None or empty string (optional field)
   - If provided, must not exceed 1000 characters
   - May contain any Unicode characters including special characters
   - Error: Raise `InvalidTaskError` if too long

3. **ID Validation**:
   - Must be positive integer (>= 1)
   - Must be unique within the current session
   - Auto-assigned at creation, cannot be changed
   - Error: Raise `TaskNotFoundError` if ID doesn't exist in operations

4. **Completed Validation**:
   - Must be boolean (True or False)
   - Defaults to False at creation
   - Can be toggled between True and False

**Immutability Constraints**:
- Task ID is immutable once assigned
- All other fields (title, description, completed) are mutable via update operations

**State Diagram**:

```
┌─────────────┐
│   Created   │ (completed = False)
└──────┬──────┘
       │
       │ mark_complete()
       ▼
┌─────────────┐
│  Completed  │ (completed = True)
└──────┬──────┘
       │
       │ mark_incomplete()
       ▼
┌─────────────┐
│ Incomplete  │ (completed = False)
└─────────────┘
       ▲
       │
       └────────── Toggles between states ──────────┘
```

**Entity Lifecycle**:

1. **Creation**: Task is created with auto-generated ID, required title, optional description, and completed = False
2. **Active**: Task exists in memory and can be read, updated, or have status toggled
3. **Deleted**: Task is removed from memory and ID is retired (not reused in session)

**Relationships**:
- None (Task is a standalone entity with no relationships in Phase I)

---

## Storage Structure

### TaskStore

**Description**: In-memory storage container for all tasks in the current session.

**Implementation**: Dictionary mapping integer IDs to Task objects (`dict[int, Task]`)

**Structure**:
```python
{
    1: Task(id=1, title="Task 1", description="", completed=False),
    2: Task(id=2, title="Task 2", description="Details", completed=True),
    5: Task(id=5, title="Task 5", description="", completed=False)
}
```

**Characteristics**:
- Keys: Integer task IDs (sequential but may have gaps from deletions)
- Values: Task objects (frozen dataclass instances)
- Initialization: Empty dictionary (`{}`)
- Lifetime: Exists only during application runtime (lost on exit)

**Operations**:

| Operation | Complexity | Description |
|-----------|-----------|-------------|
| Add | O(1) | Insert new task with auto-generated ID |
| Get by ID | O(1) | Retrieve task by ID, raise TaskNotFoundError if missing |
| Update | O(1) | Update title/description by ID |
| Delete | O(1) | Remove task by ID |
| List all | O(n) | Return all tasks, sorted by ID |
| Filter by status | O(n) | Return tasks filtered by completed status |

**Concurrent Access**: Not applicable (single-threaded CLI application)

**Persistence**: None (data lost on application termination per FR-013)

---

## ID Generation Strategy

**Approach**: Sequential counter starting at 1

**Algorithm**:
```
1. Initialize counter to 1 at application start
2. When new task created:
   a. Assign current counter value as task ID
   b. Increment counter by 1
3. On delete: Do NOT decrement counter or reuse IDs
```

**Example Sequence**:
```
Action          | Counter | IDs in Storage
----------------|---------|----------------
Start           | 1       | {}
Add Task A      | 2       | {1: TaskA}
Add Task B      | 3       | {1: TaskA, 2: TaskB}
Delete Task 1   | 3       | {2: TaskB}
Add Task C      | 4       | {2: TaskB, 3: TaskC}  # ID 1 not reused
```

**Rationale**:
- Simple to implement (single integer counter)
- User-friendly (short, predictable IDs)
- Safe (no ID reuse prevents confusion within session)
- Sufficient for Phase I scope (no cross-session persistence)

**Constraints**:
- Counter never decrements
- Counter persists in memory only (resets on app restart)
- Maximum ID limited by Python integer size (effectively unlimited)

---

## Exception Types

Custom exceptions for domain-specific error handling:

### TaskNotFoundError

**Usage**: Raised when operation references non-existent task ID

**Scenarios**:
- Get: `task_manager.get(999)` when ID 999 doesn't exist
- Update: Attempting to update task with invalid ID
- Delete: Attempting to delete task with invalid ID
- Complete/Incomplete: Attempting to toggle status of non-existent task

**Message Format**: `"Task with ID {id} not found"`

---

### InvalidTaskError

**Usage**: Raised when task data violates validation rules (base class)

**Scenarios**:
- Title too long (> 200 chars)
- Description too long (> 1000 chars)

**Message Format**: `"Invalid task: {specific_reason}"`

---

### EmptyTitleError

**Usage**: Raised when task title is empty or whitespace-only (subclass of InvalidTaskError)

**Scenarios**:
- Add: `task_manager.add("")`
- Add: `task_manager.add("   ")`
- Update: Updating title to empty string

**Message Format**: `"Task title cannot be empty"`

---

## Validation Summary

**Entry Points**:
1. **CLI Layer**: Primary validation point for user input
   - Validates command arguments before calling TaskManager
   - Formats validation errors as user-friendly messages

2. **TaskManager**: Business rule enforcement
   - Validates task data consistency
   - Raises domain exceptions for violations

**Validation Flow**:
```
User Input
    ↓
CLI Validation (format, type, length)
    ↓ (if valid)
TaskManager Validation (business rules)
    ↓ (if valid)
Task Creation/Update
    ↓
In-Memory Storage
```

**Error Propagation**:
```
TaskManager raises Exception
    ↓
CLI catches Exception
    ↓
CLI formats error message
    ↓
Display to user via stderr
```

---

## Data Examples

### Valid Task Examples

```python
# Minimal task (title only)
Task(id=1, title="Buy groceries", description="", completed=False)

# Full task with description
Task(id=2, title="Review PR #42", description="Check code quality and tests", completed=False)

# Completed task
Task(id=3, title="Setup development environment", description="Install Python 3.13, uv, and pytest", completed=True)

# Task with Unicode
Task(id=4, title="学习中文", description="Practice characters: 你好世界", completed=False)

# Task with special characters
Task(id=5, title="Fix bug: null -> ''", description="Replace null with empty string in API", completed=False)
```

### Invalid Task Examples

```python
# Empty title (raises EmptyTitleError)
Task(id=1, title="", description="Details", completed=False)

# Whitespace-only title (raises EmptyTitleError)
Task(id=2, title="   ", description="Details", completed=False)

# Title too long (raises InvalidTaskError)
Task(id=3, title="A" * 201, description="", completed=False)

# Description too long (raises InvalidTaskError)
Task(id=4, title="Valid", description="B" * 1001, completed=False)
```

---

## Migration Notes (Phase I → Phase II)

**Phase II Changes**:
- Add database persistence (Neon Serverless PostgreSQL)
- Add SQLModel ORM models
- Add timestamp fields (created_at, updated_at)
- Add user_id field for multi-user support
- Change ID from int to UUID for global uniqueness

**Compatibility Strategy**:
- Phase I TaskManager interface remains stable
- Phase II adds DatabaseTaskManager implementing same interface
- Business logic (validation, state transitions) unchanged
- Tests updated to cover both in-memory and database implementations

**No Breaking Changes Required**:
- Task attributes (title, description, completed) remain the same
- Validation rules unchanged
- Exception types preserved
