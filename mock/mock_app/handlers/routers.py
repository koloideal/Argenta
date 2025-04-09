from rich.console import Console

from argenta.command import Command
from argenta.command.flag import Flags, InputFlags
from argenta.command.flag.defaults import PredeterminedFlags
from argenta.router import Router
from .handlers_implementation.help_command import help_command


work_router: Router = Router(title='Work points:')

settings_router: Router = Router(title='Settings points:')

console = Console()


@work_router.command(Command('get', 'Get Help'))
def command_help():
    help_command()


@work_router.command(Command('start', 'Start Solving', Flags(PredeterminedFlags.HOST, PredeterminedFlags.PORT)))
def command_start_solving(args: InputFlags):
    print(args.get_flag('test'))


@settings_router.command(Command('update', 'Update WordMath'))
def command_update():
    print('eeeeeee')




