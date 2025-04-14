from typing import Callable

from argenta.command import Command
from argenta.command.flag import InputFlags



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


class CommandHandlers:
    def __init__(self, command_handlers: list[CommandHandler] = None):
        self.command_handlers = command_handlers if command_handlers else []

    def get_command_handlers(self) -> list[CommandHandler]:
        return self.command_handlers

    def add_command_handler(self, command_handler: CommandHandler):
        self.command_handlers.append(command_handler)

    def add_command_handlers(self, *command_handlers: CommandHandler):
        self.command_handlers.extend(command_handlers)

    def __iter__(self):
        return iter(self.command_handlers)

    def __next__(self):
        return next(iter(self.command_handlers))