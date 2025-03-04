from typing import Callable, Any
from inspect import getfullargspec

from ..command.entity import Command
from ..command.params.flag.entity import Flag
from ..command.params.flag.flags_group.entity import FlagsGroup
from ..router.exceptions import (RepeatedCommandException,
                                 RepeatedFlagNameException,
                                 TooManyTransferredArgsException,
                                 RequiredArgumentNotPassedException,
                                 IncorrectNumberOfHandlerArgsException)


class Router:
    def __init__(self,
                 title: str = 'Commands group title:',
                 name: str = 'subordinate'):

        self._title = title
        self._name = name

        self._command_entities: list[dict[str, Callable[[], None] | Command]] = []
        self._ignore_command_register: bool = False

        self._not_valid_flag_handler: Callable[[Flag], None] = lambda flag: print(f"Undefined or incorrect input flag: '{flag.get_string_entity()} {flag.get_value()}'")


    def command(self, command: Command) -> Callable[[Any],  Any]:
        self._validate_command(command)

        def command_decorator(func):
            Router._validate_func_args(command, func)
            self._command_entities.append({'handler_func': func,
                                           'command': command})
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        return command_decorator

    def set_invalid_input_flag_handler(self, func):
        processed_args = getfullargspec(func).args
        if len(processed_args) != 1:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._not_valid_flag_handler = func


    def input_command_handler(self, input_command: Command):
        input_command_name: str = input_command.get_trigger()
        input_command_flags: FlagsGroup = input_command.get_input_flags()
        for command_entity in self._command_entities:
            if input_command_name.lower() == command_entity['command'].get_trigger().lower():
                if command_entity['command'].get_registered_flags():
                    if input_command_flags:
                        for flag in input_command_flags:
                            is_valid = command_entity['command'].validate_input_flag(flag)
                            if not is_valid:
                                self._not_valid_flag_handler(flag)
                                return
                        return command_entity['handler_func'](input_command_flags.unparse_to_dict())
                    else:
                        return command_entity['handler_func']({})
                else:
                    if input_command_flags:
                        self._not_valid_flag_handler(input_command_flags[0])
                        return
                    else:
                        return command_entity['handler_func']()


    def _validate_command(self, command: Command):
        command_name: str = command.get_trigger()
        if command_name in self.get_all_commands():
            raise RepeatedCommandException()
        if self._ignore_command_register:
            if command_name.lower() in [x.lower() for x in self.get_all_commands()]:
                raise RepeatedCommandException()

        flags: FlagsGroup = command.get_registered_flags()
        if flags:
            flags_name: list = [x.get_string_entity().lower() for x in flags]
            if len(set(flags_name)) < len(flags_name):
                raise RepeatedFlagNameException()


    @staticmethod
    def _validate_func_args(command: Command, func: Callable):
        registered_args = command.get_registered_flags()
        transferred_args = getfullargspec(func).args
        if registered_args and transferred_args:
           if len(transferred_args) != 1:
                raise TooManyTransferredArgsException()
        elif registered_args and not transferred_args:
            raise RequiredArgumentNotPassedException()
        elif not registered_args and transferred_args:
            raise TooManyTransferredArgsException()


    def set_ignore_command_register(self, ignore_command_register: bool):
        self._ignore_command_register = ignore_command_register


    def get_command_entities(self) -> list[dict[str, Callable[[], None] | Command]]:
        return self._command_entities


    def get_name(self) -> str:
        return self._name


    def get_title(self) -> str:
        return self._title


    def get_all_commands(self) -> list[str]:
        all_commands: list[str] = []
        for command_entity in self._command_entities:
            all_commands.append(command_entity['command'].get_trigger())

        return all_commands
