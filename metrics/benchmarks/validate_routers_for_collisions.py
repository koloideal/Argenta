__all__ = [
    "benchmark_extreme_routers",
    "benchmark_few_routers",
    "benchmark_many_aliases_per_command",
    "benchmark_many_commands_per_router",
    "benchmark_many_routers",
]

from argenta import App
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router

from .entity import benchmarks


def _handler(_res: Response) -> None:
    pass


def setup_app_with_routers(
    router_count: int, commands_per_router: int = 1, aliases_per_command: int = 0
) -> App:
    app = App(override_system_messages=True)

    for router_index in range(router_count):
        router = Router()
        for command_index in range(commands_per_router):
            aliases = (
                {
                    f"alias{router_index}_{command_index}_{alias_index}"
                    for alias_index in range(aliases_per_command)
                }
                if aliases_per_command
                else set()
            )
            router.command(Command(f"cmd{router_index}_{command_index}", aliases=aliases))(_handler)
        app.include_router(router)

    app._setup_system_router()
    return app


_FEW_ROUTERS_APP = setup_app_with_routers(3)
_MANY_ROUTERS_APP = setup_app_with_routers(10)
_MANY_COMMANDS_APP = setup_app_with_routers(3, commands_per_router=10)
_MANY_ALIASES_APP = setup_app_with_routers(3, commands_per_router=5, aliases_per_command=10)
_EXTREME_APP = setup_app_with_routers(20, commands_per_router=10, aliases_per_command=20)


@benchmarks.register(
    type_="validate_routers_for_collisions",
    description="With few routers (3 routers, 1 command each)",
)
def benchmark_few_routers() -> None:
    _FEW_ROUTERS_APP._validate_routers_for_collisions()


@benchmarks.register(
    type_="validate_routers_for_collisions",
    description="With many routers (10 routers, 1 command each)",
)
def benchmark_many_routers() -> None:
    _MANY_ROUTERS_APP._validate_routers_for_collisions()


@benchmarks.register(
    type_="validate_routers_for_collisions",
    description="With many commands per router (3 routers, 10 commands each)",
)
def benchmark_many_commands_per_router() -> None:
    _MANY_COMMANDS_APP._validate_routers_for_collisions()


@benchmarks.register(
    type_="validate_routers_for_collisions",
    description="With many aliases (3 routers, 5 commands, 10 aliases each)",
)
def benchmark_many_aliases_per_command() -> None:
    _MANY_ALIASES_APP._validate_routers_for_collisions()


@benchmarks.register(
    type_="validate_routers_for_collisions",
    description="Extreme (20 routers, 10 commands, 20 aliases each)",
)
def benchmark_extreme_routers() -> None:
    _EXTREME_APP._validate_routers_for_collisions()
