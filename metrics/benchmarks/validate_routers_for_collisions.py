from dataclasses import dataclass
from types import SimpleNamespace

from argenta import App
from argenta.command.models import Command
from argenta.router import Router
from metrics.benchmarks._scenarios import command_handler
from metrics.benchmarks.entity import benchmarks


@dataclass(frozen=True, slots=True)
class ValidateRoutersConfig:
    benchmark_type: str = "validate_routers_for_collisions"
    few_routers_count: int = 3
    many_routers_count: int = 10
    many_commands_per_router: int = 10
    aliased_commands_per_router: int = 5
    aliases_per_command: int = 10
    extreme_routers_count: int = 20
    extreme_commands_per_router: int = 10
    extreme_aliases_per_command: int = 20


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
            router.command(Command(f"cmd{router_index}_{command_index}", aliases=aliases))(
                command_handler
            )
        app.include_router(router)

    app._setup_system_router()
    return app


_CONFIG = ValidateRoutersConfig()
_APPS = SimpleNamespace(
    few_routers=setup_app_with_routers(_CONFIG.few_routers_count),
    many_routers=setup_app_with_routers(_CONFIG.many_routers_count),
    many_commands=setup_app_with_routers(
        _CONFIG.few_routers_count, commands_per_router=_CONFIG.many_commands_per_router
    ),
    many_aliases=setup_app_with_routers(
        _CONFIG.few_routers_count,
        commands_per_router=_CONFIG.aliased_commands_per_router,
        aliases_per_command=_CONFIG.aliases_per_command,
    ),
    extreme=setup_app_with_routers(
        _CONFIG.extreme_routers_count,
        commands_per_router=_CONFIG.extreme_commands_per_router,
        aliases_per_command=_CONFIG.extreme_aliases_per_command,
    ),
)


@benchmarks.register(
    type_=_CONFIG.benchmark_type,
    description="With few routers (3 routers, 1 command each)",
)
def benchmark_few_routers() -> None:
    _APPS.few_routers._validate_routers_for_collisions()


@benchmarks.register(
    type_=_CONFIG.benchmark_type,
    description="With many routers (10 routers, 1 command each)",
)
def benchmark_many_routers() -> None:
    _APPS.many_routers._validate_routers_for_collisions()


@benchmarks.register(
    type_=_CONFIG.benchmark_type,
    description="With many commands per router (3 routers, 10 commands each)",
)
def benchmark_many_commands_per_router() -> None:
    _APPS.many_commands._validate_routers_for_collisions()


@benchmarks.register(
    type_=_CONFIG.benchmark_type,
    description="With many aliases (3 routers, 5 commands, 10 aliases each)",
)
def benchmark_many_aliases_per_command() -> None:
    _APPS.many_aliases._validate_routers_for_collisions()


@benchmarks.register(
    type_=_CONFIG.benchmark_type,
    description="Extreme (20 routers, 10 commands, 20 aliases each)",
)
def benchmark_extreme_routers() -> None:
    _APPS.extreme._validate_routers_for_collisions()
