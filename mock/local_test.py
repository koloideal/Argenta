from argenta.router import Router
from argenta.command import Command
from argenta.response import Response
from argenta.metrics import get_time_of_pre_cycle_setup
from argenta.response.status import Status
from argenta.command.flag import Flag, Flags
from argenta.app import App
from argenta.orchestrator import Orchestrator


router = Router()

@router.command(Command('case are'))
def handler(response: Response):
    print(response.status)



app = App(repeat_command_groups=False)
app.include_router(router)

app.run_polling()









