from dishka import Provider, Scope, provide

from .repository import TaskRepository


class TaskProvider(Provider):
    @provide(scope=Scope.APP)
    def get_repository(self) -> TaskRepository:
        return TaskRepository()
