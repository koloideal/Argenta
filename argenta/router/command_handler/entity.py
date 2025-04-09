from typing import Callable
from argenta.command import Command
from argenta.command.flag.models import InputFlags


class CommandHandler:
    def __init__(self, handler: Callable[[], None] | Callable[[InputFlags], None], handled_command: Command):
        self._handler = handler
        self._handled_command = handled_command

    def handling(self, input_flags: InputFlags = None):
        if input_flags is not None:
            self._handler(input_flags)
        else:
            self._handler()

    def get_handler(self):
        return self._handler

    def get_handled_command(self):
        return self._handled_command