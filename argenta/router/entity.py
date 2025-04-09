from typing import Callable, Any
from inspect import getfullargspec

from argenta.command import Command
from argenta.command.models import InputCommand
from argenta.router.command_handlers.entity import CommandHandlers
from argenta.router.command_handler.entity import CommandHandler
from argenta.command.flag.models import Flag, Flags, InputFlags
from argenta.router.exceptions import (RepeatedFlagNameException,
                                       TooManyTransferredArgsException,
                                       RequiredArgumentNotPassedException,
                                       IncorrectNumberOfHandlerArgsException,
                                       TriggerCannotContainSpacesException)


class Router:
    def __init__(self,
                 title: str = 'Commands group title:',
                 name: str = 'Default'):
        self._title = title
        self._name = name

        self._command_handlers: CommandHandlers = CommandHandlers()
        self._ignore_command_register: bool = False
        self._not_valid_flag_handler: Callable[[Flag], None] = lambda flag: print(f"Undefined or incorrect input flag: {flag.get_string_entity()}{(' '+flag.get_value()) if flag.get_value() else ''}")


    def command(self, command: Command) -> Callable[[Any],  Any]:
        self._validate_command(command)

        def command_decorator(func):
            Router._validate_func_args(command, func)
            self._command_handlers.add_command_handler(CommandHandler(func, command))

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


    def input_command_handler(self, input_command: InputCommand):
        input_command_name: str = input_command.get_trigger()
        input_command_flags: InputFlags = input_command.get_input_flags()

        for command_handler in self._command_handlers:
            handle_command = command_handler.get_handled_command()
            if input_command_name.lower() == handle_command.get_trigger().lower():
                if handle_command.get_registered_flags().get_flags():
                    if input_command_flags.get_flags():
                        if self._validate_input_flags(handle_command, input_command_flags):
                            command_handler.handling(input_command_flags)
                            return
                    else:
                        command_handler.handling(input_command_flags)
                        return
                else:
                    if input_command_flags.get_flags():
                        self._not_valid_flag_handler(input_command_flags[0])
                        return
                    else:
                        command_handler.handling()
                        return


    def _validate_input_flags(self, handle_command: Command, input_flags: InputFlags):
        for flag in input_flags:
            is_valid = handle_command.validate_input_flag(flag)
            if not is_valid:
                self._not_valid_flag_handler(flag)
                return False
        return True


    @staticmethod
    def _validate_command(command: Command):
        command_name: str = command.get_trigger()
        if command_name.find(' ') != -1:
            raise TriggerCannotContainSpacesException()

        flags: Flags = command.get_registered_flags()
        if flags:
            flags_name: list = [x.get_string_entity().lower() for x in flags]
            if len(set(flags_name)) < len(flags_name):
                raise RepeatedFlagNameException()


    @staticmethod
    def _validate_func_args(command: Command, func: Callable):
        registered_args = command.get_registered_flags()
        transferred_args = getfullargspec(func).args
        if registered_args.get_flags() and transferred_args:
           if len(transferred_args) != 1:
                raise TooManyTransferredArgsException()
        elif registered_args.get_flags() and not transferred_args:
            raise RequiredArgumentNotPassedException()
        elif not registered_args.get_flags() and transferred_args:
            raise TooManyTransferredArgsException()


    def set_ignore_command_register(self, ignore_command_register: bool):
        self._ignore_command_register = ignore_command_register


    def get_triggers(self):
        all_triggers: list[str] = []
        for command_handler in self._command_handlers:
            all_triggers.append(command_handler.get_handled_command().get_trigger())
        return all_triggers


    def get_command_handlers(self) -> CommandHandlers:
        return self._command_handlers


    def get_name(self) -> str:
        return self._name


    def get_title(self) -> str:
        return self._title


    def set_title(self, title: str):
        self._title = title
