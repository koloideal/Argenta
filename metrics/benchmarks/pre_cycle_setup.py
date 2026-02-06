__all__ = [
    "benchmark_no_aliases",
    "benchmark_with_many_aliases",
    "benchmark_few_aliases",
    "benchmark_extreme_aliases",
    "benchmark_very_many_aliases"
]

from argenta import App
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router

from .entity import benchmarks


@benchmarks.register(type_="pre_cycle_setup", description="With no aliases")
def benchmark_no_aliases() -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command1'))
    def handler1(_res: Response) -> None:  
        pass

    @router.command(Command('command2'))
    def handler2(_res: Response) -> None:  
        pass

    @router.command(Command('command3'))
    def handler3(_res: Response) -> None:  
        pass

    app.include_router(router)
    app._pre_cycle_setup()


@benchmarks.register(type_="pre_cycle_setup", description="With few aliases (6 total)")
def benchmark_few_aliases() -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command1', aliases={'c1', 'cmd1'}))
    def handler1(_res: Response) -> None:  
        pass

    @router.command(Command('command2', aliases={'c2', 'cmd2'}))
    def handler2(_res: Response) -> None:  
        pass

    @router.command(Command('command3', aliases={'c3', 'cmd3'}))
    def handler3(_res: Response) -> None:  
        pass

    app.include_router(router)
    app._pre_cycle_setup()


@benchmarks.register(type_="pre_cycle_setup", description="With many aliases (15 total)")
def benchmark_with_many_aliases() -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command1', aliases={'c1', 'cmd1', 'com1', 'first', 'one'}))
    def handler1(_res: Response) -> None:  
        pass

    @router.command(Command('command2', aliases={'c2', 'cmd2', 'com2', 'second', 'two'}))
    def handler2(_res: Response) -> None:  
        pass

    @router.command(Command('command3', aliases={'c3', 'cmd3', 'com3', 'third', 'three'}))
    def handler3(_res: Response) -> None:  
        pass

    app.include_router(router)
    app._pre_cycle_setup()


@benchmarks.register(type_="pre_cycle_setup", description="With very many aliases (60 total)")
def benchmark_very_many_aliases() -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command1', aliases={f'alias1_{i}' for i in range(20)}))
    def handler1(_res: Response) -> None:  
        pass

    @router.command(Command('command2', aliases={f'alias2_{i}' for i in range(20)}))
    def handler2(_res: Response) -> None:  
        pass

    @router.command(Command('command3', aliases={f'alias3_{i}' for i in range(20)}))
    def handler3(_res: Response) -> None: 
        pass

    app.include_router(router)
    app._pre_cycle_setup()


@benchmarks.register(type_="pre_cycle_setup", description="With extreme aliases (300 total)")
def benchmark_extreme_aliases() -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command1', aliases={f'alias1_{i}' for i in range(100)}))
    def handler1(_res: Response) -> None:  
        pass

    @router.command(Command('command2', aliases={f'alias2_{i}' for i in range(100)}))
    def handler2(_res: Response) -> None:  
        pass

    @router.command(Command('command3', aliases={f'alias3_{i}' for i in range(100)}))
    def handler3(_res: Response) -> None:  
        pass

    app.include_router(router)
    app._pre_cycle_setup()
