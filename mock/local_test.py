from argenta.response import Response, Status
from argenta.app import App
from argenta.app.dividing_line import StaticDividingLine, DynamicDividingLine
from argenta.app.autocompleter import AutoCompleter
from argenta.app.defaults import PredefinedMessages
from argenta.command import Command
from argenta.command.flags import Flags, InputFlags, InvalidValueInputFlags, UndefinedInputFlags, ValidInputFlags
from argenta.command.flag import Flag, InputFlag
from argenta.command.flag.defaults import PredefinedFlags
from argenta.router import Router
from argenta.orchestrator import Orchestrator

from argenta.command.models import InputCommand
import inspect

def some():
    ellipsis
    global inspect
    pass


print(inspect.getsourcelines(some))
