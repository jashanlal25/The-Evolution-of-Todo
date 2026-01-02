# Research: Phase I Todo CLI App

**Date**: 2026-01-02
**Feature**: 001-todo-cli-app
**Purpose**: Document architectural decisions and research findings for the in-memory Python todo CLI application

## Technical Decisions

### Decision 1: Task Identifier Strategy

**Decision**: Use auto-incremented integer IDs starting from 1

**Rationale**:
- Simplicity: Easy for users to remember and type (e.g., `todo complete 3`)
- Determinism: Predictable ID sequence aids in testing and debugging
- User-friendliness: Short numeric IDs are ideal for CLI interactions
- Memory efficiency: Integers consume less memory than UUIDs
- Session-scoped: Since data is not persisted across sessions, global uniqueness is unnecessary

**Alternatives Considered**:
1. **UUID (v4)**:
   - Pros: Globally unique, no collision risk
   - Cons: Long strings difficult to type in CLI (e.g., `todo complete 550e8400-e29b-41d4-a716-446655440000`), overkill for in-memory single-session use
   - Rejected because: User experience significantly worse for CLI interactions

2. **Hash-based IDs** (e.g., first 8 chars of title hash):
   - Pros: Semi-readable, collision-resistant
   - Cons: Not guaranteed unique, user cannot predict, harder to implement
   - Rejected because: Adds unnecessary complexity without clear benefit

**Consequences**:
- ID generation is trivial (increment counter)
- IDs are sequential and predictable
- Must handle ID reuse carefully if delete is implemented (do not reuse deleted IDs within session)

---

### Decision 2: CLI Command Structure

**Decision**: Use subcommand pattern with `argparse` (e.g., `python -m src.cli.main add "title" "description"`)

**Rationale**:
- Clarity: Each operation is a distinct subcommand (add, list, update, complete, incomplete, delete)
- Maintainability: Easy to extend with new commands
- Standard practice: Follows common CLI patterns (git, docker, kubectl)
- Pythonic: `argparse` subparsers provide excellent support for this pattern
- Self-documenting: `python -m src.cli.main --help` and `python -m src.cli.main add --help` provide built-in documentation

**Alternatives Considered**:
1. **Single command with flags** (e.g., `python -m src.cli.main --add "title" "description"`):
   - Pros: Single entry point
   - Cons: Becomes unwieldy with many operations, harder to read, conflicting flag names
   - Rejected because: Poor scalability and user experience with 5+ operations

2. **Interactive REPL** (prompt-based):
   - Pros: User-friendly for beginners
   - Cons: Harder to script, less efficient for power users, more complex to implement
   - Rejected because: Does not align with hackathon speed goals and standard CLI patterns

**Consequences**:
- Each operation gets its own subparser
- Help text automatically generated per command
- Easy to test each command independently
- May require wrapper script for convenience (e.g., `todo add` instead of `python -m src.cli.main add`)

---

### Decision 3: In-Memory Data Storage Structure

**Decision**: Use dictionary with integer keys mapping to Task objects (`dict[int, Task]`)

**Rationale**:
- O(1) lookup by ID for all operations (get, update, delete, complete)
- Natural mapping: ID → Task object
- Easy to iterate for list operations (`dict.values()`)
- Memory efficient for expected scale (< 1000 tasks per session)
- Pythonic: Dictionary is the standard choice for key-value storage

**Alternatives Considered**:
1. **List of Task objects** (`list[Task]`):
   - Pros: Simple, maintains insertion order naturally
   - Cons: O(n) lookup by ID, requires linear search for get/update/delete operations
   - Rejected because: Performance degrades with task count, awkward ID management

2. **Separate lists for complete/incomplete tasks**:
   - Pros: Fast filtering by status
   - Cons: Complex to maintain, moving tasks between lists error-prone, harder to implement update/delete
   - Rejected because: Over-optimization for simple use case, adds unnecessary complexity

**Consequences**:
- ID assignment needs separate counter (start at 1, increment for each new task)
- List command needs to sort by ID for consistent output
- Dictionary comprehension useful for filtering (e.g., completed tasks)
- Task deletion leaves gaps in ID sequence (acceptable for session scope)

---

### Decision 4: Testing Strategy

