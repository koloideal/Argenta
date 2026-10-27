from dataclasses import dataclass
from types import SimpleNamespace

from argenta.command.models import InputCommand
from argenta.router import Router
from metrics.benchmarks._scenarios import (
    flags_router,
    router_with_commands,
)
from metrics.benchmarks.entity import benchmarks


@dataclass(frozen=True, slots=True)
class FindsAppropriateHandlerConfig:
    benchmark_type: str = "finds_appropriate_handler"
    simple_commands_count: int = 1
    many_commands_count: int = 50
    many_flags_per_command: int = 20
    many_flags_input_count: int = 10
    extreme_commands_count: int = 100
    extreme_flags_per_command: int = 10


def _many_flags_scenario(
    flags_per_command: int, input_flags_count: int
) -> tuple[Router, InputCommand]:
    router = router_with_commands("flag", 1, flags_per_command)
    input_args = " ".join(f"--flag0_f{flag_index}" for flag_index in range(input_flags_count))
    return router, InputCommand.parse(f"flag0 {input_args}")


_CONFIG = FindsAppropriateHandlerConfig()
_SCENARIOS = SimpleNamespace(
    simple=(router_with_commands("cmd", _CONFIG.simple_commands_count), InputCommand.parse("cmd0")),
    three_flags=(flags_router(("a", "b", "c")), InputCommand.parse("test -a -b -c")),
    many_commands=(
        router_with_commands("cmd", _CONFIG.many_commands_count),
        InputCommand.parse("cmd25"),
    ),
    many_flags=_many_flags_scenario(_CONFIG.many_flags_per_command, _CONFIG.many_flags_input_count),
    extreme=(
        router_with_commands(
            "cmd", _CONFIG.extreme_commands_count, _CONFIG.extreme_flags_per_command
        ),
        InputCommand.parse("cmd50 --cmd50_f0 --cmd50_f1 --cmd50_f2"),
    ),
)


@benchmarks.register(type_=_CONFIG.benchmark_type, description="Simple command (no flags)")
def benchmark_simple_command() -> None:
    router, input_command = _SCENARIOS.simple
    router.finds_appropriate_handler(input_command)


@benchmarks.register(type_=_CONFIG.benchmark_type, description="Command with flags (3 flags)")
def benchmark_command_with_flags() -> None:
    router, input_command = _SCENARIOS.three_flags
    router.finds_appropriate_handler(input_command)


@benchmarks.register(type_=_CONFIG.benchmark_type, description="Many commands (50 commands)")
def benchmark_many_commands() -> None:
    router, input_command = _SCENARIOS.many_commands
    router.finds_appropriate_handler(input_command)


@benchmarks.register(type_=_CONFIG.benchmark_type, description="Command with many flags (20 flags)")
def benchmark_command_with_many_flags() -> None:
    router, input_command = _SCENARIOS.many_flags
    router.finds_appropriate_handler(input_command)


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Extreme (100 commands, 10 flags each)"
)
def benchmark_extreme_router() -> None:
    router, input_command = _SCENARIOS.extreme
    router.finds_appropriate_handler(input_command)
