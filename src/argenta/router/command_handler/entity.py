__all__ = ["CommandHandler", "CommandHandlers"]

from collections.abc import Iterator
from typing import Callable

from argenta.command import Command
from argenta.response import Response


class CommandHandler:
    def __init__(self, handler_as_func: Callable[..., None], handled_command: Command):
        """
        Private. Entity of the model linking the handler and the command being processed
        :param handler: the handler being called
        :param handled_command: the command being processed
        """
        self.handler_as_func: Callable[..., None] = handler_as_func
        self.handled_command: Command = handled_command

    def handling(self, response: Response) -> None:
        """
        Private. Direct processing of an input command
        :param response: the entity of response: various groups of flags and status of response
        :return: None
        """
        self.handler_as_func(response)


class CommandHandlers:
    def __init__(self, command_handlers: list[CommandHandler] | None = None):
        """
        Private. The model that unites all CommandHandler of the routers
        :param command_handlers: list of CommandHandlers for register
        """
        self.command_handlers: list[CommandHandler] = command_handlers if command_handlers else []

    def add_handler(self, command_handler: CommandHandler) -> None:
        """
        Private. Adds a CommandHandler to the list of CommandHandlers
        :param command_handler: CommandHandler to be added
        :return: None
        """
        self.command_handlers.append(command_handler)

    def __iter__(self) -> Iterator[CommandHandler]:
        return iter(self.command_handlers)

    def __next__(self) -> CommandHandler:
        return next(iter(self.command_handlers))
