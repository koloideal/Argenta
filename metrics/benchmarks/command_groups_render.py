from argenta import App
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router
from metrics.benchmarks.entity import benchmarks


def _command_handler(_res: Response) -> None: ...


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
            )(_command_handler)
        app.include_router(router)
    return app


_FEW_APP = setup_app(3, 3)
_MANY_APP = setup_app(10, 10)


@benchmarks.register(
    type_="command_groups_render", description="Few routers (3 routers, 3 commands each)"
)
def benchmark_render_few_commands() -> None:
    _FEW_APP._viewer.view_command_groups_description(
        _FEW_APP._description_message_generator, _FEW_APP.registered_routers
    )


@benchmarks.register(
    type_="command_groups_render", description="Many routers (10 routers, 10 commands each)"
)
def benchmark_render_many_commands() -> None:
    _MANY_APP._viewer.view_command_groups_description(
        _MANY_APP._description_message_generator, _MANY_APP.registered_routers
    )
