__all__ = ["CliProvider", "create_cli_container"]

from dishka import Container, Provider, Scope, make_container, provide  # pyright: ignore[reportUnknownVariableType]
from rich.console import Console


class CliProvider(Provider):
    @provide(scope=Scope.APP)
    def get_console(self) -> Console:
        return Console()


def create_cli_container() -> Container:
    return make_container(CliProvider())
