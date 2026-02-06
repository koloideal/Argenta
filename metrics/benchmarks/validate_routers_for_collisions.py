__all__ = [
    "benchmark_few_routers",
    "benchmark_many_routers",
    "benchmark_many_commands_per_router",
    "benchmark_many_aliases_per_command",
    "benchmark_extreme_routers"
]

from argenta import App
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router

from .entity import benchmarks


@benchmarks.register(type_="validate_routers_for_collisions", description="With few routers (3 routers, 1 command each)")
def benchmark_few_routers() -> None:
    app = App(override_system_messages=True)

    for i in range(3):
        router = Router()

        @router.command(Command(f'cmd{i}'))
        def handler(_res: Response) -> None:
            pass

        app.include_router(router)

    app._setup_system_router()
    app._validate_routers_for_collisions()


@benchmarks.register(type_="validate_routers_for_collisions", description="With many routers (10 routers, 1 command each)")
def benchmark_many_routers() -> None:
    app = App(override_system_messages=True)

    for i in range(10):
        router = Router()

        @router.command(Command(f'cmd{i}'))
        def handler(_res: Response) -> None:
            pass

        app.include_router(router)

    app._setup_system_router()
    app._validate_routers_for_collisions()


@benchmarks.register(type_="validate_routers_for_collisions", description="With many commands per router (3 routers, 10 commands each)")
def benchmark_many_commands_per_router() -> None:
    app = App(override_system_messages=True)

    for i in range(3):
        router = Router()

        for j in range(10):
            @router.command(Command(f'cmd{i}_{j}'))
            def handler(_res: Response) -> None:
                pass

        app.include_router(router)

    app._setup_system_router()
    app._validate_routers_for_collisions()


@benchmarks.register(type_="validate_routers_for_collisions", description="With many aliases (3 routers, 5 commands, 10 aliases each)")
def benchmark_many_aliases_per_command() -> None:
    app = App(override_system_messages=True)

    for i in range(3):
        router = Router()

        for j in range(5):
            @router.command(Command(f'cmd{i}_{j}', aliases={f'alias{i}_{j}_{k}' for k in range(10)}))
            def handler(_res: Response) -> None:
                pass

        app.include_router(router)

    app._setup_system_router()
    app._validate_routers_for_collisions()


@benchmarks.register(type_="validate_routers_for_collisions", description="Extreme (20 routers, 10 commands, 20 aliases each)")
def benchmark_extreme_routers() -> None:
    app = App(override_system_messages=True)

    for i in range(20):
        router = Router()

        for j in range(10):
            @router.command(Command(f'cmd{i}_{j}', aliases={f'alias{i}_{j}_{k}' for k in range(20)}))
            def handler(_res: Response) -> None:
                pass

        app.include_router(router)

    app._setup_system_router()
    app._validate_routers_for_collisions()
