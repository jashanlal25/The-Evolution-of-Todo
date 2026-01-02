# Implementation Plan: Phase I Todo CLI App

**Branch**: `001-todo-cli-app` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an in-memory command-line todo application in Python that allows users to manage tasks through five core operations: add, list, update, mark complete/incomplete, and delete. The application stores tasks in memory using Python data structures with no persistence, providing a simple CLI interface for hackathon participants to track their work. This serves as Phase I of "The Evolution of Todo" project, establishing the foundation for later phases with web interfaces, databases, and cloud deployment.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (argparse is standard library)
**Storage**: In-memory dictionary (`dict[int, Task]`), no persistence
**Testing**: pytest with contract and integration tests
**Target Platform**: Linux, macOS, Windows (WSL) - cross-platform CLI
**Project Type**: single (console application)
**Performance Goals**: All operations complete in < 5 seconds, add/update/delete in < 100ms, list in < 500ms
**Constraints**: 80-character terminal width, UTF-8 encoding, no external dependencies for runtime
**Scale/Scope**: Up to 10,000 tasks per session (in-memory limit)

**Development Tools**:
- **Package Manager**: uv (fast Python package installer)
- **Code Quality**: ruff (linting + formatting)
- **Type Checking**: mypy with strict mode
- **Testing**: pytest, pytest-cov

**Zero Runtime Dependencies**: argparse (CLI framework) is Python standard library

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development (SDD) is Supreme ✅

**Status**: PASS

**Evidence**:
- Feature has complete spec.md with user stories, requirements, and success criteria
- Implementation plan (this file) created from spec
- Tasks.md will be generated from this plan before implementation
- All code will be AI-generated from these specifications

**Compliance**: Full compliance. All development originates from approved specifications.

---

### Principle II: Human as Architect, AI as Implementer ✅

**Status**: PASS

**Evidence**:
- Human architect defined requirements and acceptance criteria in spec.md
- AI (Claude Code) will generate all implementation code
- Architectural decisions documented in research.md with human review
- No manual coding permitted per constitution

**Compliance**: Full compliance. Human provides architecture, AI generates code.

---

### Principle III: Sequential Phase Completion ✅

**Status**: PASS

**Evidence**:
- This is Phase I (first phase of five)
- No dependencies on future phases
- Phase II will build on Phase I foundation (TaskManager → FastAPI)
- Phase completion requires all tests passing and ADR creation

**Compliance**: Full compliance. Building Phase I from scratch with clean foundation.

---

### Principle IV: Architectural Clarity and Documentation ✅

**Status**: PASS

**Evidence**:
- research.md documents 7 architectural decisions with rationale and alternatives
- data-model.md defines Task entity and validation rules
- contracts/ contains CLI and TaskManager service contracts
- No implicit dependencies or undocumented assumptions

**Architectural Decisions Documented**:
1. Task identifier strategy (auto-increment vs UUID)
2. CLI command structure (subcommands vs flags)
3. Data storage structure (dict vs list)
4. Testing strategy (contract tests with pytest)
5. Project structure (separation of concerns)
6. Python tooling and dependencies (uv, ruff, mypy)
7. Error handling and validation approach

**Compliance**: Full compliance. All significant decisions explicitly documented.

---

### Principle V: Separation of Concerns ✅

**Status**: PASS

**Evidence**:

**Layer Structure**:
```
src/
├── models/      # Task data model (entities only, no logic)
├── services/    # TaskManager (business logic, storage abstraction)
├── cli/         # CLI interface (argparse, formatters)
└── utils/       # ID generation, validation helpers
```

**Clear Boundaries**:
- **Presentation (CLI)**: Input validation, argument parsing, output formatting
- **Business Logic (TaskManager)**: Task operations, business rules enforcement
- **Data (Task model)**: Immutable data structures, no behavior
- **Cross-cutting (utils)**: ID generation, validation functions

**Abstraction Enforcement**:
- CLI depends on TaskManager interface, not implementation details
- TaskManager operates on Task entities, not storage specifics
- Task model is frozen dataclass (immutable, no methods)

