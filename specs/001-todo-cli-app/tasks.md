# Tasks: Phase I Todo CLI App

**Input**: Design documents from `/specs/001-todo-cli-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included per constitution requirement for TDD (Test-Driven Development)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (per plan.md)
- All paths are absolute from repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan (src/, tests/, pyproject.toml)
- [ ] T002 Initialize Python 3.13+ project with uv and dependencies (pytest, ruff, mypy)
- [ ] T003 [P] Configure ruff linting and formatting in pyproject.toml
- [ ] T004 [P] Configure mypy type checking with strict mode in pyproject.toml
- [ ] T005 [P] Create .gitignore for Python projects

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 [P] Create Task dataclass model in src/models/task.py with frozen=True, slots=True
- [ ] T007 [P] Create custom exception classes in src/models/exceptions.py (TaskNotFoundError, InvalidTaskError, EmptyTitleError)
- [ ] T008 Create TaskManager service skeleton in src/services/task_manager.py with __init__, storage dict, and ID counter
- [ ] T009 [P] Create CLI validators module in src/cli/validators.py (validate_title, validate_description, validate_id stubs)
- [ ] T010 [P] Create CLI formatters module in src/cli/formatters.py (format_task_added, format_task_table stubs)
- [ ] T011 Create CLI commands module skeleton in src/cli/commands.py (empty command handler functions)
- [ ] T012 Create main entry point src/cli/main.py with argparse setup and subcommand routing structure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title/description and view all tasks in a formatted list

**Independent Test**: Add a task via CLI, then list tasks to verify task appears with correct ID, title, description, and incomplete status. Start with empty list and verify friendly message.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for 'add' command success case in tests/contract/test_cli_add.py
- [ ] T014 [P] [US1] Contract test for 'add' command with empty title error in tests/contract/test_cli_add.py
- [ ] T015 [P] [US1] Contract test for 'add' command with title too long in tests/contract/test_cli_add.py
- [ ] T016 [P] [US1] Contract test for 'list' command with empty tasks in tests/contract/test_cli_list.py
- [ ] T017 [P] [US1] Contract test for 'list' command with populated tasks in tests/contract/test_cli_list.py
- [ ] T018 [P] [US1] Contract test for TaskManager.add() method in tests/contract/test_task_manager.py
- [ ] T019 [P] [US1] Contract test for TaskManager.list_all() method in tests/contract/test_task_manager.py
- [ ] T020 [US1] Integration test for add→list user journey in tests/integration/test_user_journeys.py

### Implementation for User Story 1

- [ ] T021 [P] [US1] Implement validate_title() in src/cli/validators.py (check non-empty, max 200 chars)
- [ ] T022 [P] [US1] Implement validate_description() in src/cli/validators.py (check max 1000 chars)
- [ ] T023 [US1] Implement TaskManager.add() in src/services/task_manager.py (ID generation, validation, storage)
- [ ] T024 [US1] Implement TaskManager.list_all() in src/services/task_manager.py (return sorted tasks)
- [ ] T025 [P] [US1] Implement format_task_added() in src/cli/formatters.py (format confirmation message)
- [ ] T026 [P] [US1] Implement format_task_table() in src/cli/formatters.py (format table with ID, Title, Description, Status; 80-char width)
- [ ] T027 [US1] Implement add_command() in src/cli/commands.py (parse args, validate, call TaskManager.add, format output)
- [ ] T028 [US1] Implement list_command() in src/cli/commands.py (call TaskManager.list_all, handle empty list, format output)
- [ ] T029 [US1] Wire add and list subcommands in src/cli/main.py argparse setup
- [ ] T030 [US1] Add error handling for add and list commands (catch exceptions, format errors to stderr, exit code 1)
- [ ] T031 [US1] Run tests for User Story 1 and verify all pass

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can add tasks and view the list.

---

## Phase 4: User Story 2 - Mark Tasks as Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion status to track progress

**Independent Test**: Add a task, mark it complete, verify status changes in list, mark it incomplete, verify status reverts

### Tests for User Story 2

- [ ] T032 [P] [US2] Contract test for 'complete' command success case in tests/contract/test_cli_complete.py
- [ ] T033 [P] [US2] Contract test for 'complete' command with non-existent ID in tests/contract/test_cli_complete.py
- [ ] T034 [P] [US2] Contract test for 'incomplete' command success case in tests/contract/test_cli_complete.py
- [ ] T035 [P] [US2] Contract test for 'incomplete' command with invalid ID in tests/contract/test_cli_complete.py
- [ ] T036 [P] [US2] Contract test for TaskManager.mark_complete() in tests/contract/test_task_manager.py
- [ ] T037 [P] [US2] Contract test for TaskManager.mark_incomplete() in tests/contract/test_task_manager.py
- [ ] T038 [US2] Integration test for add→complete→list→incomplete→list journey in tests/integration/test_user_journeys.py

### Implementation for User Story 2

- [ ] T039 [P] [US2] Implement validate_id() in src/cli/validators.py (check positive integer)
- [ ] T040 [US2] Implement TaskManager.mark_complete() in src/services/task_manager.py (get task, update status, return task)
- [ ] T041 [US2] Implement TaskManager.mark_incomplete() in src/services/task_manager.py (get task, update status, return task)
- [ ] T042 [P] [US2] Implement format_task_completed() in src/cli/formatters.py (format completion confirmation)
- [ ] T043 [P] [US2] Implement format_task_incompleted() in src/cli/formatters.py (format incomplete confirmation)
- [ ] T044 [US2] Implement complete_command() in src/cli/commands.py (parse ID, validate, call mark_complete, format output)
- [ ] T045 [US2] Implement incomplete_command() in src/cli/commands.py (parse ID, validate, call mark_incomplete, format output)
- [ ] T046 [US2] Wire complete and incomplete subcommands in src/cli/main.py argparse setup
- [ ] T047 [US2] Add error handling for complete and incomplete commands (TaskNotFoundError, invalid ID)
- [ ] T048 [US2] Run tests for User Story 2 and verify all pass

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can add, view, and toggle task completion.

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can modify task titles and descriptions as requirements evolve

**Independent Test**: Add a task, update its title, verify change in list, update description, verify change, update both, verify both changes

### Tests for User Story 3

- [ ] T049 [P] [US3] Contract test for 'update' command with title only in tests/contract/test_cli_update.py
- [ ] T050 [P] [US3] Contract test for 'update' command with description only in tests/contract/test_cli_update.py
- [ ] T051 [P] [US3] Contract test for 'update' command with both title and description in tests/contract/test_cli_update.py
- [ ] T052 [P] [US3] Contract test for 'update' command with non-existent ID in tests/contract/test_cli_update.py
- [ ] T053 [P] [US3] Contract test for 'update' command with empty title error in tests/contract/test_cli_update.py
- [ ] T054 [P] [US3] Contract test for TaskManager.update() in tests/contract/test_task_manager.py
- [ ] T055 [US3] Integration test for add→update→list journey in tests/integration/test_user_journeys.py

### Implementation for User Story 3

- [ ] T056 [US3] Implement TaskManager.update() in src/services/task_manager.py (get task, validate new values, create new Task, store)
- [ ] T057 [US3] Implement format_task_updated() in src/cli/formatters.py (format update confirmation)
- [ ] T058 [US3] Implement update_command() in src/cli/commands.py (parse ID and --title/--description, validate, call update, format output)
- [ ] T059 [US3] Wire update subcommand in src/cli/main.py argparse setup with --title and --description optional arguments
- [ ] T060 [US3] Add error handling for update command (TaskNotFoundError, empty title, no updates provided)
- [ ] T061 [US3] Run tests for User Story 3 and verify all pass

**Checkpoint**: All user stories 1-3 should now be independently functional. Users can add, view, complete, and update tasks.

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can remove irrelevant or mistaken tasks from the list

**Independent Test**: Add a task, delete it by ID, verify it no longer appears in list. Add multiple tasks, delete one, verify only that task removed.

### Tests for User Story 4

- [ ] T062 [P] [US4] Contract test for 'delete' command success case in tests/contract/test_cli_delete.py
- [ ] T063 [P] [US4] Contract test for 'delete' command with non-existent ID in tests/contract/test_cli_delete.py
- [ ] T064 [P] [US4] Contract test for 'delete' command with multiple tasks in tests/contract/test_cli_delete.py
- [ ] T065 [P] [US4] Contract test for TaskManager.delete() in tests/contract/test_task_manager.py
- [ ] T066 [US4] Integration test for add→delete→list journey in tests/integration/test_user_journeys.py

### Implementation for User Story 4

- [ ] T067 [US4] Implement TaskManager.delete() in src/services/task_manager.py (get task, remove from storage, return deleted task)
- [ ] T068 [US4] Implement format_task_deleted() in src/cli/formatters.py (format deletion confirmation)
- [ ] T069 [US4] Implement delete_command() in src/cli/commands.py (parse ID, validate, call delete, format output)
- [ ] T070 [US4] Wire delete subcommand in src/cli/main.py argparse setup
- [ ] T071 [US4] Add error handling for delete command (TaskNotFoundError, invalid ID)
- [ ] T072 [US4] Run tests for User Story 4 and verify all pass

**Checkpoint**: All user stories should now be independently functional. Complete CRUD operations available.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T073 [P] Add --help text for all CLI commands in src/cli/main.py
- [ ] T074 [P] Add --version flag to src/cli/main.py showing "Todo CLI v1.0.0 (Phase I)"
- [ ] T075 [P] Add docstrings to all public methods in TaskManager (src/services/task_manager.py)
- [ ] T076 [P] Add docstrings to all CLI command functions (src/cli/commands.py)
- [ ] T077 [P] Add module-level docstrings to all Python files
- [ ] T078 Run ruff format on all source files (src/, tests/)
- [ ] T079 Run ruff check on all source files and fix any warnings
- [ ] T080 Run mypy on src/ with strict mode and fix any type errors
- [ ] T081 Run full test suite with pytest and verify 100% pass rate
- [ ] T082 Run pytest with coverage report and verify ≥90% coverage
- [ ] T083 [P] Create README.md with project overview, setup, and usage instructions
- [ ] T084 [P] Validate quickstart.md examples work correctly (manual testing)
- [ ] T085 Test Unicode character handling in titles and descriptions
- [ ] T086 Test edge cases: extremely long titles (200 chars), long descriptions (1000 chars)
- [ ] T087 Test terminal output fits in 80-character width
- [ ] T088 Final validation: Run through all user journeys from spec.md manually
- [ ] T089 Final checkpoint: Verify all acceptance criteria from plan.md are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (uses TaskManager from foundation)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (uses TaskManager from foundation)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories (uses TaskManager from foundation)

**Note**: All user stories are independently implementable and testable after Foundational phase completion

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Validators before commands
- TaskManager methods before CLI commands
- Formatters can be parallel with validators
- Commands before argparse wiring
- Error handling after commands
- Run tests after all implementation tasks

### Parallel Opportunities

- **Setup (Phase 1)**: T003, T004, T005 can run in parallel
- **Foundational (Phase 2)**: T006, T007, T009, T010 can run in parallel (different files)
- **User Story 1 Tests**: T013-T020 can all run in parallel (different test files/functions)
- **User Story 1 Implementation**: T021-T022 parallel, T025-T026 parallel
- **User Story 2 Tests**: T032-T038 can all run in parallel
- **User Story 2 Implementation**: T042-T043 parallel
- **User Story 3 Tests**: T049-T055 can all run in parallel
- **User Story 4 Tests**: T062-T066 can all run in parallel
- **Polish (Phase 7)**: T073-T077 parallel, T083-T084 parallel
- **All user stories (Phases 3-6) can be worked on in parallel by different team members after Foundational phase**

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for 'add' command success case in tests/contract/test_cli_add.py"
Task: "Contract test for 'add' command with empty title error in tests/contract/test_cli_add.py"
Task: "Contract test for 'add' command with title too long in tests/contract/test_cli_add.py"
Task: "Contract test for 'list' command with empty tasks in tests/contract/test_cli_list.py"
Task: "Contract test for 'list' command with populated tasks in tests/contract/test_cli_list.py"
Task: "Contract test for TaskManager.add() method in tests/contract/test_task_manager.py"
Task: "Contract test for TaskManager.list_all() method in tests/contract/test_task_manager.py"
Task: "Integration test for add→list user journey in tests/integration/test_user_journeys.py"

# Launch validators in parallel:
Task: "Implement validate_title() in src/cli/validators.py"
Task: "Implement validate_description() in src/cli/validators.py"

# Launch formatters in parallel:
Task: "Implement format_task_added() in src/cli/formatters.py"
Task: "Implement format_task_table() in src/cli/formatters.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T012) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T013-T031)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Can add tasks with title and description
   - Can view all tasks in formatted list
   - Empty list shows friendly message
   - Error handling works (empty title, long title)
5. Deploy/demo if ready - MVP is complete!

**MVP Scope**: 31 tasks (T001-T031)

### Incremental Delivery

1. Complete Setup + Foundational (T001-T012) → Foundation ready
2. Add User Story 1 (T013-T031) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (T032-T048) → Test independently → Deploy/Demo (can now toggle completion)
4. Add User Story 3 (T049-T061) → Test independently → Deploy/Demo (can now update tasks)
5. Add User Story 4 (T062-T072) → Test independently → Deploy/Demo (full CRUD complete)
6. Add Polish (T073-T089) → Final validation → Production ready
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup (T001-T005) together
2. Team completes Foundational (T006-T012) together
3. Once Foundational is done:
   - **Developer A**: User Story 1 (T013-T031)
   - **Developer B**: User Story 2 (T032-T048)
   - **Developer C**: User Story 3 (T049-T061)
   - **Developer D**: User Story 4 (T062-T072)
4. Stories complete and integrate independently
5. Team completes Polish (T073-T089) together

**Total Parallel Savings**: Can complete 4 user stories simultaneously after foundation, dramatically reducing time to full feature set.

---

## Task Summary

**Total Tasks**: 89

**Tasks by Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 7 tasks
- Phase 3 (User Story 1): 19 tasks (8 tests + 11 implementation)
- Phase 4 (User Story 2): 17 tasks (7 tests + 10 implementation)
- Phase 5 (User Story 3): 13 tasks (7 tests + 6 implementation)
- Phase 6 (User Story 4): 11 tasks (5 tests + 6 implementation)
- Phase 7 (Polish): 17 tasks

**Parallel Opportunities**: 45 tasks marked [P] can run in parallel within their phases

**Independent Test Criteria**:
- **US1**: Add task + list tasks → verify task appears with correct details
- **US2**: Add task + mark complete + list → verify status changed
- **US3**: Add task + update title/description → verify changes in list
- **US4**: Add tasks + delete one → verify only that task removed

**Suggested MVP Scope**: Phases 1-3 (31 tasks, User Story 1 only)

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests must be written FIRST and must FAIL before implementation (TDD requirement from constitution)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Run full test suite after each story completion
- All tasks follow constitution principles: SDD, TDD, separation of concerns, determinism
