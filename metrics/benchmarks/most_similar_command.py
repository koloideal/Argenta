__all__ = [
    "benchmark_extreme_commands",
    "benchmark_few_commands",
    "benchmark_many_aliases",
    "benchmark_many_commands_most_similar",
    "benchmark_partial_match",
]

from argenta import App
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router

from .entity import benchmarks


def _handler(_res: Response) -> None:
    pass


def setup_app_with_commands(command_count: int, aliases_per_command: int = 0) -> App:
    app = App(override_system_messages=True)
    router = Router()

    for command_index in range(command_count):
        aliases = (
            {f"alias{command_index}_{alias_index}" for alias_index in range(aliases_per_command)}
            if aliases_per_command
            else set()
        )
        router.command(Command(f"command{command_index}", aliases=aliases))(_handler)

    app.include_router(router)
    return app


_FEW_COMMANDS_APP = setup_app_with_commands(10)
_MANY_COMMANDS_APP = setup_app_with_commands(50)
_MANY_ALIASES_APP = setup_app_with_commands(20, aliases_per_command=10)
_EXTREME_APP = setup_app_with_commands(100, aliases_per_command=20)


@benchmarks.register(
    type_="most_similar_command", description="Few commands (10 commands, no match)"
)
def benchmark_few_commands() -> None:
    _FEW_COMMANDS_APP._most_similar_command("unknown")


@benchmarks.register(
    type_="most_similar_command", description="Many commands (50 commands, no match)"
)
def benchmark_many_commands_most_similar() -> None:
    _MANY_COMMANDS_APP._most_similar_command("unknown")


@benchmarks.register(
    type_="most_similar_command", description="Many aliases (20 commands, 10 aliases each)"
)
def benchmark_many_aliases() -> None:
    _MANY_ALIASES_APP._most_similar_command("unknown")


@benchmarks.register(
    type_="most_similar_command", description="Partial match (50 commands, prefix match)"
)
def benchmark_partial_match() -> None:
    _MANY_COMMANDS_APP._most_similar_command("comm")


@benchmarks.register(
    type_="most_similar_command", description="Extreme (100 commands, 20 aliases each)"
)
def benchmark_extreme_commands() -> None:
    _EXTREME_APP._most_similar_command("comm")
