from argenta.command import Command
from argenta.metrics import get_time_of_pre_cycle_setup
from argenta.response import Response
from argenta.router import Router
from argenta.app import App



def commands_with_two_aliases(num_of_commands: int):
    router = Router()

    for i in range(num_of_commands):
        @router.command(Command(f'cmd{i}', aliases=[f'cdr{i}', f'prt{i}']))
        def handler(response: Response):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            pass

    app = App()
    app.include_router(router)

    return get_time_of_pre_cycle_setup(app)

def commands_with_one_aliases(num_of_commands: int):
    router = Router()

    for i in range(num_of_commands):
        @router.command(Command(f'cmd{i}', aliases=[f'cdr{i}']))
        def handler(response: Response):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            pass

    app = App()
    app.include_router(router)

    return get_time_of_pre_cycle_setup(app)
