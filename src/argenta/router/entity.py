from typing import Callable, Literal
from inspect import getfullargspec
from argenta.command import Command
from argenta.command.models import InputCommand
from argenta.response import Response, Status
from argenta.router.command_handler.entity import CommandHandlers, CommandHandler
from argenta.command.flag.models import Flag
from argenta.command.flags.models import Flags, InputFlags, UndefinedInputFlags, ValidInputFlags, InvalidValueInputFlags
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


    def command(self, command: Command) -> Callable:
        """
        Public. Registers handler
        :param command: Registered command
        :return: decorated handler as Callable[[Any], Any]
        """
        self._validate_command(command)

        def command_decorator(func):
            Router._validate_func_args(command, func)
            self._command_handlers.add_handler(CommandHandler(func, command))

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        return command_decorator


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
        response: Response = Response()
        if handle_command.get_registered_flags().get_flags():
            if input_command_flags.get_flags():
                response.status = Status.SUCCESSFUL
                flags = self._validate_input_flags(handle_command, input_command_flags)
                response.valid_flags, response.undefined_flags, response.invalid_flags = flags
                command_handler.handling(response)
                return
            else:
                response.status = Status.SUCCESSFUL
                command_handler.handling(response)
                return
        else:
            if input_command_flags.get_flags():
                response.status = Status.UNSUCCESSFUL
                response.undefined_flags = UndefinedInputFlags(*input_command_flags)
                command_handler.handling(response)
                return
            else:
                response.status = Status.SUCCESSFUL
                command_handler.handling(response)
                return


    @staticmethod
    def _validate_input_flags(handled_command: Command, input_flags: InputFlags) -> (ValidInputFlags,
                                                                                     UndefinedInputFlags,
                                                                                     InvalidValueInputFlags):
        """
        Private. Validates flags of input command
        :param handled_command: entity of the handled command
        :param input_flags:
        :return: is flags of input command valid as bool
        """
        valid_input_flags: ValidInputFlags = ValidInputFlags()
        invalid_value_input_flags: InvalidValueInputFlags = InvalidValueInputFlags()
        undefined_input_flags: UndefinedInputFlags = UndefinedInputFlags()
        for flag in input_flags:
            flag_status: Literal['Undefined', 'Valid', 'Invalid'] = handled_command.validate_input_flag(flag)
            match flag_status:
                case 'Valid':
                    valid_input_flags.add_flag(flag)
                case 'Undefined':
                    undefined_input_flags.add_flag(flag)
                case 'Invalid':
                    invalid_value_input_flags.add_flag(flag)
        return valid_input_flags, undefined_input_flags, invalid_value_input_flags


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
        transferred_args = getfullargspec(func).args
        if len(transferred_args) > 1:
            raise TooManyTransferredArgsException()
        elif len(transferred_args) == 0:
            raise RequiredArgumentNotPassedException()


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
