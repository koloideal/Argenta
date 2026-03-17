__all__ = [
    "benchmark_few_commands",
    "benchmark_many_commands_most_similar",
    "benchmark_many_aliases",
    "benchmark_partial_match",
    "benchmark_extreme_commands",
]

from argenta import App
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router

from .entity import benchmarks


def setup_app_with_commands(command_count: int, aliases_per_command: int = 0) -> App:
    app = App(override_system_messages=True)
    router = Router()

    for i in range(command_count):
        aliases = (
            {f"alias{i}_{j}" for j in range(aliases_per_command)} if aliases_per_command else set()
        )

        @router.command(Command(f"command{i}", aliases=aliases))
        def handler(_res: Response) -> None:
            pass

    app.include_router(router)
    return app


@benchmarks.register(
    type_="most_similar_command", description="Few commands (10 commands, no match)"
)
def benchmark_few_commands() -> None:
    app = setup_app_with_commands(10)
    app._most_similar_command("unknown")


@benchmarks.register(
    type_="most_similar_command", description="Many commands (50 commands, no match)"
)
def benchmark_many_commands_most_similar() -> None:
    app = setup_app_with_commands(50)
    app._most_similar_command("unknown")


@benchmarks.register(
    type_="most_similar_command", description="Many aliases (20 commands, 10 aliases each)"
)
def benchmark_many_aliases() -> None:
    app = setup_app_with_commands(20, aliases_per_command=10)
    app._most_similar_command("unknown")


@benchmarks.register(
    type_="most_similar_command", description="Partial match (50 commands, prefix match)"
)
def benchmark_partial_match() -> None:
    app = setup_app_with_commands(50)
    app._most_similar_command("comm")


@benchmarks.register(
    type_="most_similar_command", description="Extreme (100 commands, 20 aliases each)"
)
def benchmark_extreme_commands() -> None:
    app = setup_app_with_commands(100, aliases_per_command=20)
    app._most_similar_command("comm")
