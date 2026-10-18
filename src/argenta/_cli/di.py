from dishka import (
    Container,
    Provider,
    Scope,
    make_container,
    provide,
)
from rich.console import Console

from argenta.orchestrator.config import RunnerConfig


class CliProvider(Provider):
    @provide(scope=Scope.APP)
    def get_console(self) -> Console:
        return Console()

    @provide(scope=Scope.APP)
    def get_runner_config(self) -> RunnerConfig:
        return RunnerConfig()


def create_cli_container() -> Container:
    return make_container(CliProvider())
