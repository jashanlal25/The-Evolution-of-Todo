#!/usr/bin/env python3
"""
Todo CLI - Manage your tasks from the command line.

Phase I: In-Memory Python Console Todo Application with Menu-Driven Interface
"""

import sys

from .formatters import format_task_table
from ..models.exceptions import EmptyTitleError, InvalidTaskError, TaskNotFoundError
from ..services.task_manager import TaskManager


def clear_screen() -> None:
    """Clear screen for better UI."""
    print("\n" * 2)


def show_menu() -> None:
    """Display main menu."""
    print("=" * 60)
    print("                    TODO CLI APPLICATION")
    print("=" * 60)
    print()
    print("  1. Add Task")
    print("  2. View All Tasks")
    print("  3. Complete Task")
    print("  4. Update Task")
    print("  5. Mark as Incomplete")
    print("  6. Delete Task")
    print("  7. Clear All Tasks")
    print("  8. Exit")
    print()
    print("=" * 60)


def add_task(manager: TaskManager) -> None:
    """Add a new task."""
    print("\n--- Add New Task ---")
    title = input("Enter task title: ").strip()
    if not title:
        print("❌ Error: Title cannot be empty!")
        return

    description = input("Enter description (optional, press Enter to skip): ").strip()

    try:
        task = manager.add(title, description)
        print(f"\n✅ Task added successfully!")
        print(f"   ID: {task.id}")
        print(f"   Title: {task.title}")
        if task.description:
            print(f"   Description: {task.description}")
    except (EmptyTitleError, InvalidTaskError) as e:
        print(f"❌ Error: {e}")


def view_tasks(manager: TaskManager) -> None:
    """View all tasks."""
    print("\n--- All Tasks ---")
    tasks = manager.list_all()
    if tasks:
        print(f"\nTotal tasks: {manager.count()}")
        print(format_task_table(tasks))
    else:
        print("\n📝 No tasks found. Add a task to get started!")


def complete_task(manager: TaskManager) -> None:
    """Mark a task as complete."""
    print("\n--- Complete Task ---")
    view_tasks(manager)

    if manager.count() == 0:
        return

    try:
        task_id = int(input("\nEnter task ID to mark as complete: ").strip())
        task = manager.mark_complete(task_id)
        print(f"\n✅ Task '{task.title}' marked as complete!")
    except ValueError:
        print("❌ Error: Please enter a valid number")
    except TaskNotFoundError as e:
        print(f"❌ Error: {e}")


def update_task(manager: TaskManager) -> None:
    """Update a task."""
    print("\n--- Update Task ---")
    view_tasks(manager)

    if manager.count() == 0:
        return

    try:
        task_id = int(input("\nEnter task ID to update: ").strip())

        # Get current task
        current_task = manager.get(task_id)
        print(f"\nCurrent title: {current_task.title}")
        print(f"Current description: {current_task.description}")

        new_title = input("\nEnter new title (press Enter to keep current): ").strip()
        new_desc = input("Enter new description (press Enter to keep current): ").strip()

        # Use None if user pressed Enter (keep current)
        title_update = new_title if new_title else None
        desc_update = new_desc if new_desc else None

        if not title_update and not desc_update:
            print("❌ No changes made.")
            return

        task = manager.update(task_id, title_update, desc_update)
        print(f"\n✅ Task updated successfully!")
        print(f"   ID: {task.id}")
        print(f"   Title: {task.title}")
        print(f"   Description: {task.description}")
    except ValueError:
        print("❌ Error: Please enter a valid number")
    except (TaskNotFoundError, EmptyTitleError, InvalidTaskError) as e:
        print(f"❌ Error: {e}")


def incomplete_task(manager: TaskManager) -> None:
    """Mark a task as incomplete."""
    print("\n--- Mark Task as Incomplete ---")
    view_tasks(manager)

    if manager.count() == 0:
        return

    try:
        task_id = int(input("\nEnter task ID to mark as incomplete: ").strip())
        task = manager.mark_incomplete(task_id)
        print(f"\n✅ Task '{task.title}' marked as incomplete!")
    except ValueError:
        print("❌ Error: Please enter a valid number")
    except TaskNotFoundError as e:
        print(f"❌ Error: {e}")


def delete_task(manager: TaskManager) -> None:
    """Delete a task."""
    print("\n--- Delete Task ---")
    view_tasks(manager)

    if manager.count() == 0:
        return

    try:
        task_id = int(input("\nEnter task ID to delete: ").strip())
        task = manager.delete(task_id)
        print(f"\n✅ Task '{task.title}' deleted successfully!")
    except ValueError:
        print("❌ Error: Please enter a valid number")
    except TaskNotFoundError as e:
        print(f"❌ Error: {e}")


def clear_all_tasks(manager: TaskManager) -> None:
    """Clear all tasks."""
    print("\n--- Clear All Tasks ---")

    if manager.count() == 0:
        print("\n📝 No tasks to clear.")
        return

    confirm = input(
        f"\n⚠️  Are you sure you want to delete all {manager.count()} tasks? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        count = manager.clear_all()
        print(f"\n✅ Cleared {count} task(s) successfully!")
    else:
        print("\n❌ Clear cancelled.")


def main() -> int:
    """
    Main entry point for the Todo CLI application.

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    # Create TaskManager (in-memory storage, lost on exit - Phase I)
    manager = TaskManager()

    clear_screen()
    print("Welcome to Todo CLI!")
    print("Tasks are saved during your session.")
    input("\nPress Enter to continue...")

    while True:
        clear_screen()
        show_menu()

        try:
            choice = input("Select option (1-8): ").strip()

            if choice == "1":
                add_task(manager)
            elif choice == "2":
                view_tasks(manager)
            elif choice == "3":
                complete_task(manager)
            elif choice == "4":
                update_task(manager)
            elif choice == "5":
                incomplete_task(manager)
            elif choice == "6":
                delete_task(manager)
            elif choice == "7":
                clear_all_tasks(manager)
            elif choice == "8":
                print("\n👋 Goodbye! Your tasks are saved for next time.")
                break
            else:
                print("\n❌ Invalid option. Please select 1-8.")

            input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            input("\nPress Enter to continue...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
