import warnings
from collections import Counter
from collections.abc import Callable, Iterable
from inspect import get_annotations, getfullargspec

from argenta.app.protocols import HandlerFunc
from argenta.command import Command, InputCommand, InputFlags
from argenta.command.flag import ValidationStatus
from argenta.response import Response, ResponseStatus
from argenta.router.command_handler.entity import CommandHandler, CommandHandlers
from argenta.router.exceptions import (
    RepeatedAliasNameException,
    RepeatedFlagNameException,
    RepeatedTriggerNameException,
    RequiredArgumentNotPassedException,
    TriggerContainSpacesException,
)


def _ensure_unique_command_name(lowered_name: str, triggers: set[str], aliases: set[str]) -> None:
    if lowered_name in triggers:
        raise RepeatedTriggerNameException({lowered_name})
    if lowered_name in aliases:
        raise RepeatedAliasNameException({lowered_name})


def _ensure_unique_aliases(
    lowered_aliases: Iterable[str], triggers: set[str], aliases: set[str]
) -> None:
    overlapping_aliases = {
        alias for alias in lowered_aliases if alias in triggers or alias in aliases
    }
    if overlapping_aliases:
        raise RepeatedAliasNameException(overlapping_aliases)


def _ensure_unique_flag_names(command: Command) -> None:
    flag_counts = Counter(flag.string_entity.lower() for flag in command.registered_flags)
    repeated_flags = {name for name, count in flag_counts.items() if count > 1}
    if repeated_flags:
        raise RepeatedFlagNameException(repeated_flags, command.trigger)


class Router:
    def __init__(
        self,
        title: str = "Title",
        *,
        disable_redirect_stdout: bool = False,
    ):
        """
        Public. Directly configures and manages handlers
        :param title: the title of the router, displayed when displaying the available commands
        :param disable_redirect_stdout: Disables stdout forwarding, if the argument value is True,
               the REPL frames this router's output with a static dividing line
               (a dynamic line cannot be sized without capturing the output),
               disabled forwarding is needed when there is text output in conjunction
               with a text input request (for example, input()),
               if the argument value is True, the output of the input() prompt is intercepted
               and not displayed, which is ambiguous behavior and can lead to unexpected work
        :return: None
        """
        self.title: str = title
        self.is_redirect_stdout_disabled: bool = disable_redirect_stdout

        self.command_handlers: CommandHandlers = CommandHandlers()
        self.aliases: set[str] = set()
        self.triggers: set[str] = set()

    def command(self, command: Command | str) -> Callable[[HandlerFunc], HandlerFunc]:
        """
        Public. Registers handler
        :param command: Registered command
        :return: decorated handler as Callable
        """
        redefined_command = Command(command) if isinstance(command, str) else command

        lowered_trigger, lowered_aliases = self._validate_command(redefined_command)
        self.aliases.update(lowered_aliases)
        self.triggers.add(lowered_trigger)

        def decorator(func: HandlerFunc) -> HandlerFunc:
            _validate_func_args(func)
            self.command_handlers.add_handler(
                CommandHandler(func, redefined_command), lowered_trigger, lowered_aliases
            )
            return func

        return decorator

    def finds_appropriate_handler(self, input_command: InputCommand) -> None:
        """
        Private. Finds the appropriate handler for given input command and passes control to it
        :param input_command: input command as InputCommand
        :return: None
        """
        input_command_name: str = input_command.trigger.lower()
        input_command_flags: InputFlags = input_command.input_flags

        command_handler = self.command_handlers.get_command_handler_by_trigger(input_command_name)

        if command_handler:
            self.process_input_command(input_command_flags, command_handler)
        else:
            raise RuntimeError(f"Handler for '{input_command.trigger}' command not found. Panic!")

    def process_input_command(
        self, input_command_flags: InputFlags, command_handler: CommandHandler
    ) -> None:
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

    def _validate_command(self, command: Command) -> tuple[str, set[str]]:
        """
        Private. Validates the command registered in handler
        :param command: validated command
        :return: normalized trigger and aliases if command is valid else raise exception
        """
        if any(char.isspace() for char in command.trigger):
            raise TriggerContainSpacesException()

        lowered_trigger = command.trigger.lower()
        lowered_aliases = {alias.lower() for alias in command.aliases}
        _ensure_unique_command_name(lowered_trigger, self.triggers, self.aliases)
        _ensure_unique_aliases(lowered_aliases, self.triggers, self.aliases)
        _ensure_unique_flag_names(command)
        return lowered_trigger, lowered_aliases


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


def _validate_func_args(func: HandlerFunc) -> None:
    """
    Private. Validates the arguments of the handler
    :param func: entity of the handler func
    :return: None if func is valid else raise exception
    """
    func_code = getattr(func, "__code__", None)
    if func_code is None:
        transferred_args = getfullargspec(func).args
        if len(transferred_args) == 0:
            raise RequiredArgumentNotPassedException()
        response_arg: str = transferred_args[0]
        func_annotations: dict[str, object] = get_annotations(func)
    else:
        if func_code.co_argcount == 0:
            raise RequiredArgumentNotPassedException()
        response_arg = func_code.co_varnames[0]
        func_annotations = getattr(func, "__annotations__", {})

    response_arg_annotation = func_annotations.get(response_arg)

    if response_arg_annotation is not None and response_arg_annotation is not Response:
        warnings.warn(
            f"The type hint of argument '{response_arg}' of handler "
            f"'{func.__qualname__}' must be {Response}, "
            f"but {response_arg_annotation} is specified",
            UserWarning,
            stacklevel=3,
        )
