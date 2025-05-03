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
from argenta.app.utils import most_similar_command


print(most_similar_command('case', ['case', 'tester', 'poster', 'caser']))
