from rich.console import Console

from argenta.command import Command
from argenta.router import Router


work_router: Router = Router(title='Work points:')

console = Console()


@work_router.command(Command('get', 'Get Help', aliases=['help', 'Get_help']))
def command_help():
    pass


@work_router.command(Command('run', 'Run All'))
def command_start_solving():
    pass



