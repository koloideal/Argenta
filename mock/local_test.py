from argenta.app import App
from argenta.command import Command
from argenta.orchestrator import Orchestrator
from argenta.router import Router


router = Router()
orchestrator = Orchestrator()

@router.command(Command('test'))
def test(response):
    print('test command')

app = App(ignore_command_register=True,
          override_system_messages=True,
          print_func=print)
app.include_router(router)
orchestrator.start_polling(app)