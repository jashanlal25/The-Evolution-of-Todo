# CLI Interface Contract: Todo Application

**Date**: 2026-01-02
**Feature**: 001-todo-cli-app
**Purpose**: Define the command-line interface contract for the todo application

## Interface

The todo application provides a single menu-driven interface for task management.

**Entry Point**: `python -m src.cli.main` (or via `todo` command if installed)

**Description**: Interactive menu-based interface where users select numbered options (1-8) and are prompted for inputs. Tasks persist during the application runtime (single program session) and are lost when the application exits (Phase I Constitution compliance: in-memory only, no file system persistence).

**User Experience**:
- Single command to start application
- Numbered menu options (1-8) - no need to remember command syntax
- Guided prompts for all inputs
- Tasks remain in memory throughout the session
- Clear visual feedback with ✅ and ❌ indicators
- Session-based workflow: tasks available until user exits (Option 8)

**Exit Codes**:
- `0`: Success (normal exit via Option 8)
- `1`: User error (invalid input during operation)
- `2`: System error (unexpected failures)

---

## Menu-Driven Interface Specification

### Entry and Navigation

```bash
./todo-app
```

**Menu Display**:
```
============================================================
                    TODO CLI APPLICATION
============================================================

  1. Add Task
  2. View All Tasks
  3. Complete Task
  4. Update Task
  5. Mark as Incomplete
  6. Delete Task
  7. Clear All Tasks
  8. Exit

============================================================
Select option (1-8):
```

### Option 1: Add Task

**Prompts**:
```
--- Add New Task ---
Enter task title: <user input>
Enter description (optional, press Enter to skip): <user input>
```

**Success Output**:
```
✅ Task added successfully!
   ID: <id>
   Title: <title>
   Description: <description>
```

**Error Cases**:
- Empty title: `❌ Error: Title cannot be empty!`
- Title too long: `❌ Error: Task title cannot exceed 200 characters`
- Description too long: `❌ Error: Task description cannot exceed 1000 characters`

### Option 2: View All Tasks

**Output (with tasks)**:
```
--- All Tasks ---

Total tasks: <count>
ID | Title                          | Description                     | Status
---|--------------------------------|---------------------------------|------------
<id> | <title (max 30 chars)>       | <description (max 30 chars)>   | <Complete/Incomplete>
```

**Output (no tasks)**:
```
--- All Tasks ---

📝 No tasks found. Add a task to get started!
```

### Option 3: Complete Task

**Flow**:
1. Display all tasks (same as Option 2)
2. Prompt: `Enter task ID to mark as complete: <user input>`
3. Success: `✅ Task '<title>' marked as complete!`
4. Error: `❌ Error: Task with ID <id> not found` or `❌ Error: Please enter a valid number`

### Option 4: Update Task

**Flow**:
1. Display all tasks
2. Prompt: `Enter task ID to update: <user input>`
3. Show current task:
   ```
   Current title: <title>
   Current description: <description>
   ```
4. Prompts:
   ```
   Enter new title (press Enter to keep current): <user input>
   Enter new description (press Enter to keep current): <user input>
   ```
5. Success:
   ```
   ✅ Task updated successfully!
      ID: <id>
      Title: <title>
      Description: <description>
   ```
6. Error: `❌ No changes made.` (if both prompts skipped)

### Option 5: Mark as Incomplete

**Flow**:
1. Display all tasks
2. Prompt: `Enter task ID to mark as incomplete: <user input>`
3. Success: `✅ Task '<title>' marked as incomplete!`
4. Error: `❌ Error: Task with ID <id> not found`

### Option 6: Delete Task

**Flow**:
1. Display all tasks
2. Prompt: `Enter task ID to delete: <user input>`
3. Success: `✅ Task '<title>' deleted successfully!`
4. Error: `❌ Error: Task with ID <id> not found`

### Option 7: Clear All Tasks

**Flow**:
1. If no tasks: `📝 No tasks to clear.`
2. If tasks exist:
   - Prompt: `⚠️  Are you sure you want to delete all <count> tasks? (yes/no): <user input>`
   - If "yes": `✅ Cleared <count> task(s) successfully!`
   - If not "yes": `❌ Clear cancelled.`

### Option 8: Exit

**Output**: `👋 Goodbye! Your tasks are saved for next time.`

**Note**: Tasks are only saved during the current application run (in-memory). They are lost when the program exits (Phase I Constitution).

---

## Output Formatting Rules

### General Rules

1. **Width**: All output must fit within 80 characters
2. **Encoding**: UTF-8 encoding for Unicode support
3. **Line Endings**: Unix-style line endings (`\n`)
4. **Visual Indicators**: Use ✅ for success, ❌ for errors, 📝 for informational messages

### Success Messages

- Format: Structured output with clear indicators
- Example: `✅ Task added successfully!`

### Error Messages

- Format: `❌ Error: <message>`
- Must be actionable and user-friendly

### Table Formatting

```
ID | Title                          | Description                     | Status
---|--------------------------------|---------------------------------|------------
1  | Buy groceries                  |                                 | Incomplete
```

**Rules**:
- Column widths: ID (3), Title (30), Description (30), Status (12)
- Header separator: dashes (`---`)
- Truncation: Append `...` if text exceeds column width
- Alignment: Left-aligned text

---

## Validation Rules

All operations validate input before processing:

1. **Type Validation**: Ensure inputs match expected types (integers for IDs, strings for text)
2. **Range Validation**: Check length constraints (title ≤ 200 chars, description ≤ 1000 chars)
3. **Existence Validation**: Verify task ID exists for operations requiring it
4. **Business Rules**: Enforce non-empty titles, positive IDs

**Validation Order**:
1. Type and format (is it a valid integer?)
2. Range and constraints (is title within length?)
3. Existence and state (does task ID exist?)

---

## Performance Contract

All operations must complete within 5 seconds:
- User interactions should feel instant
- No noticeable delays for typical usage (up to 100 tasks)

**Expected Performance**:
- Menu display: Instant
- Add task: < 100ms
- View tasks: < 500ms (up to 1000 tasks)
- Update/Complete/Delete: < 100ms
- Clear all: < 100ms

---

## Compatibility Contract

**Python Version**: 3.13+
**Operating Systems**: Linux, macOS, Windows (WSL)
**Terminal**: Standard POSIX terminals, 80-character width minimum
**Encoding**: UTF-8 input and output

---

## Phase I Constraints (Constitution Compliance)

**Data Persistence**:
- ✅ Tasks stored in memory only
- ✅ No file system writes
- ✅ No databases
- ✅ Data lost on application exit

**Interface**:
- ✅ Console-only (no GUI, web, or API)
- ✅ Single menu-driven interface
- ✅ Clear user feedback for all operations

**Features** (exhaustive list):
1. Add Task
2. View All Tasks
3. Complete Task
4. Update Task
5. Mark as Incomplete
6. Delete Task
7. Clear All Tasks
8. Exit

No additional features permitted in Phase I.

