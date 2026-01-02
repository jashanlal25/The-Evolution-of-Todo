# Todo CLI - Phase I

Phase I of "The Evolution of Todo" project: An in-memory command-line todo application built with Python.

## Overview

This is a simple, lightweight CLI tool for managing todo tasks. Tasks are stored in memory during command execution (no persistence across sessions in Phase I).

## Features

- ✅ Add tasks with title and description
- ✅ View all tasks in a formatted table
- ✅ Mark tasks as complete or incomplete
- ✅ Update task titles and descriptions
- ✅ Delete tasks
- ✅ Clear, user-friendly error messages
- ✅ 80-character terminal width compatibility

## Requirements

- Python 3.13 or higher
- uv package manager (recommended) or pip

## Installation

### Using uv (recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### Using pip

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

## Usage

After installation with `pip install -e .`, you can use either:
- `todo <command>` (if installed in editable mode)
- `python3 -m src.cli.main <command>` (module execution)

### Add a Task

```bash
# With title only
python3 src/cli/main.py add "Buy groceries"

# With title and description
python3 src/cli/main.py add "Review PR #42" "Check code quality and run tests"
```

### List All Tasks

```bash
python3 src/cli/main.py list
```

**Example Output**:
```
ID | Title                          | Description                     | Status
---|--------------------------------|---------------------------------|------------
1  | Buy groceries                  |                                 | Incomplete
2  | Review PR #42                  | Check code quality and run t... | Complete
```

### Mark Task as Complete

```bash
python3 src/cli/main.py complete 1
```

### Mark Task as Incomplete

```bash
python3 src/cli/main.py incomplete 1
```

### Update a Task

```bash
# Update title only
python3 src/cli/main.py update 1 --title "Buy groceries and cook dinner"

# Update description only
python3 src/cli/main.py update 2 --description "Detailed review notes"

# Update both
python3 src/cli/main.py update 1 --title "New title" --description "New description"
```

### Delete a Task

```bash
python3 src/cli/main.py delete 1
```

### Get Help

```bash
# General help
python3 src/cli/main.py --help

# Command-specific help
python3 src/cli/main.py add --help
python3 src/cli/main.py update --help
```

### Version Information

```bash
python3 src/cli/main.py --version
```

## Project Structure

```
.
├── src/
│   ├── models/          # Data models (Task, exceptions)
│   ├── services/        # Business logic (TaskManager)
│   ├── cli/
│   │   ├── main.py      # Main entry point
│   │   ├── commands.py  # CLI command handlers
│   │   ├── validators.py # Input validation
│   │   └── formatters.py # Output formatting
│   └── utils/           # Utility functions
├── tests/
│   ├── contract/        # Contract tests
│   └── integration/     # Integration tests
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
```

### Code Quality

```bash
# Format code
ruff format src/ tests/

# Lint code
ruff check src/ tests/

# Fix linting issues
ruff check --fix src/ tests/

# Type checking
mypy src/
```

## Important Notes

### Data Persistence

⚠️ **Phase I stores tasks in memory only**. All data is lost when you exit the application. Each command execution starts with an empty task list.

This is by design for Phase I. Phase II will add database persistence.

### Limitations

- No data persistence (tasks lost after each command)
- No file storage or database
- Single-user, single-session only
- Maximum 10,000 tasks per session (practical limit)

### Phase II Preview

The next phase will add:
- Database persistence (Neon Serverless PostgreSQL)
- Web interface (Next.js + FastAPI)
- Multi-user support
- Task history and timestamps

## Architecture

This application follows clean architecture principles:

- **Models Layer** (`src/models/`): Data entities (Task) and exceptions
- **Services Layer** (`src/services/`): Business logic (TaskManager)
- **CLI Layer** (`src/cli/`): User interface, validation, formatting
- **Separation of Concerns**: Each layer has clear responsibilities

### Design Patterns

- **Service Layer Pattern**: TaskManager abstracts storage and business logic
- **Immutable Entities**: Task is a frozen dataclass
- **Command Pattern**: Each CLI operation is a separate handler
- **Validation at Boundary**: CLI validates before calling service

## Contributing

This is a hackathon project following Spec-Driven Development (SDD) principles. All code is AI-generated from specifications.

## License

Phase I: Internal hackathon project

## Acknowledgments

Built with Claude Code and Spec-Kit Plus as part of "The Evolution of Todo" hackathon project.
