__all__ = [
    "benchmark_extreme_aliases",
    "benchmark_few_aliases",
    "benchmark_no_aliases",
    "benchmark_very_many_aliases",
    "benchmark_with_many_aliases",
]

from argenta import App
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router

from .entity import benchmarks


def _handler(_res: Response) -> None:
    pass


def _startup(aliases_per_command: tuple[set[str], ...]) -> None:
    app = App(override_system_messages=True)
    router = Router()
    for command_index, aliases in enumerate(aliases_per_command):
        router.command(Command(f"command{command_index}", aliases=aliases))(_handler)
    app.include_router(router)
    app._pre_cycle_setup()


@benchmarks.register(type_="app_startup", description="With no aliases")
def benchmark_no_aliases() -> None:
    _startup((set(), set(), set()))


@benchmarks.register(type_="app_startup", description="With few aliases (6 total)")
def benchmark_few_aliases() -> None:
    _startup(({"c1", "cmd1"}, {"c2", "cmd2"}, {"c3", "cmd3"}))


@benchmarks.register(type_="app_startup", description="With many aliases (15 total)")
def benchmark_with_many_aliases() -> None:
    _startup(
        (
            {"c1", "cmd1", "com1", "first", "one"},
            {"c2", "cmd2", "com2", "second", "two"},
            {"c3", "cmd3", "com3", "third", "three"},
        )
    )


@benchmarks.register(type_="app_startup", description="With very many aliases (60 total)")
def benchmark_very_many_aliases() -> None:
    _startup(tuple({f"alias{command_index}_{i}" for i in range(20)} for command_index in range(3)))


@benchmarks.register(type_="app_startup", description="With extreme aliases (300 total)")
def benchmark_extreme_aliases() -> None:
    _startup(tuple({f"alias{command_index}_{i}" for i in range(100)} for command_index in range(3)))
