from typing import Callable, Iterator

from argenta.command import Command
from argenta.command.flags.models import InputFlags



class CommandHandler:
    def __init__(self, handler: Callable[[], None] | Callable[[InputFlags], None], handled_command: Command):
        """
        Private. Entity of the model linking the handler and the command being processed
        :param handler: the handler being called
        :param handled_command: the command being processed
        """
        self._handler = handler
        self._handled_command = handled_command

    def handling(self, input_flags: InputFlags = None) -> None:
        """
        Private. Direct processing of an input command
        :param input_flags: the flags of the input command
        :return: None
        """
        if input_flags is not None:
            self._handler(input_flags)
        else:
            self._handler()

    def get_handler(self) -> Callable[[], None] | Callable[[InputFlags], None]:
        """
        Private. Returns the handler being called
        :return: the handler being called as Callable[[], None] or Callable[[InputFlags], None]
        """
        return self._handler

    def get_handled_command(self) -> Command:
        """
        Private. Returns the command being processed
        :return: the command being processed as Command
        """
        return self._handled_command


class CommandHandlers:
    def __init__(self, command_handlers: list[CommandHandler] = None):
        """
        Private. The model that unites all CommandHandler of the routers
        :param command_handlers: list of CommandHandlers for register
        """
        self.command_handlers = command_handlers if command_handlers else []

    def get_handlers(self) -> list[CommandHandler]:
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