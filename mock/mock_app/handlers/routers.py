import re
from pprint import pprint
from rich.console import Console

from argenta.command.entity import Command
from argenta.command.params.flag.entity import Flag
from argenta.command.params.flag.flags_group.entity import FlagsGroup
from argenta.router import Router
from .handlers_implementation.help_command import help_command


work_router: Router = Router(title='Work nts:')
work_router.set_invalid_input_flag_handler(lambda flag: print(f'Invalid input flag: "{flag.get_string_entity()} {flag.get_value()}"'))

settings_router: Router = Router(title='Settings points:')


console = Console()


flags = FlagsGroup(flags=[
    Flag(flag_name='host',
         flag_prefix='--',
         possible_flag_values=re.compile(r'^192.168.\d{1,3}.\d{1,3}$')),
    Flag(flag_name='port',
         flag_prefix='--', )
])


@work_router.command(Command(trigger='0', description='Get Help'))
def command_help():
    help_command()


@work_router.command(Command(trigger='--gbP', description='Start Solving', flags=flags))
def command_start_solving(args: dict):
    print('Solving...')
    pprint(args)
    #start_solving_command()


@settings_router.command(Command(trigger='G', description='Update WordMath'))
def command_update():
    print('Command update')



