from argenta.app.models import App
from argenta.command.flag.defaults import PredefinedFlags
from argenta.command.flag.flags.models import Flags, InputFlags
from argenta.command.flag.models import Flag, InputFlag, PossibleValues, ValidationStatus
from argenta.command.models import Command
from argenta.orchestrator.entity import Orchestrator
from argenta.response.entity import Response
from argenta.router.entity import Router


router = Router()
orchestrator = Orchestrator()

@router.command(Command('test'))
def test(response: Response):
    undefined_flag = response.input_flags.get_flag("port")
    print(response.input_flags.get_flags())
    if undefined_flag and undefined_flag.get_status() == ValidationStatus.UNDEFINED:
        print(f'test command with undefined flag with value: {undefined_flag.get_string_entity()} {undefined_flag.get_value()}')

app = App(override_system_messages=True,
            print_func=print)
app.include_router(router)
orchestrator.start_polling(app)