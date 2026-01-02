# Quickstart: Phase I Todo CLI App

**Date**: 2026-01-02
**Feature**: 001-todo-cli-app
**Purpose**: Fast-track guide for hackathon participants to set up and use the todo CLI application

## Prerequisites

- **Python**: Version 3.13 or higher
- **uv**: Python package installer (faster alternative to pip)
- **Operating System**: Linux, macOS, or Windows (with WSL)
- **Terminal**: 80-character width minimum

## Installation

### 1. Install Python 3.13+

Check your Python version:
```bash
python --version
```

If you need to install Python 3.13+:
- **macOS**: `brew install python@3.13`
- **Ubuntu/Debian**: `sudo apt install python3.13`
- **Windows**: Download from https://www.python.org/downloads/

### 2. Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### 3. Clone Repository

```bash
git clone <repository-url>
cd todo-cli-app
```

### 4. Install Dependencies

```bash
# Create virtual environment and install dev dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

**Expected time**: Under 2 minutes

## Usage

### Basic Commands

#### Add a Task

```bash
# Simple task with title only
python -m src.cli.main add "Buy groceries"

# Task with title and description
python -m src.cli.main add "Review PR #42" "Check code quality and run tests"
```

**Output**:
```
Task added successfully!
ID: 1
Title: Buy groceries
Description:
Status: Incomplete
```

#### List All Tasks

```bash
python -m src.cli.main list
```

**Output**:
```
ID | Title                          | Description                     | Status
---|--------------------------------|---------------------------------|------------
1  | Buy groceries                  |                                 | Incomplete
2  | Review PR #42                  | Check code quality and run t... | Complete
```

#### Mark Task as Complete

```bash
python -m src.cli.main complete 1
```

**Output**:
```
Task marked as complete!
ID: 1
Title: Buy groceries
```

#### Mark Task as Incomplete

```bash
python -m src.cli.main incomplete 1
```

**Output**:
```
Task marked as incomplete!
ID: 1
Title: Buy groceries
```

#### Update a Task

```bash
# Update title only
python -m src.cli.main update 1 --title "Buy groceries and cook dinner"

# Update description only
python -m src.cli.main update 2 --description "Detailed review notes"

# Update both
python -m src.cli.main update 1 --title "New title" --description "New description"
```

**Output**:
```
Task updated successfully!
ID: 1
Title: Buy groceries and cook dinner
Description:
Status: Incomplete
```

#### Delete a Task

```bash
python -m src.cli.main delete 1
```

**Output**:
```
Task deleted successfully!
ID: 1
Title: Buy groceries
```

### Getting Help

```bash
# General help
python -m src.cli.main --help

# Command-specific help
python -m src.cli.main add --help
python -m src.cli.main update --help
```

## Example Workflow

Here's a typical task management session:

```bash
# 1. Add some tasks
python -m src.cli.main add "Setup development environment" "Install Python, uv, and pytest"
python -m src.cli.main add "Write unit tests"
python -m src.cli.main add "Implement features"
python -m src.cli.main add "Run integration tests"

# 2. View all tasks
python -m src.cli.main list

# 3. Complete first task
python -m src.cli.main complete 1

# 4. Update a task with more details
python -m src.cli.main update 2 --description "Write unit tests for TaskManager and CLI"

# 5. View updated list
python -m src.cli.main list

# 6. Mark another task complete
python -m src.cli.main complete 2

# 7. Delete a task you no longer need
python -m src.cli.main delete 4

# 8. Final task list
python -m src.cli.main list
```

## Common Errors and Solutions

### Error: Task title cannot be empty

**Cause**: You provided an empty string or whitespace-only title

**Solution**: Provide a non-empty title
```bash
# Wrong
python -m src.cli.main add ""

# Correct
python -m src.cli.main add "My task"
```

### Error: Task with ID X not found

**Cause**: You referenced a task ID that doesn't exist (deleted or never created)

**Solution**: Run `python -m src.cli.main list` to see valid IDs
```bash
# Check existing tasks first
python -m src.cli.main list

# Then use a valid ID
python -m src.cli.main complete 2
```

### Error: Invalid task ID. Must be a positive integer

**Cause**: You provided a non-numeric or negative ID

**Solution**: Use positive integers only
```bash
# Wrong
python -m src.cli.main complete abc
python -m src.cli.main delete -1

# Correct
python -m src.cli.main complete 5
```

### Error: Task title cannot exceed 200 characters

**Cause**: Your title is too long

**Solution**: Use a shorter title and put details in description
```bash
# Wrong
python -m src.cli.main add "Very long title that exceeds 200 characters..."

# Correct
python -m src.cli.main add "Implement feature X" "Detailed description of the feature..."
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Suite

```bash
# Contract tests only
pytest tests/contract/

# Integration tests only
pytest tests/integration/
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Development Tools

### Code Formatting

```bash
# Format code with ruff
ruff format src/ tests/
```

### Linting

```bash
# Run ruff linter
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### Type Checking

```bash
# Run mypy type checker
mypy src/
```

### Pre-Commit Checks

Run all quality checks before committing:
```bash
# Format, lint, type check, and test
ruff format src/ tests/
ruff check --fix src/ tests/
mypy src/
pytest
```

## Data Persistence

**Important**: This is an in-memory application. All tasks are lost when you exit the program.

```bash
# Session 1
python -m src.cli.main add "Task 1"
python -m src.cli.main list  # Shows Task 1

# Exit and restart
exit

# Session 2
python -m src.cli.main list  # Empty list - Task 1 is gone
```

**Phase II** (coming soon) will add database persistence to retain tasks across sessions.

## Troubleshooting

### Python version issues

```bash
# Check Python version
python --version

# If using system Python 3.13+
python3.13 todo.py add "Task"

# Or create alias
alias python=python3.13
```

### Virtual environment issues

```bash
# Deactivate current environment
deactivate

# Remove and recreate
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Module execution

```bash
# Run as a module
python -m src.cli.main add "Task"

# Or install with pip and use the todo command
pip install -e .
todo add "Task"
```

## Performance Tips

- **Batch operations**: Add multiple tasks in sequence without delays
- **List filtering**: Use `list` command sparingly with many tasks (filters coming in Phase II)
- **Task limits**: Practical limit is ~10,000 tasks per session (beyond this, consider Phase II database version)

## Next Steps

- **Extend functionality**: Add your own features (priority levels, due dates, categories)
- **Improve UI**: Add colors, better table formatting, or rich text output
- **Add persistence**: Implement file-based storage as practice for Phase II
- **Build Phase II**: Migrate to web application with FastAPI and Next.js

## Support

**Documentation**:
- Full specification: `specs/001-todo-cli-app/spec.md`
- Implementation plan: `specs/001-todo-cli-app/plan.md`
- CLI contract: `specs/001-todo-cli-app/contracts/cli-interface.md`

**Issues**:
- Report bugs or request features via GitHub issues
- Check existing issues before creating new ones

**Community**:
- Join hackathon discussion channel
- Share your improvements and extensions

## Success Criteria Checklist

Verify your setup is working correctly:

- [ ] Installation completed in under 5 minutes
- [ ] Can add tasks and see confirmation instantly (< 5 seconds)
- [ ] Can view task list with all details
- [ ] Can complete all five operations (add, list, update, complete/incomplete, delete)
- [ ] Error messages are clear and actionable
- [ ] All CLI output fits in 80-character terminal
- [ ] Data persists during session but resets on restart

**All checked?** You're ready to build your todo workflow! 🎉
