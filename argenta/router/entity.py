from typing import Callable, Any
from ..router.exceptions import (InvalidCommandInstanceException,
                                 UnknownCommandHandlerHasAlreadyBeenCreatedException,
                                 InvalidDescriptionInstanceException,
                                 RepeatedCommandException)


class Router:
    def __init__(self,
                 title: str = 'Commands group title:',
                 name: str = 'subordinate',
                 ignore_command_register: bool = False):

        self.ignore_command_register = ignore_command_register
        self.title = title
        self.name = name

        self._command_entities: list[dict[str, Callable[[], None] | str]] = []
        self.unknown_command_func: Callable[[str], None] | None = None
        self._is_main_router: bool = False


    def command(self, command: str, description: str = None) -> Callable[[Any],  Any]:
        processed_description = Router._validate_description(command, description)
        self._validate_command(command)

        def command_decorator(func):
            self._command_entities.append({'handler_func': func,
                                           'command': command,
                                           'description': processed_description})
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        return command_decorator


    def unknown_command(self, func):
        if self.unknown_command_func is not None:
            raise UnknownCommandHandlerHasAlreadyBeenCreatedException()

        self.unknown_command_func: Callable = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


    def input_command_handler(self, input_command):
        for command_entity in self._command_entities:
            if input_command.lower() == command_entity['command'].lower():
                if self.ignore_command_register:
                    return command_entity['handler_func']()
                else:
                    if input_command == command_entity['command']:
                        return command_entity['handler_func']()


    def unknown_command_handler(self, unknown_command):
        self.unknown_command_func(unknown_command)


    def _validate_command(self, command: str):
        if not isinstance(command, str):
            raise InvalidCommandInstanceException()
        if command in self.get_all_commands():
            raise RepeatedCommandException()
        if self.ignore_command_register:
            if command.lower() in [x.lower() for x in self.get_all_commands()]:
                raise RepeatedCommandException()


    @staticmethod
    def _validate_description(command: str, description: str):
        if not isinstance(description, str):
            if description is None:
                description = f'description for "{command}" command'
            else:
                raise InvalidDescriptionInstanceException()
        return description


    def set_router_as_main(self):
        if self.name == 'subordinate':
            self.name = 'main'
        self._is_main_router = True


    def get_command_entities(self) -> list[dict[str, Callable[[], None] | str]]:
        return self._command_entities


    def get_name(self) -> str:
        return self.name


    def get_title(self) -> str:
        return self.title


    def get_router_info(self) -> dict:
        return {
            'title': self.title,
            'name': self.name,
            'ignore_command_register': self.ignore_command_register,
            'attributes': {
                'command_entities': self._command_entities,
                'unknown_command_func': self.unknown_command_func,
                'is_main_router': self._is_main_router
            }

        }


    def get_all_commands(self) -> list[str]:
        all_commands: list[str] = []
        for command_entity in self._command_entities:
            all_commands.append(command_entity['command'])

        return all_commands
