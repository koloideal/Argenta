from typing import Callable, Any
from src.core.router.exceptions import (InvalidCommandInstanceException,
                                        UnknownCommandHandlerHasAlreadyBeenCreatedException,
                                        InvalidDescriptionInstanceException)


class Router:
    def __init__(self,
                 name: str,
                 ignore_command_register: bool = False):

        self.ignore_command_register: bool = ignore_command_register
        self._name = name

        self.processed_commands: list[dict[str, Callable[[], None] | str]] = []
        self.unknown_command_func: Callable[[str], None] | None = None
        self._is_main_router: bool = False


    def command(self, command: str, description: str) -> Callable[[Any], Any]:
        if not isinstance(command, str):
            raise InvalidCommandInstanceException()
        if not isinstance(description, str):
            raise InvalidDescriptionInstanceException()
        else:
            def command_decorator(func):
                self.processed_commands.append({'func': func,
                                                'command': command,
                                                'description': description})
                def wrapper(*args, **kwargs):
                    return func(*args, **kwargs)
                return wrapper
            return command_decorator


    def unknown_command(self, func):
        if self.unknown_command_func is not None:
            raise UnknownCommandHandlerHasAlreadyBeenCreatedException()

        self.unknown_command_func = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


    def input_command_handler(self, input_command):
        for command_entity in self.processed_commands:
            if input_command.lower() == command_entity['command'].lower():
                if self.ignore_command_register:
                    return command_entity['func']()
                else:
                    if input_command == command_entity['command']:
                        return command_entity['func']()

    def unknown_command_handler(self, unknown_command):
        self.unknown_command_func(unknown_command)


    def set_router_as_main(self):
        self._is_main_router = True


    def get_registered_commands(self) -> list[dict[str, Callable[[], None] | str]]:
        return self.processed_commands


    def get_name(self) -> str:
        return self._name

