__all__ = ["CliProvider", "create_cli_container"]

from dishka import (  # pyright: ignore[reportUnknownVariableType]
    Container,
    Provider,
    Scope,
    make_container,
    provide,
)
from rich.console import Console


class CliProvider(Provider):
    @provide(scope=Scope.APP)
    def get_console(self) -> Console:
        return Console()


def create_cli_container() -> Container:
    return make_container(CliProvider())
