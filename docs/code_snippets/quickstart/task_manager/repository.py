from dataclasses import dataclass
from typing import Literal

Priority = Literal["low", "medium", "high"]

@dataclass
class Task:
    description: str
    priority: Priority = "medium"

class TaskRepository:
    def __init__(self):
        self._tasks: list[Task] = []

    def add_task(self, task: Task):
        self._tasks.append(task)

    def get_all_tasks(self) -> list[Task]:
        return self._tasks
