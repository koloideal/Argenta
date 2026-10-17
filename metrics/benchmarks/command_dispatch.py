from argenta import App
from argenta.command import Flag, Flags
from argenta.command.models import Command
from argenta.repl import REPLRuntime
from argenta.response import Response
from argenta.router import Router
from metrics.benchmarks.entity import benchmarks


def _command_handler(_res: Response) -> None: ...


def setup_app(command_count: int = 20) -> App:
    app = App(override_system_messages=True)
    router = Router()
    for command_index in range(command_count):
        router.command(
            Command(
                f"cmd{command_index}",
                flags=Flags([Flag("verbose"), Flag("output")]),
            )
        )(_command_handler)
    app.include_router(router)
    app._setup_system_router()
    return app


_APP = setup_app()
_RUNTIME = REPLRuntime(_APP)


@benchmarks.register(type_="command_dispatch", description="Simple command, no flags")
def benchmark_dispatch_simple() -> None:
    _RUNTIME._dispatch_command("cmd5")


@benchmarks.register(type_="command_dispatch", description="Command with flags and a value")
def benchmark_dispatch_flags_and_values() -> None:
    _RUNTIME._dispatch_command("cmd5 --verbose --output result.txt")


@benchmarks.register(type_="command_dispatch", description="Unknown command (suggestion path)")
def benchmark_dispatch_unknown_command() -> None:
    _RUNTIME._dispatch_command("commd5")