**Compliance**: Full compliance. Clean layer separation with explicit boundaries.

---

### Principle VI: Test-Driven Development (TDD) ✅

**Status**: PASS

**Evidence**:

**Test Strategy** (from research.md):
1. **Contract Tests** (tests/contract/): Validate CLI commands match spec requirements
2. **Integration Tests** (tests/integration/): Validate command sequences and state

**TDD Workflow**:
- Phase: Red → Write failing tests based on contracts
- Phase: Green → Implement code to pass tests
- Phase: Refactor → Improve code while keeping tests green

**Test Coverage Requirements**:
- Contract tests for all public APIs (CLI commands, TaskManager methods)
- Integration tests for all user journeys (P1-P4 from spec)
- Tests validate requirements directly from spec.md

**Compliance**: Full compliance. Tests written before implementation, validating spec requirements.

---

### Principle VII: Determinism and Reproducibility ✅

**Status**: PASS

**Evidence**:

**Deterministic Behavior**:
- ID generation is sequential counter (predictable, testable)
- No random elements in task management
- All dependencies explicitly versioned in pyproject.toml
- Configuration externalized (if needed in future phases)

**Reproducibility**:
- Specification complete and unambiguous
- All decisions documented in research.md
- PHRs will record AI prompts and responses
- uv.lock ensures exact dependency versions

**Version Control**:
- All specs, plans, and code in git
- No environment-specific hardcoded values
- Build process scripted (uv venv + uv pip install)

**Compliance**: Full compliance. Implementation is deterministic and reproducible from specs.

---

### Gate Evaluation

**All Principles**: ✅ PASS

**Decision**: Proceed to implementation (Phase 0 and Phase 1 complete)

**Post-Design Re-Evaluation**: All principles remain compliant after design phase. No violations detected.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-app/
├── spec.md              # User stories, requirements, success criteria (/sp.specify output)
├── plan.md              # This file - implementation plan (/sp.plan output)
├── research.md          # Architectural decisions and research findings (Phase 0 output)
├── data-model.md        # Task entity definition and validation (Phase 1 output)
├── quickstart.md        # Setup and usage guide for participants (Phase 1 output)
├── contracts/           # Interface contracts (Phase 1 output)
│   ├── cli-interface.md          # CLI command specifications
│   └── task-manager-service.md   # TaskManager service contract
└── tasks.md             # Executable tasks (Phase 2 - /sp.tasks command, NOT YET CREATED)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── task.py          # Task dataclass entity
│   └── exceptions.py    # Custom exception types (TaskNotFoundError, etc.)
├── services/
│   ├── __init__.py
│   └── task_manager.py  # TaskManager business logic and in-memory storage
├── cli/
│   ├── __init__.py
│   ├── main.py          # Main entry point (parses args, dispatches to CLI commands)
│   ├── commands.py      # CLI command handlers (add, list, update, etc.)
│   ├── formatters.py    # Output formatting (tables, messages)
│   └── validators.py    # Input validation functions
└── utils/
    ├── __init__.py
    └── id_generator.py  # ID counter management

tests/
├── __init__.py
├── contract/
│   ├── __init__.py
│   ├── test_cli_add.py       # Contract tests for 'add' command
│   ├── test_cli_list.py      # Contract tests for 'list' command
│   ├── test_cli_update.py    # Contract tests for 'update' command
│   ├── test_cli_complete.py  # Contract tests for 'complete/incomplete' commands
│   ├── test_cli_delete.py    # Contract tests for 'delete' command
│   └── test_task_manager.py  # Contract tests for TaskManager service
└── integration/
    ├── __init__.py
    └── test_user_journeys.py # Integration tests for P1-P4 user stories

