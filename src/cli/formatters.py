"""Output formatting functions for CLI display."""

from src.models.task import Task


def format_task_added(task: Task) -> str:
    """
    Format task creation confirmation message.

    Args:
        task: The newly created task

    Returns:
        str: Formatted confirmation message
    """
    return (
        f"Task added successfully!\n"
        f"ID: {task.id}\n"
        f"Title: {task.title}\n"
        f"Description: {task.description}\n"
        f"Status: {'Complete' if task.completed else 'Incomplete'}"
    )


def format_task_table(tasks: list[Task]) -> str:
    """
    Format task list as table.

    Args:
        tasks: List of tasks to display

    Returns:
        str: Formatted table or empty message
    """
    if not tasks:
        return "No tasks found. Add a task to get started!"

    # Build table header
    lines = []
    lines.append("ID | Title                          | Description                     | Status")
    lines.append("---|--------------------------------|---------------------------------|------------")

    # Build table rows
    for task in tasks:
        # Truncate long text to fit 80-char width
        title_display = task.title[:30] if len(task.title) <= 30 else task.title[:27] + "..."
        desc_display = (
            task.description[:30]
            if len(task.description) <= 30
            else task.description[:27] + "..."
        )
        status_display = "Complete" if task.completed else "Incomplete"

        # Format row with padding
        lines.append(
            f"{task.id:<3}| {title_display:<31}| {desc_display:<32}| {status_display}"
        )

    return "\n".join(lines)


def format_task_updated(task: Task) -> str:
    """
    Format task update confirmation message.

    Args:
        task: The updated task

    Returns:
        str: Formatted confirmation message
    """
    return (
        f"Task updated successfully!\n"
        f"ID: {task.id}\n"
        f"Title: {task.title}\n"
        f"Description: {task.description}\n"
        f"Status: {'Complete' if task.completed else 'Incomplete'}"
    )


def format_task_completed(task: Task) -> str:
    """
    Format task completion confirmation message.

    Args:
        task: The completed task

    Returns:
        str: Formatted confirmation message
    """
    return f"Task marked as complete!\nID: {task.id}\nTitle: {task.title}"


def format_task_incompleted(task: Task) -> str:
    """
    Format task incomplete confirmation message.

    Args:
        task: The task marked incomplete

    Returns:
        str: Formatted confirmation message
    """
    return f"Task marked as incomplete!\nID: {task.id}\nTitle: {task.title}"


def format_task_deleted(task: Task) -> str:
    """
    Format task deletion confirmation message.

    Args:
        task: The deleted task

    Returns:
        str: Formatted confirmation message
    """
    return f"Task deleted successfully!\nID: {task.id}\nTitle: {task.title}"
