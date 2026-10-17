from argenta.command import Flag, Flags
from argenta.command.models import Command, InputCommand
from argenta.response import Response
from argenta.router import Router
from metrics.benchmarks.entity import benchmarks

_BENCHMARK_TYPE = "finds_appropriate_handler"
_MANY_COMMANDS_COUNT = 50
_FLAGS_PER_COMMAND = 20
_INPUT_FLAGS_COUNT = 10


def _command_handler(_res: Response) -> None: ...


def _router_with_commands(
    trigger_prefix: str, command_count: int, flags_per_command: int = 0
) -> Router:
    router = Router()
    for command_index in range(command_count):
        flags = (
            Flags(
                [
                    Flag(f"{trigger_prefix}{command_index}_f{flag_index}")
                    for flag_index in range(flags_per_command)
                ]
            )
            if flags_per_command
            else None
        )
        router.command(Command(f"{trigger_prefix}{command_index}", flags=flags))(_command_handler)
    return router


_SIMPLE_ROUTER = _router_with_commands("cmd", 1)
_SIMPLE_INPUT = InputCommand.parse("cmd0")

_THREE_FLAGS = Flags([Flag("a"), Flag("b"), Flag("c")])
_THREE_FLAGS_ROUTER = Router()
_THREE_FLAGS_ROUTER.command(Command("test", flags=_THREE_FLAGS))(_command_handler)
_THREE_FLAGS_INPUT = InputCommand.parse("test -a -b -c")

_MANY_COMMANDS_ROUTER = _router_with_commands("cmd", _MANY_COMMANDS_COUNT)
_MANY_COMMANDS_INPUT = InputCommand.parse("cmd25")

_MANY_FLAGS_ROUTER = _router_with_commands("flag", 1, _FLAGS_PER_COMMAND)
_MANY_FLAGS_ARGS = " ".join(f"--flag0_f{flag_index}" for flag_index in range(_INPUT_FLAGS_COUNT))
_MANY_FLAGS_INPUT = InputCommand.parse(f"flag0 {_MANY_FLAGS_ARGS}")

_EXTREME_ROUTER = _router_with_commands("cmd", 100, 10)
_EXTREME_INPUT = InputCommand.parse("cmd50 --cmd50_f0 --cmd50_f1 --cmd50_f2")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Simple command (no flags)")
def benchmark_simple_command() -> None:
    _SIMPLE_ROUTER.finds_appropriate_handler(_SIMPLE_INPUT)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Command with flags (3 flags)")
def benchmark_command_with_flags() -> None:
    _THREE_FLAGS_ROUTER.finds_appropriate_handler(_THREE_FLAGS_INPUT)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Many commands (50 commands)")
def benchmark_many_commands() -> None:
    _MANY_COMMANDS_ROUTER.finds_appropriate_handler(_MANY_COMMANDS_INPUT)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Command with many flags (20 flags)")
def benchmark_command_with_many_flags() -> None:
    _MANY_FLAGS_ROUTER.finds_appropriate_handler(_MANY_FLAGS_INPUT)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Extreme (100 commands, 10 flags each)")
def benchmark_extreme_router() -> None:
    _EXTREME_ROUTER.finds_appropriate_handler(_EXTREME_INPUT)