pyproject.toml           # Project metadata and dependencies (with entry point: todo)
uv.lock                  # Locked dependency versions
README.md                # Project overview and setup instructions
.gitignore               # Git ignore rules
```

**Structure Decision**: Selected **single project structure** (Option 1) because:
- Phase I is CLI-only with no web or mobile components
- Simple, flat structure suitable for small codebase (<1000 LOC)
- Clear separation of concerns across models/, services/, cli/, utils/
- Easy to navigate for hackathon participants
- Prepares for Phase II migration (services/ can be extracted to FastAPI backend)

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All constitution principles are compliant with Phase I design.

This section is intentionally empty.

---

## Architecture Overview

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    User (Terminal)                        │
└────────────────────┬─────────────────────────────────────┘
                     │ Commands (stdin)
                     │ Output (stdout/stderr)
                     ▼
┌──────────────────────────────────────────────────────────┐
│              src/cli/main.py (Entry Point)                │
│  - Parses CLI arguments with argparse                     │
│  - Routes to appropriate command handler                  │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│                 CLI Layer (src/cli/)                      │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ commands.py: Command handlers                       │ │
│  │  - add_command(), list_command(), update_command()  │ │
│  │  - complete_command(), incomplete_command()         │ │
│  │  - delete_command()                                 │ │
│  └────────┬────────────────────────────────────────────┘ │
│           │                                               │
│  ┌────────▼───────────────────────────┐ ┌──────────────┐ │
│  │ validators.py: Input validation    │ │ formatters.py│ │
│  │  - validate_title(), validate_id() │ │  - Table fmt │ │
│  └────────────────────────────────────┘ └──────────────┘ │
└────────────────────┬─────────────────────────────────────┘
                     │ Calls business logic
                     ▼
┌──────────────────────────────────────────────────────────┐
│              Business Logic (src/services/)               │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ task_manager.py: TaskManager                        │ │
│  │  - add(title, desc) -> Task                         │ │
│  │  - get(id) -> Task                                  │ │
│  │  - update(id, title, desc) -> Task                  │ │
│  │  - mark_complete(id) -> Task                        │ │
│  │  - mark_incomplete(id) -> Task                      │ │
│  │  - delete(id) -> Task                               │ │
│  │  - list_all() -> list[Task]                         │ │
│  │                                                      │ │
│  │ Storage: dict[int, Task]                            │ │
│  │ ID Counter: int (starts at 1)                       │ │
│  └────────┬────────────────────────────────────────────┘ │
└───────────┼──────────────────────────────────────────────┘
            │ Uses entities
            ▼
┌──────────────────────────────────────────────────────────┐
│                Data Layer (src/models/)                   │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ task.py: Task dataclass                             │ │
│  │  @dataclass(frozen=True, slots=True)                │ │
│  │  - id: int                                          │ │
│  │  - title: str                                       │ │
│  │  - description: str                                 │ │
│  │  - completed: bool                                  │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ exceptions.py: Custom exceptions                    │ │
│  │  - TaskNotFoundError                                │ │
│  │  - InvalidTaskError                                 │ │
│  │  - EmptyTitleError                                  │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

### Data Flow

**Add Task Flow**:
```
User: python -m src.cli.main add "Title" "Description"
  │
  ├─> src/cli/main.py: Parse arguments
  │
  ├─> cli.commands.add_command(args)
  │   ├─> cli.validators.validate_title("Title")  # Check length, non-empty
  │   ├─> cli.validators.validate_description("Description")  # Check length
  │   └─> task_manager.add("Title", "Description")
  │       ├─> Generate ID (counter++)
  │       ├─> Create Task(id, title, desc, completed=False)
  │       ├─> Store in dict: storage[id] = task
  │       └─> Return Task
  │
  └─> cli.formatters.format_task_added(task)
      └─> Print to stdout
```

**List Tasks Flow**:
```
User: python -m src.cli.main list
  │
  ├─> src/cli/main.py: Parse arguments
  │
  ├─> cli.commands.list_command(args)
  │   └─> task_manager.list_all()
  │       ├─> Get all tasks from dict.values()
  │       ├─> Sort by ID
  │       └─> Return list[Task]
  │
  └─> cli.formatters.format_task_table(tasks)
      ├─> Build table with columns: ID, Title, Description, Status
      ├─> Truncate long text to fit 80-char width
      └─> Print to stdout
