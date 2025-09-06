from typing import Callable, Iterator

from argenta.command import Command
from argenta.response import Response


class CommandHandler:
    def __init__(self, handler: Callable[[Response], None], handled_command: Command):
        """
        Private. Entity of the model linking the handler and the command being processed
        :param handler: the handler being called
        :param handled_command: the command being processed
        """
        self._handler = handler
        self._handled_command = handled_command

    def handling(self, response: Response) -> None:
        """
        Private. Direct processing of an input command
        :param response: the entity of response: various groups of flags and status of response
        :return: None
        """
        self._handler(response)

    @property
    def handler(self) -> Callable[[Response], None]:
        """
        Private. Returns the handler being called
        :return: the handler being called as Callable[[Response], None]
        """
        return self._handler

    @property
    def handled_command(self) -> Command:
        """
        Private. Returns the command being processed
        :return: the command being processed as Command
        """
        return self._handled_command


class CommandHandlers:
    def __init__(self, command_handlers: list[CommandHandler] | None = None):
        """
        Private. The model that unites all CommandHandler of the routers
        :param command_handlers: list of CommandHandlers for register
        """
        self.command_handlers = command_handlers if command_handlers else []

    @property
    def handlers(self) -> list[CommandHandler]:
        """
        Private. Returns the list of CommandHandlers
        :return: the list of CommandHandlers as list[CommandHandler]
        """
        return self.command_handlers

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
