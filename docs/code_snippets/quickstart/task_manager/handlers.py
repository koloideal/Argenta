from typing import cast

from argenta import Command, Response, Router
from argenta.command.flag import ValidationStatus, Flag, Flags
from argenta.di import FromDishka

from .repository import Priority, Task, TaskRepository

router = Router(title="Task Manager")


@router.command(
    Command(
        "add-task",
        description="Add a new task",
        flags=Flags(
            [
                Flag("description"),
                Flag("priority", possible_values=["low", "medium", "high"]),
            ]
        ),
    )
)
def add_task(response: Response, repo: FromDishka[TaskRepository]):
    description_flag = response.input_flags.get_flag_by_name("description")
    if not description_flag or not description_flag.status == ValidationStatus.VALID:
        print("Error: --description flag is required.")
        return
    task_description = description_flag.input_value or ""

    priority_flag = response.input_flags.get_flag_by_name("priority")
    if priority_flag and priority_flag.status == ValidationStatus.VALID:
        priority_value = priority_flag.input_value
    else:
        priority_value = "medium"

    priority = cast(Priority, priority_value)

    task = Task(description=task_description, priority=priority)
    repo.add_task(task)
    print(f"Added task: '{task.description}' with priority '{task.priority}'")


@router.command(Command("list-tasks", description="List all tasks"))
def list_tasks(response: Response, repo: FromDishka[TaskRepository]):
    tasks = repo.get_all_tasks()
    if not tasks:
        print("No tasks found.")
        return

    print("Tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task.description} (Priority: {task.priority})")
