from argenta.command import Command
from argenta.metrics import get_time_of_pre_cycle_setup
from argenta.response import Response
from argenta.router import Router
from argenta.app import App


router = Router()

for i in range(10000):
    @router.command(Command(f'cmd{i}', aliases=[f'cdr{i}', f'prt{i}']))
    def handler(response: Response):
        pass

app = App()
app.include_router(router)

print(get_time_of_pre_cycle_setup(app))
