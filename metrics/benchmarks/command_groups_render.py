from dataclasses import dataclass
from types import SimpleNamespace

from argenta import App
from argenta.command.models import Command
from argenta.repl import REPLConfig, TerminalLayout
from argenta.router import Router
from metrics.benchmarks._scenarios import command_handler
from metrics.benchmarks.entity import benchmarks


@dataclass(frozen=True, slots=True)
class CommandGroupsRenderConfig:
    benchmark_type: str = "command_groups_render"
    few_router_count: int = 3
    few_commands_per_router: int = 3
    many_router_count: int = 10
    many_commands_per_router: int = 10


def setup_app(router_count: int, commands_per_router: int) -> App:
    app = App()
    for router_index in range(router_count):
        router = Router(title=f"Group {router_index}")
        for command_index in range(commands_per_router):
            router.command(
                Command(
                    f"cmd{router_index}_{command_index}",
                    description=f"Does work {router_index}_{command_index}",
                )
            )(command_handler)
        app.include_router(router)
    return app


_CONFIG = CommandGroupsRenderConfig()
_APPS = SimpleNamespace(
    few=setup_app(_CONFIG.few_router_count, _CONFIG.few_commands_per_router),
    many=setup_app(_CONFIG.many_router_count, _CONFIG.many_commands_per_router),
)
_LAYOUTS = SimpleNamespace(
    few=TerminalLayout(_APPS.few.printer, _APPS.few.renderer, REPLConfig()),
    many=TerminalLayout(_APPS.many.printer, _APPS.many.renderer, REPLConfig()),
)


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Few routers (3 routers, 3 commands each)"
)
def benchmark_render_few_commands() -> None:
    _APPS.few.present_command_groups(_LAYOUTS.few)


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Many routers (10 routers, 10 commands each)"
)
def benchmark_render_many_commands() -> None:
    _APPS.many.present_command_groups(_LAYOUTS.many)