```

**Update Task Flow**:
```
User: python -m src.cli.main update 1 --title "New Title"
  │
  ├─> src/cli/main.py: Parse arguments
  │
  ├─> cli.commands.update_command(args)
  │   ├─> cli.validators.validate_id(1)  # Check positive integer
  │   ├─> cli.validators.validate_title("New Title")  # If provided
  │   └─> task_manager.update(1, title="New Title")
  │       ├─> Get existing task from dict (or raise TaskNotFoundError)
  │       ├─> Create new Task with updated title (frozen dataclass)
  │       ├─> Replace in dict: storage[1] = new_task
  │       └─> Return Task
  │
  └─> cli.formatters.format_task_updated(task)
      └─> Print to stdout
```

**Error Handling Flow**:
```
User: python -m src.cli.main complete 999  # Non-existent ID
  │
  ├─> src/cli/main.py: Parse arguments
  │
  ├─> cli.commands.complete_command(args)
  │   └─> task_manager.mark_complete(999)
  │       └─> Raise TaskNotFoundError(999)
  │
  └─> CLI catches exception
      └─> Print "Error: Task with ID 999 not found" to stderr
      └─> Exit with code 1
```

### Key Design Patterns

1. **Service Layer Pattern**: TaskManager abstracts storage and business logic
2. **Immutable Entities**: Task is frozen dataclass (updates create new instances)
3. **Command Pattern**: Each CLI subcommand is a separate handler function
4. **Validation at Boundary**: CLI layer validates input before calling service
5. **Exception-Based Error Handling**: Service raises domain exceptions, CLI formats messages

---

## Implementation Phases

### Phase 0: Research ✅ COMPLETE

**Deliverable**: `research.md`

**Content**:
- 7 architectural decisions documented with rationale and alternatives
- Python 3.13 best practices research
- In-memory storage patterns research
- CLI testing strategies with pytest

**Status**: Complete (file created)

---

### Phase 1: Design & Contracts ✅ COMPLETE

**Deliverables**:
- `data-model.md`: Task entity definition, validation rules, state transitions
- `contracts/cli-interface.md`: CLI command specifications with examples and error cases
- `contracts/task-manager-service.md`: TaskManager method signatures and contracts
- `quickstart.md`: Setup and usage guide for hackathon participants

**Status**: Complete (all files created)

**Agent Context**: Updated CLAUDE.md with Phase I database info (in-memory)

---

### Phase 2: Task Generation (NEXT STEP)

**Command**: `/sp.tasks`

**Deliverable**: `tasks.md`

**Content**:
- Foundational tasks (project setup, dependencies, structure)
- P1 tasks (Add and View Tasks)
- P2 tasks (Mark Complete/Incomplete)
- P3 tasks (Update Task Details)
- P4 tasks (Delete Tasks)
- Each task with exact file paths, acceptance tests, and dependencies

**Status**: NOT YET STARTED (awaiting `/sp.tasks` command)

---

### Phase 3: Implementation (FUTURE)

**Commands**: `/sp.implement` (Red → Green → Refactor)

**Deliverables**:
- Source code in `src/`
- Tests in `tests/`
- All tests passing
- All acceptance criteria met

**Status**: NOT YET STARTED (after tasks.md)

---

## Testing Strategy

### Test Pyramid

```
         /\
        /  \        Unit Tests (Optional)
       /    \       - TaskManager methods
      /      \      - Validation functions
     /--------\
    /          \    Integration Tests
   /            \   - User journey sequences
  /              \  - Multi-command workflows
 /----------------\
/                  \ Contract Tests (Primary)
--------------------
 CLI commands        TaskManager service
 (subprocess)        (direct method calls)
