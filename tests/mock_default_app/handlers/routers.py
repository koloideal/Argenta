from rich.console import Console
from argenta.router import Router


work_router: Router = Router(name='work')
settings_router: Router = Router(name='settings')

console = Console()


@work_router.command(command='2')
def command_help():
    console.print('[bold red]command help [/bold red]')


@work_router.command(command='2', description='txiyxykkkkkkkkkkkk')
def command_start_solving():
    console.print('[bold red]command start [/bold red]')


@settings_router.command(command='2')
def command_settings():
    console.print('[bold red]command settings [/bold red]')


@work_router.unknown_command
def command_unknown_command(command):
    console.print(f'[bold red]Unknown command: [/bold red]{command}')
