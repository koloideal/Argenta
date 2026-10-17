from argenta import App
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router
from metrics.benchmarks.entity import benchmarks

_BENCHMARK_TYPE = "most_similar_command"
_MANY_COMMANDS_COUNT = 50
_ALIASED_COMMANDS_COUNT = 20
_EXTREME_COMMANDS_COUNT = 100
_EXTREME_ALIASES_COUNT = 20


def _command_handler(_res: Response) -> None: ...


def setup_app_with_commands(command_count: int, aliases_per_command: int = 0) -> App:
    app = App(override_system_messages=True)
    router = Router()

    for command_index in range(command_count):
        aliases = (
            {f"alias{command_index}_{alias_index}" for alias_index in range(aliases_per_command)}
            if aliases_per_command
            else set()
        )
        router.command(Command(f"command{command_index}", aliases=aliases))(_command_handler)

    app.include_router(router)
    return app


_FEW_COMMANDS_APP = setup_app_with_commands(10)
_MANY_COMMANDS_APP = setup_app_with_commands(_MANY_COMMANDS_COUNT)
_MANY_ALIASES_APP = setup_app_with_commands(_ALIASED_COMMANDS_COUNT, aliases_per_command=10)
_EXTREME_APP = setup_app_with_commands(
    _EXTREME_COMMANDS_COUNT, aliases_per_command=_EXTREME_ALIASES_COUNT
)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Few commands (10 commands, no match)")
def benchmark_few_commands() -> None:
    _FEW_COMMANDS_APP._most_similar_command("unknown")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Many commands (50 commands, no match)")
def benchmark_many_commands_most_similar() -> None:
    _MANY_COMMANDS_APP._most_similar_command("unknown")


@benchmarks.register(
    type_=_BENCHMARK_TYPE, description="Many aliases (20 commands, 10 aliases each)"
)
def benchmark_many_aliases() -> None:
    _MANY_ALIASES_APP._most_similar_command("unknown")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Partial match (50 commands, prefix match)")
def benchmark_partial_match() -> None:
    _MANY_COMMANDS_APP._most_similar_command("comm")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Extreme (100 commands, 20 aliases each)")
def benchmark_extreme_commands() -> None:
    _EXTREME_APP._most_similar_command("comm")
