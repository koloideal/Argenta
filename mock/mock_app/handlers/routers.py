from pprint import pprint
from rich.console import Console

from argenta.command import Command
from argenta.command.flag import FlagsGroup
from argenta.command.flag.defaults import DefaultFlags
from argenta.router import Router
from argenta.router.defaults import system_router
from .handlers_implementation.help_command import help_command


work_router: Router = Router(title='Work nts:')
work_router.set_invalid_input_flag_handler(lambda flag: print(f'Invalid input flag: {flag.get_string_entity()} {flag.get_value() if flag.get_value() else ''}'))

settings_router: Router = Router(title='Settings points:')


console = Console()


@work_router.command(Command(trigger='0', description='Get Help'))
def command_help():
    help_command()


@work_router.command(Command(trigger='P', description='Start Solving', flags=FlagsGroup(DefaultFlags.host_flag, DefaultFlags.port_flag)))
def command_start_solving(args: dict):
    print('Solving...')
    pprint(args)
    #start_solving_command()


@settings_router.command(Command(trigger='G', description='Update WordMath'))
def command_update():
    print('Command update')




