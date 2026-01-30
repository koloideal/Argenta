__all__ = ["App"]

import io
import re
from contextlib import redirect_stdout
from typing import Callable, Never, TypeAlias

from rich.console import Console

from argenta.app.autocompleter import AutoCompleter
from argenta.app.behavior_handlers.entity import BehaviorHandlersFabric
from argenta.app.presentation.renderers import PlainRenderer, RichRenderer, Renderer
from argenta.app.dividing_line.models import DynamicDividingLine, StaticDividingLine
from argenta.app.presentation.viewers import Viewer
from argenta.app.protocols import (
    DescriptionMessageGenerator,
    EmptyCommandHandler,
    NonStandardBehaviorHandler,
    Printer,
)
from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.command.exceptions import (
    InputCommandException,
    RepeatedInputFlagsException,
    UnprocessedInputFlagException,
)
from argenta.router.exceptions import RepeatedAliasNameException, RepeatedTriggerNameException
from argenta.command.models import Command, InputCommand
from argenta.response import Response
from argenta.router import Router


Matches: TypeAlias = list[str] | list[Never]
_ANSI_ESCAPE_RE: re.Pattern[str] = re.compile(r"\u001b\[[0-9;]*m")


class BaseApp:
    def __init__(
        self,
        *,
        prompt: str,
        initial_message: str,
        farewell_message: str,
        exit_command: Command,
        system_router_title: str,
        dividing_line: StaticDividingLine | DynamicDividingLine | None,
        repeat_command_groups_printing: bool,
        override_system_messages: bool,
        autocompleter: AutoCompleter,
        print_func: Printer,
    ) -> None:
        self._prompt: str = prompt
        self._print_func: Printer = print_func
        self._exit_command: Command = exit_command
        self._dividing_line: StaticDividingLine | DynamicDividingLine | None = dividing_line
        self._repeat_command_groups_printing: bool = repeat_command_groups_printing
        self._override_system_messages: bool = override_system_messages
        self._autocompleter: AutoCompleter = autocompleter
        self._system_router: Router = Router(title=system_router_title)

        self._stdout_buffer: io.StringIO = io.StringIO()
        self.registered_routers: RegisteredRouters = RegisteredRouters()
        self._messages_on_startup: list[str] = []

        if self._override_system_messages:
            self._renderer: Renderer = PlainRenderer()
        else:
            self._renderer: Renderer = RichRenderer()

        self._viewer: Viewer = Viewer(self._print_func, self._renderer)
        self._handlers_fabric: BehaviorHandlersFabric = BehaviorHandlersFabric(
            self._print_func,
            self._renderer,
            self._most_similar_command
        )

        self._initial_message: str = self._renderer.render_initial_message(initial_message)
        self._farewell_message: str = self._renderer.render_farewell_message(farewell_message)
        self._description_message_generator: DescriptionMessageGenerator = self._handlers_fabric.generate_description_message_generator()
        self._incorrect_input_syntax_handler: NonStandardBehaviorHandler[str] = self._handlers_fabric.generate_incorrect_input_syntax_handler()
        self._repeated_input_flags_handler: NonStandardBehaviorHandler[str] = self._handlers_fabric.generate_repeated_input_flags_handler()
        self._empty_input_command_handler: EmptyCommandHandler = self._handlers_fabric.generate_empty_input_command_handler()
        self._unknown_command_handler: NonStandardBehaviorHandler[InputCommand] = self._handlers_fabric.generate_unknown_command_handler()
        self._exit_command_handler: NonStandardBehaviorHandler[Response] = self._handlers_fabric.generate_exit_command_handler(self._farewell_message)

    def set_description_message_pattern(self, _: DescriptionMessageGenerator, /) -> None:
        """
        Public. Sets the output pattern of the available commands
        :param _: output pattern of the available commands
        :return: None
        """
        self._description_message_generator = _

    def set_incorrect_input_syntax_handler(self, _: NonStandardBehaviorHandler[str], /) -> None:
        """
        Public. Sets the handler for incorrect flags when entering a command
        :param _: handler for incorrect flags when entering a command
        :return: None
        """
        self._incorrect_input_syntax_handler = _

    def set_repeated_input_flags_handler(self, _: NonStandardBehaviorHandler[str], /) -> None:
        """
        Public. Sets the handler for repeated flags when entering a command
        :param _: handler for repeated flags when entering a command
        :return: None
        """
        self._repeated_input_flags_handler = _

    def set_unknown_command_handler(self, _: NonStandardBehaviorHandler[InputCommand], /) -> None:
        """
        Public. Sets the handler for unknown commands when entering a command
        :param _: handler for unknown commands when entering a command
        :return: None
        """
        self._unknown_command_handler = _

    def set_empty_command_handler(self, _: EmptyCommandHandler, /) -> None:
        """
        Public. Sets the handler for empty commands when entering a command
        :param _: handler for empty commands when entering a command
        :return: None
        """
        self._empty_input_command_handler = _

    def set_exit_command_handler(self, _: NonStandardBehaviorHandler[Response], /) -> None:
        """
        Public. Sets the handler for exit command when entering a command
        :param _: handler for exit command when entering a command
        :return: None
        """
        self._exit_command_handler = _

    def _print_static_framed_text(self, text: str) -> None:
        """
        Private. Outputs text by framing it in a static or dynamic split strip
        :param text: framed text
        :return: None
        """
        match self._dividing_line:
            case StaticDividingLine() as dividing_line:
                self._print_func(dividing_line.get_full_static_line(is_override=self._override_system_messages))
                print(text.strip("\n"))
                self._print_func(dividing_line.get_full_static_line(is_override=self._override_system_messages))
            case DynamicDividingLine() as dividing_line:
                self._print_func(
                    StaticDividingLine(dividing_line.get_unit_part()).get_full_static_line(
                        is_override=self._override_system_messages
                    )
                )
                print(text.strip("\n"))
                self._print_func(
                    StaticDividingLine(dividing_line.get_unit_part()).get_full_static_line(
                        is_override=self._override_system_messages
                    )
                )
            case None:
                print("\n" + text.strip("\n") + "\n")
            case _:
                raise NotImplementedError(f"Dividing line with type {self._dividing_line} is not implemented")

    def _is_exit_command(self, command: InputCommand) -> bool:
        """
        Private. Checks if the given command is an exit command
        :param command: command to check
        :return: is it an exit command or not as bool
        """
        trigger = command.trigger
        exit_trigger = self._exit_command.trigger
        if trigger.lower() == exit_trigger.lower():
            return True
        elif trigger.lower() in [x.lower() for x in self._exit_command.aliases]:
            return True
        return False

    def _is_unknown_command(self, input_command: InputCommand) -> bool:
        if not self.registered_routers.get_router_by_trigger(input_command.trigger.lower()):
            return True
        return False

    def _capture_stdout(self, func: Callable[[], None]) -> str:
        """
        Private. Captures stdout from a function call using a reusable buffer
        :param func: function to execute with captured stdout
        :return: captured stdout as string
        """
        self._stdout_buffer.seek(0)
        self._stdout_buffer.truncate(0)
        with redirect_stdout(self._stdout_buffer):
            func()
        return self._stdout_buffer.getvalue()

    def _error_handler(self, error: InputCommandException, raw_command: str) -> None:
        """
        Private. Handles parsing errors of the entered command
        :param error: error being handled
        :param raw_command: the raw input command
        :return: None
        """
        if isinstance(error, UnprocessedInputFlagException):
            self._incorrect_input_syntax_handler(raw_command)
        elif isinstance(error, RepeatedInputFlagsException):
            self._repeated_input_flags_handler(raw_command)
        else:
            self._empty_input_command_handler()

    def _setup_system_router(self) -> None:
        """
        Private. Sets up system router
        :return: None
        """
        @self._system_router.command(self._exit_command)
        def _(response: Response) -> None:
            self._exit_command_handler(response)

        self.registered_routers.add_registered_router(self._system_router)

    def _validate_routers_for_collisions(self) -> None:
        """
        Private. Validates that there are no trigger/alias collisions between routers
        :return: None
        :raises: RepeatedTriggerNameException or RepeatedAliasNameException if collision detected
        """

        all_triggers: set[str] = set()
        all_aliases: set[str] = set()

        for router_entity in self.registered_routers:
            union_units: set[str] = all_triggers | all_aliases
            trigger_collisions: set[str] = union_units & router_entity.triggers
            if trigger_collisions:
                raise RepeatedTriggerNameException()

            alias_collisions: set[str] = union_units & router_entity.aliases
            if alias_collisions:
                raise RepeatedAliasNameException(alias_collisions)

            all_triggers.update(router_entity.triggers)
            all_aliases.update(router_entity.aliases)

    def _most_similar_command(self, unknown_command: str) -> str | None:
        all_commands = self.registered_routers.get_triggers()

        matches_startswith_unknown_command: Matches = sorted(
            cmd for cmd in all_commands if cmd.startswith(unknown_command)
        )
        matches_startswith_cmd: Matches = sorted(cmd for cmd in all_commands if unknown_command.startswith(cmd))

        matches: Matches = matches_startswith_unknown_command or matches_startswith_cmd

        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            return sorted(matches, key=lambda cmd: len(cmd))[0]
        else:
            return None

    def _pre_cycle_setup(self) -> None:
        """
        Private. Configures various aspects of the application before the start of the cycle
        :return: None
        """
        self._setup_system_router()
        self._validate_routers_for_collisions()
        self._autocompleter.initial_setup(self.registered_routers.get_triggers())

        if self._messages_on_startup:
            self._viewer.view_messages_on_startup(self._messages_on_startup)

        if not self._repeat_command_groups_printing:
            self._viewer.view_command_groups_description(self._description_message_generator, self.registered_routers)

    def _process_exist_and_valid_command(self, input_command: InputCommand) -> None:
        processing_router = self.registered_routers.get_router_by_trigger(input_command.trigger.lower())

        if not processing_router:
            raise RuntimeError(f"Router for '{input_command.trigger}' not found. Panic!")

        match (self._dividing_line, processing_router.disable_redirect_stdout):
            case (None, bool()):
                processing_router.finds_appropriate_handler(input_command)
            case (DynamicDividingLine(), False):
                stdout_result = self._capture_stdout(lambda: processing_router.finds_appropriate_handler(input_command))
                clear_text = _ANSI_ESCAPE_RE.sub("", stdout_result)
                max_length_line = max([len(line) for line in clear_text.split("\n")])
                max_length_line = (
                    max_length_line if 10 <= max_length_line <= 100 else 100 if max_length_line > 100 else 10
                )

                self._print_func(
                    self._dividing_line.get_full_dynamic_line(
                        length=max_length_line, is_override=self._override_system_messages
                    )
                )
                print(clear_text.strip("\n"))
                self._print_func(
                    self._dividing_line.get_full_dynamic_line(
                        length=max_length_line, is_override=self._override_system_messages
                    )
                )
            case (StaticDividingLine() as dividing_line, bool()) | (DynamicDividingLine() as dividing_line, True):
                self._print_func(
                    StaticDividingLine(dividing_line.get_unit_part()).get_full_static_line(
                        is_override=self._override_system_messages
                    )
                )
                processing_router.finds_appropriate_handler(input_command)
                self._print_func(
                    StaticDividingLine(dividing_line.get_unit_part()).get_full_static_line(
                        is_override=self._override_system_messages
                    )
                )
            case _:
                raise NotImplementedError(f"Dividing line with type {self._dividing_line} is not implemented")


