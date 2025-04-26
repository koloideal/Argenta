from typing import Callable
from inspect import getfullargspec
from argenta.command import Command
from argenta.command.models import InputCommand
from argenta.router.command_handler.entity import CommandHandlers, CommandHandler
from argenta.command.flag.models import Flag, Flags, InputFlags
from argenta.router.exceptions import (RepeatedFlagNameException,
                                       TooManyTransferredArgsException,
                                       RequiredArgumentNotPassedException,
                                       TriggerContainSpacesException)


class Router:
    def __init__(self,
                 title: str = None):
        """
        Public. Directly configures and manages handlers
        :param title: the title of the router, displayed when displaying the available commands
        :return: None
        """
        self._title = title

        self._command_handlers: CommandHandlers = CommandHandlers()
        self._ignore_command_register: bool = False
        self._not_valid_flag_handler: Callable[[Flag], None] = lambda flag: print(f"Undefined or incorrect input flag: {flag.get_string_entity()}{(' '+flag.get_value()) if flag.get_value() else ''}")


    def command(self, command: Command) -> Callable:
        """
        Public. Registers handler
        :param command: Registered command
        :return: decorated handler as Callable[[Any], Any]
        """
        self._validate_command(command)

        def command_decorator(func):
            Router._validate_func_args(command, func)
            self._command_handlers.add_command_handler(CommandHandler(func, command))

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        return command_decorator


    def set_invalid_input_flag_handler(self, func: Callable[[Flag], None]) -> None:
        """
        Public. Registers handler for invalid input flag
        :param func: registered handler
        :return: None
        """
        self._not_valid_flag_handler = func


    def finds_appropriate_handler(self, input_command: InputCommand) -> None:
        """
        Private. Finds the appropriate handler for given input command and passes control to it
        :param input_command: input command as InputCommand
        :return: None
        """
        input_command_name: str = input_command.get_trigger()
        input_command_flags: InputFlags = input_command.get_input_flags()

        for command_handler in self._command_handlers:
            handle_command = command_handler.get_handled_command()
            if input_command_name.lower() == handle_command.get_trigger().lower():
                self.process_input_command(input_command_flags, command_handler)
            if input_command_name.lower() in handle_command.get_aliases():
                self.process_input_command(input_command_flags, command_handler)


    def process_input_command(self, input_command_flags: InputFlags, command_handler: CommandHandler) -> None:
        """
        Private. Processes input command with the appropriate handler
        :param input_command_flags: input command flags as InputFlags
        :param command_handler: command handler for input command as CommandHandler
        :return: None
        """
        handle_command = command_handler.get_handled_command()
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


    def _validate_input_flags(self, handled_command: Command, input_flags: InputFlags) -> bool:
        """
        Private. Validates flags of input command
        :param handled_command: entity of the handled command
        :param input_flags:
        :return: is flags of input command valid as bool
        """
        for flag in input_flags:
            is_valid: bool = handled_command.validate_input_flag(flag)
            if not is_valid:
                self._not_valid_flag_handler(flag)
                return False
        return True


    @staticmethod
    def _validate_command(command: Command) -> None:
        """
        Private. Validates the command registered in handler
        :param command: validated command
        :return: None if command is valid else raise exception
        """
        command_name: str = command.get_trigger()
        if command_name.find(' ') != -1:
            raise TriggerContainSpacesException()

        flags: Flags = command.get_registered_flags()
        if flags:
            flags_name: list = [x.get_string_entity().lower() for x in flags]
            if len(set(flags_name)) < len(flags_name):
                raise RepeatedFlagNameException()


    @staticmethod
    def _validate_func_args(command: Command, func: Callable) -> None:
        """
        Private. Validates the arguments of the handler
        :param command: registered command in handler
        :param func: entity of the handler func
        :return: None if func is valid else raise exception
        """
        registered_args = command.get_registered_flags()
        transferred_args = getfullargspec(func).args
        if registered_args.get_flags() and transferred_args:
           if len(transferred_args) != 1:
                raise TooManyTransferredArgsException()
        elif registered_args.get_flags() and not transferred_args:
            raise RequiredArgumentNotPassedException()
        elif not registered_args.get_flags() and transferred_args:
            raise TooManyTransferredArgsException()


    def set_command_register_ignore(self, _: bool) -> None:
        """
        Private. Sets the router behavior on the input commands register
        :param _: is command register ignore
        :return: None
        """
        self._ignore_command_register = _


    def get_triggers(self) -> list[str]:
        """
        Public. Gets registered triggers
        :return: registered in router triggers as list[str]
        """
        all_triggers: list[str] = []
        for command_handler in self._command_handlers:
            all_triggers.append(command_handler.get_handled_command().get_trigger())
        return all_triggers


    def get_aliases(self) -> list[str]:
        """
        Public. Gets registered aliases
        :return: registered in router aliases as list[str]
        """
        all_aliases: list[str] = []
        for command_handler in self._command_handlers:
            if command_handler.get_handled_command().get_aliases():
                all_aliases.extend(command_handler.get_handled_command().get_aliases())
        return all_aliases


    def get_command_handlers(self) -> CommandHandlers:
        """
        Private. Gets registered command handlers
        :return: registered command handlers as CommandHandlers
        """
        return self._command_handlers


    def get_title(self) -> str | None:
        """
        Public. Gets title of the router
        :return: the title of the router as str or None
        """
        return self._title


    def set_title(self, title: str) -> None:
        """
        Public. Sets the title of the router
        :param title: title that will be setted
        :return: None
        """
        self._title = title
