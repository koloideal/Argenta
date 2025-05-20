from typing import Callable, Literal, Type
from inspect import getfullargspec, get_annotations, getsourcefile, getsourcelines
from rich.console import Console

from argenta.command import Command
from argenta.command.models import InputCommand
from argenta.response import Response, Status
from argenta.router.command_handler.entity import CommandHandlers, CommandHandler
from argenta.command.flag.flags import (
    Flags,
    InputFlags,
    UndefinedInputFlags,
    ValidInputFlags,
    InvalidValueInputFlags,
)
from argenta.router.exceptions import (
    RepeatedFlagNameException,
    TooManyTransferredArgsException,
    RequiredArgumentNotPassedException,
    TriggerContainSpacesException,
)


class Router:
    def __init__(self, title: str | None = "Awesome title", disable_redirect_stdout: bool = False):
        """
        Public. Directly configures and manages handlers
        :param title: the title of the router, displayed when displaying the available commands
        :param disable_redirect_stdout: Disables stdout forwarding, if the argument value is True,
               the StaticDividingLine will be forced to be used as a line separator for this router,
               disabled forwarding is needed when there is text output in conjunction with a text input request (for example, input()),
               if the argument value is True, the output of the input() prompt is intercepted and not displayed,
               which is ambiguous behavior and can lead to unexpected work
        :return: None
        """
        self.title = title
        self.disable_redirect_stdout = disable_redirect_stdout

        self._command_handlers: CommandHandlers = CommandHandlers()
        self._ignore_command_register: bool = False

    def command(self, command: Command | str) -> Callable:
        """
        Public. Registers handler
        :param command: Registered command
        :return: decorated handler as Callable
        """
        if isinstance(command, str):
            redefined_command = Command(command)
        else:
            redefined_command = command
        self._validate_command(redefined_command)

        def command_decorator(func):
            Router._validate_func_args(func)
            self._command_handlers.add_handler(CommandHandler(func, redefined_command))

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

    def process_input_command(
        self, input_command_flags: InputFlags, command_handler: CommandHandler
    ) -> None:
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
                response: Response = self._structuring_input_flags(
                    handle_command, input_command_flags
                )
                command_handler.handling(response)
            else:
                response.status = Status.ALL_FLAGS_VALID
                command_handler.handling(response)
        else:
            if input_command_flags.get_flags():
                response.status = Status.UNDEFINED_FLAGS
                response.undefined_flags = UndefinedInputFlags()
                response.undefined_flags.add_flags(input_command_flags.get_flags())
                command_handler.handling(response)
            else:
                response.status = Status.ALL_FLAGS_VALID
                command_handler.handling(response)

    @staticmethod
    def _structuring_input_flags(
        handled_command: Command, input_flags: InputFlags
    ) -> Response:
        """
        Private. Validates flags of input command
        :param handled_command: entity of the handled command
        :param input_flags:
        :return: entity of response as Response
        """
        valid_input_flags: ValidInputFlags = ValidInputFlags()
        invalid_value_input_flags: InvalidValueInputFlags = InvalidValueInputFlags()
        undefined_input_flags: UndefinedInputFlags = UndefinedInputFlags()
        for flag in input_flags:
            flag_status: Literal["Undefined", "Valid", "Invalid"] = (
                handled_command.validate_input_flag(flag)
            )
            if flag_status == "Valid":
                valid_input_flags.add_flag(flag)
            elif flag_status == "Undefined":
                undefined_input_flags.add_flag(flag)
            elif flag_status == "Invalid":
                invalid_value_input_flags.add_flag(flag)

        if (
            not invalid_value_input_flags.get_flags()
            and not undefined_input_flags.get_flags()
        ):
            status = Status.ALL_FLAGS_VALID
        elif (
            invalid_value_input_flags.get_flags()
            and not undefined_input_flags.get_flags()
        ):
            status = Status.INVALID_VALUE_FLAGS
        elif (
            not invalid_value_input_flags.get_flags()
            and undefined_input_flags.get_flags()
        ):
            status = Status.UNDEFINED_FLAGS
        else:
            status = Status.UNDEFINED_AND_INVALID_FLAGS

        return Response(
            invalid_value_flags=invalid_value_input_flags,
            valid_flags=valid_input_flags,
            status=status,
            undefined_flags=undefined_input_flags,
        )

    @staticmethod
    def _validate_command(command: Command | str) -> None:
        """
        Private. Validates the command registered in handler
        :param command: validated command
        :return: None if command is valid else raise exception
        """
        command_name: str = command.get_trigger()
        if command_name.find(" ") != -1:
            raise TriggerContainSpacesException()
        flags: Flags = command.get_registered_flags()
        if flags:
            flags_name: list = [x.get_string_entity().lower() for x in flags]
            if len(set(flags_name)) < len(flags_name):
                raise RepeatedFlagNameException()

    @staticmethod
    def _validate_func_args(func: Callable) -> None:
        """
        Private. Validates the arguments of the handler
        :param func: entity of the handler func
        :return: None if func is valid else raise exception
        """
        transferred_args = getfullargspec(func).args
        if len(transferred_args) > 1:
            raise TooManyTransferredArgsException()
        elif len(transferred_args) == 0:
            raise RequiredArgumentNotPassedException()

        transferred_arg: str = transferred_args[0]
        func_annotations: dict[str, Type] = get_annotations(func)

        if arg_annotation := func_annotations.get(transferred_arg):
            if arg_annotation is Response:
                pass
            else:
                file_path: str | None = getsourcefile(func)
                source_line: int = getsourcelines(func)[1]
                fprint = Console().print
                fprint(f'\nFile "{file_path}", line {source_line}\n[b red]WARNING:[/b red] [i]The typehint '
                    f"of argument([green]{transferred_arg}[/green]) passed to the handler is [/i][bold blue]{Response}[/bold blue],"
                    f" [i]but[/i] [bold blue]{arg_annotation}[/bold blue] [i]is specified[/i]",
                    highlight=False)

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