AVAILABLE_DIVIDING_LINES: TypeAlias = StaticDividingLine | DynamicDividingLine
DEFAULT_PRINT_FUNC: Printer = Console().print
DEFAULT_EXIT_COMMAND: Command = Command("q", description="Exit command")


class App(BaseApp):
    def __init__(
        self,
        *,
        prompt: str = ">>> ",
        initial_message: str = "Argenta",
        farewell_message: str = "See you",
        exit_command: Command = DEFAULT_EXIT_COMMAND,
        system_router_title: str = "System points:",
        dividing_line: AVAILABLE_DIVIDING_LINES | None = None,
        repeat_command_groups_printing: bool = False,
        override_system_messages: bool = False,
        autocompleter: AutoCompleter | None = None,
        print_func: Printer = DEFAULT_PRINT_FUNC,
    ) -> None:
        """
        Public. The essence of the application itself.
        Configures and manages all aspects of the behavior and presentation of the user interacting with the user
        :param prompt: displayed before entering the command
        :param initial_message: displayed at the start of the app
        :param farewell_message: displayed at the end of the app
        :param exit_command: the entity of the command that will be terminated when entered
        :param system_router_title: system router title
        :param dividing_line: the entity of the dividing line
        :param repeat_command_groups_printing: whether to repeat the available commands and their description
        :param override_system_messages: whether to redefine the default formatting of system messages
        :param autocompleter: the entity of the autocompleter
        :param print_func: system messages text output function
        :return: None
        """
        super().__init__(
            prompt=prompt,
            initial_message=initial_message,
            farewell_message=farewell_message,
            exit_command=exit_command,
            system_router_title=system_router_title,
            dividing_line=dividing_line,
            repeat_command_groups_printing=repeat_command_groups_printing,
            override_system_messages=override_system_messages,
            autocompleter=autocompleter or AutoCompleter(),
            print_func=print_func,
        )

    def run_polling(self) -> None:
        """
        Private. Starts the user input processing cycle
        :return: None
        """
        self._print_func(self._initial_message)
        self._pre_cycle_setup()
        while True:
            if self._repeat_command_groups_printing:
                self._viewer.view_command_groups_description(self._description_message_generator, self.registered_routers)

            print()  # pre-prompt gap
            raw_command: str = self._autocompleter.prompt(self._renderer.render_prompt(self._prompt))
            print()  # post-prompt gap

            try:
                input_command: InputCommand = InputCommand.parse(raw_command=raw_command)
            except InputCommandException as error:  # noqa F841
                stderr_result = self._capture_stdout(
                    lambda: self._error_handler(error, raw_command)  # noqa F821
                )
                self._print_static_framed_text(stderr_result)
                continue

            if self._is_exit_command(input_command):
                self._system_router.finds_appropriate_handler(input_command)
                return

            if self._is_unknown_command(input_command):
                stdout_res = self._capture_stdout(lambda: self._unknown_command_handler(input_command))
                self._print_static_framed_text(stdout_res)
                continue

            self._process_exist_and_valid_command(input_command)

    def include_router(self, router: Router) -> None:
        """
        Public. Registers the router in the application
        :param router: registered router
        :return: None
        """
        self.registered_routers.add_registered_router(router)

    def include_routers(self, *routers: Router) -> None:
        """
        Public. Registers the routers in the application
        :param routers: registered routers
        :return: None
        """
        for router in routers:
            self.include_router(router)

    def add_message_on_startup(self, message: str) -> None:
        """
        Public. Adds a message that will be displayed when the application is launched
        :param message: the message being added
        :return: None
        """
        self._messages_on_startup.append(message)
