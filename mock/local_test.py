from argenta.app.dividing_line.models import DynamicDividingLine
from argenta.app.models import App
from argenta.command.flag.models import Flag, ValidationStatus
from argenta.command import InputCommand
from argenta.orchestrator import ArgParser
from argenta.orchestrator.argparser import PositionalArgument
from argenta.orchestrator.entity import Orchestrator
from argenta.response.entity import Response
from argenta.router.entity import Router


parsed = InputCommand.parse('--port --host 22')


print(f'trigger: {parsed.trigger}\n')
for flag in parsed.input_flags:
    print(f'flag: {flag}')
