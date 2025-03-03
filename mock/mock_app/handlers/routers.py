import re
from pprint import pprint

from rich.console import Console

from argenta.command.entity import Command
from argenta.command.params.flag.entity import Flag
from argenta.command.params.flag.flags_group.entity import FlagsGroup
from argenta.router import Router


work_router: Router = Router(title='Work nts:')
settings_router: Router = Router(title='Settings points:')

console = Console()

flagi = FlagsGroup(flags=[
    Flag(flag_name='host',
         flag_prefix='--',
         possible_flag_values=re.compile(r'^192.168.\d{1,3}.\d{1,3}$')),
    Flag(flag_name='port',
         flag_prefix='--', )
])


@work_router.command(Command(command='0', description='Get Help'))
def command_help():
    print('Help command')
    '''flags = args.get_flags()
    for flag in flags:
        print(f'name: "{flag.get_string_entity()}", value: "{flag.get_value()}"')'''
    #help_command()


@work_router.command(Command(command='P', description='Start Solving', flags=flagi))
def command_start_solving(argrrtrts: dict):
    print('Solving...')
    pprint(argrrtrts)
    #start_solving_command()


@settings_router.command(Command(command='G', description='Update WordMath'))
def command_update():
    print('uefi')
    # upgrade_command()


def invalid_input_flag(flag: Flag):
    print(f'Invalid inpuuuuuuuuuuuuuuuuuuuuuuuut flag: "{flag.get_string_entity()} {flag.get_value()}"')


work_router.set_invalid_input_flag_handler(invalid_input_flag)



