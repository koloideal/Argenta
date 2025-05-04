from rich.console import Console

from argenta.command import Command
from argenta.command.flag.defaults import PredefinedFlags
from argenta.command.flags import Flags
from argenta.response import Response
from argenta.router import Router


work_router: Router = Router(title='Work points:')

console = Console()


@work_router.command(Command('get', 'Get Help', aliases=['help', 'Get_help'], flags=Flags(PredefinedFlags.PORT, PredefinedFlags.HOST)))
def command_help(response: int):
    print(response.status)
    print(response.undefined_flags.get_flags())
    print(response.valid_flags.get_flags())
    print(response.invalid_value_flags.get_flags())


@work_router.command(Command('run', 'Run All'))
def command_start_solving(response: str):
    print(response.status)
    print(response.undefined_flags.get_flags())
    print(response.valid_flags.get_flags())
    print(response.invalid_value_flags.get_flags())



