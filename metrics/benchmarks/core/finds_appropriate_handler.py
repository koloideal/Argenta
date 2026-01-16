__all__ = [
    "benchmark_simple_command",
    "benchmark_command_with_flags",
    "benchmark_many_commands",
    "benchmark_command_with_many_flags",
    "benchmark_extreme_router"
]

from argenta.command.models import Command, InputCommand
from argenta.command import Flag, Flags
from argenta.response import Response
from argenta.router import Router

from ..models import benchmark
from ..utils import get_time_of_finds_appropriate_handler


@benchmark(type_="finds_appropriate_handler", description="Simple command (no flags)")
def benchmark_simple_command() -> float:
    router = Router()

    @router.command(Command('test'))
    def handler(_res: Response) -> None:
        pass

    input_cmd = InputCommand.parse('test')
    return get_time_of_finds_appropriate_handler(router, input_cmd)


@benchmark(type_="finds_appropriate_handler", description="Command with flags (3 flags)")
def benchmark_command_with_flags() -> float:
    router = Router()

    @router.command(Command('test', flags=Flags([Flag('a'), Flag('b'), Flag('c')])))
    def handler(_res: Response) -> None:
        pass

    input_cmd = InputCommand.parse('test -a -b -c')
    return get_time_of_finds_appropriate_handler(router, input_cmd)


@benchmark(type_="finds_appropriate_handler", description="Many commands (50 commands)")
def benchmark_many_commands() -> float:
    router = Router()

    for i in range(50):
        @router.command(Command(f'cmd{i}'))
        def handler(_res: Response) -> None:
            pass

    input_cmd = InputCommand.parse('cmd25')
    return get_time_of_finds_appropriate_handler(router, input_cmd)


@benchmark(type_="finds_appropriate_handler", description="Command with many flags (20 flags)")
def benchmark_command_with_many_flags() -> float:
    router = Router()

    flags = Flags([Flag(f'flag{i}') for i in range(20)])

    @router.command(Command('test', flags=flags))
    def handler(_res: Response) -> None:
        pass

    input_cmd = InputCommand.parse('test ' + ' '.join(f'-flag{i}' for i in range(10)))
    return get_time_of_finds_appropriate_handler(router, input_cmd)


@benchmark(type_="finds_appropriate_handler", description="Extreme (100 commands, 10 flags each)")
def benchmark_extreme_router() -> float:
    router = Router()

    for i in range(100):
        flags = Flags([Flag(f'f{i}_{j}') for j in range(10)])

        @router.command(Command(f'cmd{i}', flags=flags))
        def handler(_res: Response) -> None:
            pass

    input_cmd = InputCommand.parse('cmd50 -f50_0 -f50_1 -f50_2')
    return get_time_of_finds_appropriate_handler(router, input_cmd)
