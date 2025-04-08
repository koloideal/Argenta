from rich.console import Console

from argenta.command import Command
from argenta.command.flag import Flags, InputFlags, Flag
from argenta.command.flag.defaults import PredeterminedFlags
from argenta.router import Router
from .handlers_implementation.help_command import help_command


work_router: Router = Router(title='Work points:')
work_router.set_invalid_input_flag_handler(lambda flag: print(f'Invalid input flag: {flag.get_string_entity()} {flag.get_value() if flag.get_value() else ''}'))

settings_router: Router = Router(title='Settings points:')


console = Console()

flag = Flag('test')


@work_router.command(Command('0', 'Get Help'))
def command_help():
    help_command()


@work_router.command(Command('S', 'Start Solving', Flags(PredeterminedFlags.HOST, PredeterminedFlags.PORT, flag)))
def command_start_solving(args: InputFlags):
    print(args.get_flag('test'))


@settings_router.command(Command('U', 'Update WordMath'))
def command_update():
    pass




