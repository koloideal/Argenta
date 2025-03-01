from typing import Callable, Any
from inspect import getfullargspec
from ..command.entity import Command
from ..command.params.flag.flags_group.entity import FlagsGroup
from ..router.exceptions import (RepeatedCommandException, RepeatedFlagNameException,
                                 TooManyTransferredArgsException,
                                 RequiredArgumentNotPassedException,
                                 NotValidInputFlagHandlerHasBeenAlreadyCreatedException,
                                 IncorrectNumberOfHandlerArgsException)


class Router:
    def __init__(self,
                 title: str = 'Commands group title:',
                 name: str = 'subordinate'):

        self.title = title
        self.name = name

        self._command_entities: list[dict[str, Callable[[], None] | Command]] = []
        self._ignore_command_register: bool = False

        self._not_valid_flag_handler: Callable[[Command], None] | None = None


    def command(self, command: Command) -> Callable[[Any],  Any]:
        command.validate_commands_params()
        self._validate_command(command)

        def command_decorator(func):
            Router._validate_func_args(command, func)
            self._command_entities.append({'handler_func': func,
                                           'command': command})
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        return command_decorator

    def not_valid_input_flag(self, func):
        if self._not_valid_flag_handler:
            raise NotValidInputFlagHandlerHasBeenAlreadyCreatedException()
        else:
            processed_args = getfullargspec(func).args
            if len(processed_args) != 1:
                raise IncorrectNumberOfHandlerArgsException()
            else:
                self._not_valid_flag_handler = func
                def wrapper(*args, **kwargs):
                    return func(*args, **kwargs)

                return wrapper


    def input_command_handler(self, input_command: Command):
        input_command_name: str = input_command.get_string_entity()
        input_command_flags: FlagsGroup = input_command.get_input_flags()
        for command_entity in self._command_entities:
            if input_command_name.lower() == command_entity['command'].get_string_entity().lower():
                if command_entity['command'].get_registered_flags():
                    if input_command_flags:
                        for flag in input_command_flags:
                            is_valid = command_entity['command'].validate_input_flag(flag)
                            if not is_valid:
                                if self._not_valid_flag_handler:
                                    self._not_valid_flag_handler(input_command)
                                else:
                                    print(f"Undefined or incorrect input flag: '{flag.get_string_entity()} {flag.get_value()}'")
                                return
                        return command_entity['handler_func'](input_command_flags)
                    else:
                        return command_entity['handler_func'](FlagsGroup(None))
                else:
                    if input_command_flags:
                        if self._not_valid_flag_handler:
                            self._not_valid_flag_handler(input_command)
                        else:
                            print(f"Undefined or incorrect input flag: '{input_command_flags[0].get_string_entity()} {input_command_flags[0].get_value()}'")
                        return
                    else:
                        return command_entity['handler_func']()


    def _validate_command(self, command: Command):
        command_name: str = command.get_string_entity()
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
        return self.name


    def get_title(self) -> str:
        return self.title


    def get_router_info(self) -> dict:
        return {
            'title': self.title,
            'name': self.name,
            'ignore_command_register': self._ignore_command_register,
            'attributes': {
                'command_entities': self._command_entities,
            }

        }


    def get_all_commands(self) -> list[str]:
        all_commands: list[str] = []
        for command_entity in self._command_entities:
            all_commands.append(command_entity['command'].get_string_entity())

        return all_commands

    def get_all_flags(self) -> list[FlagsGroup]:
        all_flags: list[FlagsGroup] = []
        for command_entity in self._command_entities:
            all_flags.append(command_entity['command'].get_registered_flags())

        return all_flags