**Decision**: Contract testing with pytest focusing on CLI command interface

**Rationale**:
- Contract tests validate the CLI commands match specification requirements
- Integration approach tests the full stack (CLI → TaskManager → in-memory storage)
- Pytest provides excellent CLI testing support with `subprocess` or `click.testing.CliRunner`
- Aligns with SDD: tests validate requirements from spec.md
- Sufficient for Phase I scope (more granular unit tests can be added in later phases)

**Testing Approach**:
1. **Contract Tests** (tests/contract/):
   - Test each CLI subcommand (add, list, update, complete, incomplete, delete)
   - Validate output format, success/error messages
   - Test edge cases from spec (empty title, invalid ID, etc.)
   - Run actual CLI commands and assert on stdout/stderr

2. **Integration Tests** (tests/integration/):
   - Test command sequences (add → list → complete → list)
   - Validate state persistence within session
   - Test error handling across commands

**Alternatives Considered**:
1. **Unit tests for TaskManager class**:
   - Pros: Granular, fast
   - Cons: Tests implementation details, not user requirements
   - Decision: Include as optional complement, not primary strategy

2. **Manual testing only**:
   - Pros: Fast initial development
   - Cons: Not repeatable, violates TDD principle from constitution
   - Rejected because: Constitution requires tests before implementation

**Consequences**:
- Tests written before implementation (Red → Green → Refactor)
- Test files mirror CLI commands
- CI/CD ready (tests can run in automation)
- Clear pass/fail criteria from spec requirements

---

### Decision 5: Project Structure

**Decision**: Single project structure under `src/` with clear separation of concerns

**Rationale**:
- Phase I scope is small (CLI-only, no web/mobile components)
- Follows constitution principle of separation of concerns
- Easy to navigate for hackathon participants
- Prepares for Phase II migration (business logic in `services/` can be reused)

**Structure**:
```
src/
├── models/          # Task data model (business entities)
├── services/        # TaskManager (business logic, storage abstraction)
├── cli/             # CLI interface (argparse commands, formatters)
└── utils/           # Helpers (ID generation, input validation)

tests/
├── contract/        # CLI contract tests
└── integration/     # Multi-command integration tests
```

**Layer Responsibilities**:
- `models/`: Task class definition (data structure only, no logic)
- `services/`: TaskManager class (add, get, update, delete, list operations on in-memory dict)
- `cli/`: Command handlers, argument parsing, output formatting
- `utils/`: ID generation, validation functions

**Alternatives Considered**:
1. **Flat structure** (all in one file):
   - Pros: Simple for small project
   - Cons: Violates separation of concerns, hard to test, poor Phase II migration path
   - Rejected because: Constitution requires separation of concerns

2. **Over-engineered layers** (repositories, DTOs, use cases):
   - Pros: Enterprise-grade separation
   - Cons: Overkill for Phase I, violates YAGNI principle
   - Rejected because: Complexity not justified for in-memory CLI app

**Consequences**:
- Clear boundaries between presentation (CLI), business logic (TaskManager), and data (Task model)
- Easy to mock TaskManager for CLI tests
- Business logic (TaskManager) can be extracted to FastAPI in Phase II
- Each layer can be tested independently

---

### Decision 6: Python Tooling and Dependencies

**Decision**:
- **Python version**: 3.13+ (per constitution)
- **Package manager**: uv (per constitution)
- **CLI framework**: argparse (standard library, zero dependencies)
- **Testing framework**: pytest
- **Code quality**: ruff (linting + formatting)
- **Type checking**: mypy with strict mode

**Rationale**:
- Minimal dependencies: argparse is built-in, reduces setup complexity
- Modern Python: 3.13 provides latest performance and type hints
- Fast tooling: uv is significantly faster than pip for dependency resolution
- Quality gates: ruff + mypy enforce code standards before commit
- Constitution alignment: Follows Phase I technology constraints

**Dependencies** (pyproject.toml):
```toml
[project]
requires-python = ">=3.13"
dependencies = []  # No runtime dependencies (argparse is stdlib)

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "mypy>=1.8",
    "ruff>=0.1"
]
```

