from argenta.app.dividing_line.models import DynamicDividingLine
from argenta.app.models import App
from argenta.command.flag.models import Flag, ValidationStatus
from argenta.command.models import Command
from argenta.orchestrator import ArgParser
from argenta.orchestrator.argparser import PositionalArgument
from argenta.orchestrator.entity import Orchestrator
from argenta.response.entity import Response
from argenta.router.entity import Router


router = Router(disable_redirect_stdout=True)
orchestrator = Orchestrator(ArgParser([PositionalArgument('test')]))

print(orchestrator.get_input_args())

@router.command(Command('test', flags=Flag('case', possible_values=['1', '2', '3'])))
def test(response: Response):
    undefined_flag = response.input_flags.get_flag("port")
    if undefined_flag and undefined_flag.get_status() == ValidationStatus.UNDEFINED:
        print(f'test command with undefined flag with value: {undefined_flag.get_string_entity()} {undefined_flag.get_value()}')
    else:
        pass

app = App(dividing_line=DynamicDividingLine())
app.include_router(router)
orchestrator.start_polling(app)