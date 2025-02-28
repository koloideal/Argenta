from rich.console import Console

from argenta.command.entity import Command
from argenta.command.params.flag.entity import Flag
from argenta.command.params.flag.flags_group.entity import FlagsGroup
from argenta.router import Router

from ..handlers.handlers_implementation.help_command import help_command

work_router: Router = Router(title='Work points:')
settings_router: Router = Router(title='Settings points:')

console = Console()

flagi = FlagsGroup(flags=[
    Flag(flag_name='host',
         flag_prefix='--', ),
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
def command_start_solving(argrrtrts: FlagsGroup | None):
    print('Solving...')
    flags = argrrtrts.get_flags()
    for flag in flags:
        print(f'name: "{flag.get_string_entity()}", value: "{flag.get_value()}"')
    #start_solving_command()


@settings_router.command(Command(command='G', description='Update WordMath'))
def command_update():
    print('uefi')
    # upgrade_command()
