from dataclasses import dataclass
from types import SimpleNamespace

from argenta import App
from argenta.command.models import Command
from argenta.repl import REPLConfig, TerminalLayout
from argenta.router import Router
from metrics.benchmarks._scenarios import alias_sets, command_handler
from metrics.benchmarks.entity import benchmarks


@dataclass(frozen=True, slots=True)
class AppStartupConfig:
    benchmark_type: str = "app_startup"
    command_count: int = 3
    very_many_aliases_count: int = 20
    extreme_aliases_count: int = 100


def _startup(aliases_per_command: tuple[set[str], ...]) -> None:
    app = App(override_system_messages=True)
    router = Router()
    for command_index, aliases in enumerate(aliases_per_command):
        router.command(Command(f"command{command_index}", aliases=aliases))(command_handler)
    app.include_router(router)
    app.prepare_for_run(TerminalLayout(app.printer, app.renderer, REPLConfig()))


_CONFIG = AppStartupConfig()
_ALIAS_SETS = SimpleNamespace(
    very_many=alias_sets(_CONFIG.command_count, _CONFIG.very_many_aliases_count),
    extreme=alias_sets(_CONFIG.command_count, _CONFIG.extreme_aliases_count),
)


@benchmarks.register(type_=_CONFIG.benchmark_type, description="With no aliases")
def benchmark_no_aliases() -> None:
    _startup((set(), set(), set()))


@benchmarks.register(type_=_CONFIG.benchmark_type, description="With few aliases (6 total)")
def benchmark_few_aliases() -> None:
    _startup(({"c1", "cmd1"}, {"c2", "cmd2"}, {"c3", "cmd3"}))


@benchmarks.register(type_=_CONFIG.benchmark_type, description="With many aliases (15 total)")
def benchmark_with_many_aliases() -> None:
    _startup(
        (
            {"c1", "cmd1", "com1", "first", "one"},
            {"c2", "cmd2", "com2", "second", "two"},
            {"c3", "cmd3", "com3", "third", "three"},
        )
    )


@benchmarks.register(type_=_CONFIG.benchmark_type, description="With very many aliases (60 total)")
def benchmark_very_many_aliases() -> None:
    _startup(_ALIAS_SETS.very_many)


@benchmarks.register(type_=_CONFIG.benchmark_type, description="With extreme aliases (300 total)")
def benchmark_extreme_aliases() -> None:
    _startup(_ALIAS_SETS.extreme)
