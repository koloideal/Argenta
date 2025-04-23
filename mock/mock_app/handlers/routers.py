from rich.console import Console

from argenta.command import Command
from argenta.command.flag import Flags, InputFlags
from argenta.command.flag.defaults import PredefinedFlags
from argenta.router import Router
from .handlers_implementation.help_command import help_command


work_router: Router = Router(title='Work points:')

console = Console()


@work_router.command(Command('get', 'Get Help', aliases=['help', 'Get_help']))
def command_help():
    pass


@work_router.command(Command('run', 'Run All'))
def command_start_solving():
    pass