**Alternatives Considered**:
1. **Click library** for CLI:
   - Pros: More features, decorators, better help formatting
   - Cons: External dependency, overkill for simple CRUD commands
   - Rejected because: argparse sufficient, minimizes dependencies

2. **Poetry** instead of uv:
   - Pros: More mature, widely adopted
   - Cons: Slower than uv, constitution specifies uv
   - Rejected because: Constitution mandates uv

**Consequences**:
- Zero runtime dependencies
- Fast installation with uv
- Type safety enforced by mypy
- Consistent code style via ruff
- All tools compatible with CI/CD

---

### Decision 7: Error Handling and Validation

**Decision**: Centralized validation in CLI layer with custom exception types

**Rationale**:
- Input validation happens at CLI boundary (validate before calling TaskManager)
- TaskManager raises custom exceptions (TaskNotFoundError, InvalidTaskError)
- CLI layer catches exceptions and formats user-friendly error messages
- Aligns with requirement FR-009 and FR-010 (clear error messages, input validation)

**Error Types**:
```python
class TaskNotFoundError(Exception): pass
class InvalidTaskError(Exception): pass
class EmptyTitleError(InvalidTaskError): pass
```

**Validation Rules**:
- Title: Required, non-empty after strip(), max length 200 chars
- Description: Optional, max length 1000 chars
- Task ID: Must be positive integer, must exist in storage

**Alternatives Considered**:
1. **Validation in TaskManager**:
   - Pros: Centralized business rules
   - Cons: Mixes presentation concerns with business logic
   - Rejected because: CLI is responsible for user input validation

2. **Pydantic models**:
   - Pros: Declarative validation, excellent error messages
   - Cons: Additional dependency, overkill for simple validation
   - Rejected because: Avoid dependencies for Phase I simplicity

**Consequences**:
- CLI layer is responsible for validation and error formatting
- TaskManager assumes valid inputs (can add assertions for safety)
- Clear error messages at presentation layer
- Easy to test validation separately

---

## Research Findings

### Python 3.13 Best Practices for CLI Applications

**Key Findings**:
1. **Type Hints**: Use PEP 695 type parameter syntax for generic types
2. **Error Groups**: ExceptionGroup for handling multiple validation errors
3. **Pattern Matching**: Use match/case for command routing (cleaner than if/elif)
4. **Dataclasses**: Use `@dataclass` for Task model (automatic __init__, __repr__)
5. **Context Managers**: Use `@contextmanager` if file persistence added in future

**Applied to Design**:
- Task model will use `@dataclass(frozen=True, slots=True)` for immutability and memory efficiency
- CLI router can use pattern matching for subcommand dispatch
- Type hints throughout with `dict[int, Task]` syntax

---

### In-Memory Storage Best Practices

**Key Findings**:
1. **Thread Safety**: Not required for single-threaded CLI app
2. **Memory Limits**: Python dict can handle millions of entries efficiently
3. **ID Generation**: Simple counter is sufficient, no need for UUID library
4. **Iteration Order**: Dict maintains insertion order since Python 3.7+

**Applied to Design**:
- No thread locking needed
- No memory limits enforced (trust OS limits)
- Simple counter-based ID generation
- Can rely on dict iteration order for consistent list output

---

### Testing CLI Applications with Pytest

**Key Findings**:
1. **Subprocess vs CliRunner**: subprocess tests end-to-end, CliRunner tests programmatically
2. **Fixtures**: Use pytest fixtures for setup/teardown of TaskManager state
3. **Parametrize**: Use `@pytest.mark.parametrize` for edge cases
4. **Capsys**: Use `capsys` fixture to capture stdout/stderr

**Applied to Design**:
- Use subprocess for contract tests (full CLI execution)
- Use fixtures to reset TaskManager state between tests
- Parametrize edge cases (empty title, invalid ID, long strings)
- Assert on captured output for format validation

---

## Open Questions

None - all technical decisions resolved for Phase I scope.

---

## References

- Constitution: `.specify/memory/constitution.md` (Phase I constraints)
- Feature Spec: `specs/001-todo-cli-app/spec.md` (requirements and success criteria)
- Python 3.13 Documentation: https://docs.python.org/3.13/
- Argparse Tutorial: https://docs.python.org/3/howto/argparse.html
- Pytest Documentation: https://docs.pytest.org/
