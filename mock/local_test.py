from argenta.router import Router
from argenta.command import Command
from argenta.response import Response
from argenta.metrics import get_time_of_pre_cycle_setup
from argenta.response.status import Status
from argenta.command.flag import Flag, Flags
from argenta.app import App
from argenta.orchestrator import Orchestrator


router = Router()

for i in range(10000):
    trigger = f"cmd{i}"

    @router.command(Command(trigger, aliases=[f'dfs{i}', f'fds{i}']))
    def handler(response: Response):
        print(response.status)



app = App(repeat_command_groups=False)
app.include_router(router)

print(get_time_of_pre_cycle_setup(app))







