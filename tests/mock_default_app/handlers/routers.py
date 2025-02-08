from rich.console import Console
from argenta.router import Router


work_router: Router = Router(name='Work points:',
                             ignore_command_register=False)
settings_router: Router = Router(name='Settings points:',
                                 ignore_command_register=True)

console = Console()


@work_router.command(command='0', description='Get Help')
def command_help():
    print('help command')


@work_router.command(command='1', description='Start Solving')
def command_start_solving():
    print('start solving')


@settings_router.command(command='U', description='Update WordMath')
def command_update():
    print('update wordmath')


@work_router.unknown_command
def command_unknown_command(command):
    console.print(f'[bold red]Unknown command: [/bold red]{command}')
