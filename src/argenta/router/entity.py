__all__ = ["Router"]

from inspect import get_annotations, getfullargspec, getsourcefile, getsourcelines
from typing import Callable, TypeAlias

from rich.console import Console

from argenta.command import Command, InputCommand
from argenta.command.flag import ValidationStatus
from argenta.command.flag.flags import Flags, InputFlags
from argenta.response import Response, ResponseStatus
from argenta.router.command_handler.entity import CommandHandler, CommandHandlers
from argenta.router.exceptions import (
    RepeatedFlagNameException,
    RequiredArgumentNotPassedException,
    TriggerContainSpacesException,
)

HandlerFunc: TypeAlias = Callable[..., None]


class Router:
    def __init__(
        self,
        title: str = "Default title",
        *,
        disable_redirect_stdout: bool = False,
    ):
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
        self.title: str = title
        self.disable_redirect_stdout: bool = disable_redirect_stdout

        self.command_handlers: CommandHandlers = CommandHandlers()
        self.command_register_ignore: bool = False
        
        self.aliases: set[str] = set()
        self.triggers: set[str] = set()

    def command(self, command: Command | str) -> Callable[[HandlerFunc], HandlerFunc]:
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
    
        if overlapping := (self.aliases | self.triggers) & redefined_command.aliases:
            Console().print(f"\n[b red]WARNING:[/b red] Overlapping trigger or alias: [b blue]{overlapping}[/b blue]")
        
        self.aliases.update(redefined_command.aliases)
        self.triggers.add(redefined_command.trigger)

        def decorator(func: HandlerFunc) -> HandlerFunc:
            _validate_func_args(func)
            self.command_handlers.add_handler(CommandHandler(func, redefined_command))
            return func

        return decorator
        
    def _validate_command(self, command: Command) -> None:
        """
        Private. Validates the command registered in handler
        :param command: validated command
        :return: None if command is valid else raise exception
        """
        command_name: str = command.trigger
        if command_name.find(" ") != -1:
            raise TriggerContainSpacesException()
        flags: Flags = command.registered_flags
        flags_name: list[str] = [flag.string_entity.lower() for flag in flags]
        if len(set(flags_name)) < len(flags_name):
            raise RepeatedFlagNameException()

    def finds_appropriate_handler(self, input_command: InputCommand) -> None:
        """
        Private. Finds the appropriate handler for given input command and passes control to it
        :param input_command: input command as InputCommand
        :return: None
        """
        input_command_name: str = input_command.trigger
        input_command_flags: InputFlags = input_command.input_flags

        for command_handler in self.command_handlers:
            handle_command = command_handler.handled_command
            if input_command_name.lower() == handle_command.trigger.lower():
                self.process_input_command(input_command_flags, command_handler)
            if input_command_name.lower() in handle_command.aliases:
                self.process_input_command(input_command_flags, command_handler)

    def process_input_command(self, input_command_flags: InputFlags, command_handler: CommandHandler) -> None:
        """
        Private. Processes input command with the appropriate handler
        :param input_command_flags: input command flags as InputFlags
        :param command_handler: command handler for input command as CommandHandler
        :return: None
        """
        handle_command = command_handler.handled_command
        if handle_command.registered_flags.flags:
            if input_command_flags.flags:
                response: Response = _structuring_input_flags(handle_command, input_command_flags)
                command_handler.handling(response)
            else:
                response = Response(ResponseStatus.ALL_FLAGS_VALID)
                command_handler.handling(response)
        else:
            if input_command_flags.flags:
                undefined_flags = InputFlags()
                for input_flag in input_command_flags:
                    input_flag.status = ValidationStatus.UNDEFINED
                    undefined_flags.add_flag(input_flag)
                response = Response(ResponseStatus.UNDEFINED_FLAGS, input_flags=undefined_flags)
                command_handler.handling(response)
            else:
                response = Response(ResponseStatus.ALL_FLAGS_VALID)
                command_handler.handling(response)


def _structuring_input_flags(handled_command: Command, input_flags: InputFlags) -> Response:
    """
    Private. Validates flags of input command
    :param handled_command: entity of the handled command
    :param input_flags:
    :return: entity of response as Response
    """
    invalid_value_flags, undefined_flags = False, False

    for flag in input_flags:
        flag_status: ValidationStatus = handled_command.validate_input_flag(flag)
        flag.status = flag_status
        if flag_status == ValidationStatus.INVALID:
            invalid_value_flags = True
        elif flag_status == ValidationStatus.UNDEFINED:
            undefined_flags = True

    status = ResponseStatus.from_flags(
        has_invalid_value_flags=invalid_value_flags, has_undefined_flags=undefined_flags
    )

    return Response(status=status, input_flags=input_flags)


def _validate_func_args(func: Callable[..., None]) -> None:
    """
    Private. Validates the arguments of the handler
    :param func: entity of the handler func
    :return: None if func is valid else raise exception
    """
    transferred_args = getfullargspec(func).args
    if len(transferred_args) == 0:
        raise RequiredArgumentNotPassedException()

    response_arg: str = transferred_args[0]
    func_annotations: dict[str, None] = get_annotations(func)

    response_arg_annotation = func_annotations.get(response_arg)

    if response_arg_annotation is not None:
        if response_arg_annotation is not Response:
            source_line: int = getsourcelines(func)[1]
            Console().print(
                f'\nFile "{getsourcefile(func)}", line {source_line}\n[b red]WARNING:[/b red] [i]The typehint '
                + f"of argument([green]{response_arg}[/green]) passed to the handler must be [/i][bold blue]{Response}[/bold blue],"
                + f" [i]but[/i] [bold blue]{response_arg_annotation}[/bold blue] [i]is specified[/i]",
                highlight=False,
            )
    