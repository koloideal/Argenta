from dataclasses import dataclass
from types import SimpleNamespace

from argenta import App
from argenta.command.models import Command
from argenta.router import Router
from metrics.benchmarks._scenarios import command_handler
from metrics.benchmarks.entity import benchmarks


@dataclass(frozen=True, slots=True)
class MostSimilarCommandConfig:
    benchmark_type: str = "most_similar_command"
    few_commands_count: int = 10
    many_commands_count: int = 50
    aliased_commands_count: int = 20
    aliases_per_aliased_command: int = 10
    extreme_commands_count: int = 100
    extreme_aliases_per_command: int = 20


def setup_app_with_commands(command_count: int, aliases_per_command: int = 0) -> App:
    app = App(override_system_messages=True)
    router = Router()

    for command_index in range(command_count):
        aliases = (
            {f"alias{command_index}_{alias_index}" for alias_index in range(aliases_per_command)}
            if aliases_per_command
            else set()
        )
        router.command(Command(f"command{command_index}", aliases=aliases))(command_handler)

    app.include_router(router)
    return app


_CONFIG = MostSimilarCommandConfig()
_APPS = SimpleNamespace(
    few_commands=setup_app_with_commands(_CONFIG.few_commands_count),
    many_commands=setup_app_with_commands(_CONFIG.many_commands_count),
    many_aliases=setup_app_with_commands(
        _CONFIG.aliased_commands_count, _CONFIG.aliases_per_aliased_command
    ),
    extreme=setup_app_with_commands(
        _CONFIG.extreme_commands_count, _CONFIG.extreme_aliases_per_command
    ),
)


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Few commands (10 commands, no match)"
)
def benchmark_few_commands() -> None:
    _APPS.few_commands._most_similar_command("unknown")


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Many commands (50 commands, no match)"
)
def benchmark_many_commands_most_similar() -> None:
    _APPS.many_commands._most_similar_command("unknown")


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Many aliases (20 commands, 10 aliases each)"
)
def benchmark_many_aliases() -> None:
    _APPS.many_aliases._most_similar_command("unknown")


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Partial match (50 commands, prefix match)"
)
def benchmark_partial_match() -> None:
    _APPS.many_commands._most_similar_command("comm")


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Extreme (100 commands, 20 aliases each)"
)
def benchmark_extreme_commands() -> None:
    _APPS.extreme._most_similar_command("comm")
