from dataclasses import dataclass

from argenta import App
from argenta.command import Flag, Flags
from argenta.command.models import Command
from argenta.repl import REPLRuntime
from argenta.router import Router
from metrics.benchmarks._scenarios import command_handler
from metrics.benchmarks.entity import benchmarks


@dataclass(frozen=True, slots=True)
class CommandDispatchConfig:
    benchmark_type: str = "command_dispatch"
    command_count: int = 20


def setup_app(command_count: int) -> App:
    app = App(override_system_messages=True)
    router = Router()
    for command_index in range(command_count):
        router.command(
            Command(
                f"cmd{command_index}",
                flags=Flags([Flag("verbose"), Flag("output")]),
            )
        )(command_handler)
    app.include_router(router)
    app._setup_system_router()
    return app


_CONFIG = CommandDispatchConfig()
_RUNTIME = REPLRuntime(setup_app(_CONFIG.command_count))


@benchmarks.register(type_=_CONFIG.benchmark_type, description="Simple command, no flags")
def benchmark_dispatch_simple() -> None:
    _RUNTIME._dispatch_command("cmd5")


@benchmarks.register(type_=_CONFIG.benchmark_type, description="Command with flags and a value")
def benchmark_dispatch_flags_and_values() -> None:
    _RUNTIME._dispatch_command("cmd5 --verbose --output result.txt")


@benchmarks.register(type_=_CONFIG.benchmark_type, description="Unknown command (suggestion path)")
def benchmark_dispatch_unknown_command() -> None:
    _RUNTIME._dispatch_command("commd5")
