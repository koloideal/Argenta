from rich.console import Console

from argenta.command.entity import Command
from argenta.command.params.flag.flags_group.entity import FlagsGroup
from argenta.router import Router

from ..handlers.handlers_implementation.help_command import help_command

work_router: Router = Router(title='Work points:')
settings_router: Router = Router(title='Settings points:')

console = Console()


@work_router.command(command=Command(command='0', description='Get Help'))
def command_help(args: FlagsGroup):
    print(args.get_flags())
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    help_command()


'''@work_router.command(command='1', description='Start Solving')
def command_start_solving():
    start_solving_command()


@settings_router.command(command='U', description='Update WordMath')
def command_update():
    upgrade_command()'''


@work_router.unknown_command
def command_unknown_command(command):
    console.print(f'[bold red]Unknown command: [/bold red]{command}')