```

### Contract Tests (Primary Focus)

**Location**: `tests/contract/`

**Coverage**:
- `test_cli_add.py`: Add command with all success/error cases
- `test_cli_list.py`: List command with empty/populated states
- `test_cli_update.py`: Update command with title/description variations
- `test_cli_complete.py`: Complete/incomplete commands
- `test_cli_delete.py`: Delete command
- `test_task_manager.py`: TaskManager methods (add, get, update, delete, list, etc.)

**Approach**:
- Use subprocess to execute CLI commands (end-to-end)
- Assert on stdout/stderr output
- Validate exit codes
- Test all edge cases from spec (empty title, long strings, invalid IDs, Unicode, etc.)

**Example Test**:
```python
def test_add_task_success():
    """Test adding a task with title and description."""
    result = subprocess.run(
        ["python", "-m", "src.cli.main", "add", "Buy groceries", "Milk and bread"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Task added successfully!" in result.stdout
    assert "ID: 1" in result.stdout
    assert "Title: Buy groceries" in result.stdout
    assert "Description: Milk and bread" in result.stdout
    assert "Status: Incomplete" in result.stdout
```

### Integration Tests

**Location**: `tests/integration/`

**Coverage**:
- `test_user_journeys.py`: P1-P4 user stories from spec
  - Add → List → Complete → List
  - Add → Update → List
  - Add → Delete → List
  - Multiple tasks with various operations

**Approach**:
- Test command sequences that represent real user workflows
- Validate state persistence within session
- Ensure operations compose correctly

### Test Execution

**Run All Tests**:
```bash
pytest
```

**Run Specific Suite**:
```bash
pytest tests/contract/  # Contract tests only
pytest tests/integration/  # Integration tests only
```

**With Coverage**:
```bash
pytest --cov=src --cov-report=html
```

**Coverage Target**: 100% of public interfaces (CLI commands, TaskManager methods)

---

## Acceptance Criteria

Phase I implementation is complete when:

### Functional Completeness ✅

- [ ] All 5 core operations implemented (add, list, update, complete/incomplete, delete)
- [ ] All user stories (P1-P4) functional and tested
- [ ] All functional requirements (FR-001 to FR-013) satisfied
- [ ] All edge cases handled correctly

### Technical Quality ✅

- [ ] All contract tests passing (CLI commands, TaskManager service)
- [ ] All integration tests passing (user journeys)
- [ ] Code generated by AI from specifications (no manual coding)
- [ ] Ruff linting passing (no warnings)
- [ ] Mypy type checking passing (strict mode)
- [ ] Code coverage ≥ 90% for src/

### User Experience ✅

- [ ] Setup completes in under 5 minutes (SC-005)
- [ ] All operations complete in under 5 seconds (SC-001)
- [ ] Error messages clear and actionable (SC-004)
- [ ] CLI output fits in 80-character terminal (SC-007)
- [ ] Tasks persist during session, reset on exit (SC-006)

### Documentation ✅

- [ ] README.md with setup and usage instructions
- [ ] Quickstart.md for fast onboarding
- [ ] All CLI commands have --help text
- [ ] Code includes docstrings for public interfaces

### Constitutional Compliance ✅

- [ ] All code AI-generated from specifications (Principle II)
- [ ] All tests written before implementation (Principle VI)
- [ ] Separation of concerns enforced (Principle V)
- [ ] All architectural decisions documented (Principle IV)
- [ ] PHR created for implementation work (Principle VII)

### Phase Completion ✅

- [ ] Human architect approval obtained
- [ ] Phase retrospective completed
- [ ] ADR created if significant decisions made during implementation
- [ ] Ready for Phase II migration planning

---

## Migration Path to Phase II

### What Stays the Same

1. **Business Logic**: TaskManager interface unchanged
2. **Data Model**: Task attributes (title, description, completed) preserved
3. **Validation Rules**: Same length limits and error handling
4. **User Stories**: P1-P4 functionality remains

### What Changes in Phase II

1. **Storage**: In-memory dict → Neon Serverless PostgreSQL + SQLModel
2. **ID Type**: int → UUID for global uniqueness
3. **Additional Fields**: created_at, updated_at timestamps
4. **CLI**: Becomes optional, web UI primary interface
5. **Technology Stack**: Add Next.js (frontend) + FastAPI (backend)

### Migration Strategy

**Code Reuse**:
```python
# Phase I (in-memory)
from src.services.task_manager import TaskManager
task_manager = TaskManager()

# Phase II (database)
from src.services.database_task_manager import DatabaseTaskManager
task_manager = DatabaseTaskManager(db_session)

# Same interface, different implementation
task = task_manager.add("Title", "Description")
```

**Test Reuse**:
- Contract tests remain valid for both implementations
- Add new tests for database-specific concerns (transactions, concurrency)

**Clean Transition**:
- Phase I serves as working prototype
- Phase II adds persistence layer without breaking business logic
- Users can migrate from CLI to web UI gradually

---

## Risk Analysis

### Risk 1: Unicode Handling in CLI

**Likelihood**: Medium
**Impact**: Low
**Mitigation**:
- Use UTF-8 encoding explicitly in CLI output
- Test with Unicode characters in contract tests
- Document encoding requirements in README

### Risk 2: Terminal Width Variations

**Likelihood**: Medium
**Impact**: Low
**Mitigation**:
- Design table formatter for 80-character width
- Truncate long text with ellipsis
- Test on various terminal sizes

### Risk 3: Windows Compatibility

**Likelihood**: Low (WSL recommended)
**Impact**: Medium
**Mitigation**:
- Document WSL as preferred environment for Windows
- Test on Windows WSL during validation
- Provide troubleshooting guide in quickstart.md

### Risk 4: Memory Limits for Large Task Lists

**Likelihood**: Low
**Impact**: Low
**Mitigation**:
- Document practical limit (~10,000 tasks)
- Phase II adds database for larger scales
- In-memory is sufficient for hackathon use case

### Risk 5: ID Exhaustion

**Likelihood**: Very Low
**Impact**: Very Low
**Mitigation**:
- Python integers effectively unlimited
- Counter reset on session restart
- Not a concern for Phase I scope

---

## Architectural Decision Record (ADR) Candidates

After implementation, consider creating ADRs for:

1. **ADR-001: CLI Framework Selection** (argparse vs Click)
   - **If**: Implementation reveals significant argparse limitations
   - **Trigger**: Difficulty implementing help text or subcommand routing

2. **ADR-002: Immutable Task Entities** (frozen dataclass vs mutable class)
   - **If**: Immutability causes performance or usability issues
   - **Trigger**: High memory overhead or complex update patterns

3. **ADR-003: In-Memory Storage Structure** (dict vs alternative)
   - **If**: Dictionary proves insufficient for operations
   - **Trigger**: Performance issues or complex filtering requirements

**Note**: These are *potential* ADRs. Only create if implementation reveals significant tradeoffs or decisions that affect system design.

---

## Next Steps

1. **Run `/sp.tasks`** to generate tasks.md with dependency-ordered implementation tasks
2. **Review tasks.md** for completeness and accuracy
3. **Run `/sp.implement`** to begin TDD implementation (Red → Green → Refactor)
4. **Validate acceptance criteria** against spec.md requirements
5. **Create PHR** for planning work
6. **Human architect approval** before proceeding to implementation
7. **Create ADR** if significant decisions made during implementation

---

## References

- **Specification**: [specs/001-todo-cli-app/spec.md](./spec.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Research**: [specs/001-todo-cli-app/research.md](./research.md)
- **Data Model**: [specs/001-todo-cli-app/data-model.md](./data-model.md)
- **CLI Contract**: [specs/001-todo-cli-app/contracts/cli-interface.md](./contracts/cli-interface.md)
- **Service Contract**: [specs/001-todo-cli-app/contracts/task-manager-service.md](./contracts/task-manager-service.md)
- **Quickstart**: [specs/001-todo-cli-app/quickstart.md](./quickstart.md)
