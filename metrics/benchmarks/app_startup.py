from argenta import App
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router
from metrics.benchmarks.entity import benchmarks

_BENCHMARK_TYPE = "app_startup"
_COMMAND_COUNT = 3
_VERY_MANY_ALIASES_COUNT = 20
_EXTREME_ALIASES_COUNT = 100

_VERY_MANY_ALIAS_SETS = tuple(
    {f"alias{command_index}_{alias_index}" for alias_index in range(_VERY_MANY_ALIASES_COUNT)}
    for command_index in range(_COMMAND_COUNT)
)
_EXTREME_ALIAS_SETS = tuple(
    {f"alias{command_index}_{alias_index}" for alias_index in range(_EXTREME_ALIASES_COUNT)}
    for command_index in range(_COMMAND_COUNT)
)


def _command_handler(_res: Response) -> None: ...


def _startup(aliases_per_command: tuple[set[str], ...]) -> None:
    app = App(override_system_messages=True)
    router = Router()
    for command_index, aliases in enumerate(aliases_per_command):
        router.command(Command(f"command{command_index}", aliases=aliases))(_command_handler)
    app.include_router(router)
    app.prepare_for_run()


@benchmarks.register(type_=_BENCHMARK_TYPE, description="With no aliases")
def benchmark_no_aliases() -> None:
    _startup((set(), set(), set()))


@benchmarks.register(type_=_BENCHMARK_TYPE, description="With few aliases (6 total)")
def benchmark_few_aliases() -> None:
    _startup(({"c1", "cmd1"}, {"c2", "cmd2"}, {"c3", "cmd3"}))


@benchmarks.register(type_=_BENCHMARK_TYPE, description="With many aliases (15 total)")
def benchmark_with_many_aliases() -> None:
    _startup(
        (
            {"c1", "cmd1", "com1", "first", "one"},
            {"c2", "cmd2", "com2", "second", "two"},
            {"c3", "cmd3", "com3", "third", "three"},
        )
    )


@benchmarks.register(type_=_BENCHMARK_TYPE, description="With very many aliases (60 total)")
def benchmark_very_many_aliases() -> None:
    _startup(_VERY_MANY_ALIAS_SETS)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="With extreme aliases (300 total)")
def benchmark_extreme_aliases() -> None:
    _startup(_EXTREME_ALIAS_SETS)
