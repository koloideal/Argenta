from typing import Callable
from argenta.command import Command


class CommandHandler:
    def __init__(self, handler: Callable[[], None] | Callable[[dict], None], handled_command: Command):
        self.handler = handler
        self.handled_command = handled_command

    def handling(self, input_flags: dict = None):
        if input_flags is not None:
            self.handler(input_flags)
        else:
            self.handler()

    def get_handler(self):
        return self.handler

    def get_handled_command(self):
        return self.handled_command


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









