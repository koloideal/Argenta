__all__ = ["App"]

import io
import re
from contextlib import redirect_stdout
from typing import Callable, Never, TypeAlias

from art import text2art
from prompt_toolkit import HTML
from rich.console import Console
from rich.markup import escape

from argenta.app.autocompleter import AutoCompleter
from argenta.app.dividing_line.models import DynamicDividingLine, StaticDividingLine
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
        prompt: str | HTML,
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
        self._prompt: str | HTML = prompt
        self._print_func: Printer = print_func
        self._exit_command: Command = exit_command
        self._dividing_line: StaticDividingLine | DynamicDividingLine | None = dividing_line
        self._repeat_command_groups_printing: bool = repeat_command_groups_printing
        self._override_system_messages: bool = override_system_messages
        self._autocompleter: AutoCompleter = autocompleter
        self.system_router: Router = Router(title=system_router_title)

        self._farewell_message: str = farewell_message
        self._initial_message: str = initial_message

        self._stdout_buffer: io.StringIO = io.StringIO()

        self._description_message_gen: DescriptionMessageGenerator = (
            lambda command, description: f"{command} *=*=* {description}"
        )
        self.registered_routers: RegisteredRouters = RegisteredRouters()
        self._messages_on_startup: list[str] = []

        self._incorrect_input_syntax_handler: NonStandardBehaviorHandler[str] = (
            lambda _: print_func(f"Incorrect flag syntax: {_}")
        )
        self._repeated_input_flags_handler: NonStandardBehaviorHandler[str] = (
            lambda _: print_func(f"Repeated input flags: {_}")
        )
        self._empty_input_command_handler: EmptyCommandHandler = lambda: print_func(
            "Empty input command"
        )
        self._unknown_command_handler: NonStandardBehaviorHandler[InputCommand] = (
            lambda _: print_func(f"Unknown command: {_.trigger}")
        )
        self._exit_command_handler: NonStandardBehaviorHandler[Response] = (
            lambda _: print_func(self._farewell_message)
        )

    def set_description_message_pattern(self, _: DescriptionMessageGenerator, /) -> None:
        """
        Public. Sets the output pattern of the available commands
        :param _: output pattern of the available commands
        :return: None
        """
        self._description_message_gen = _

    def set_incorrect_input_syntax_handler(
        self, _: NonStandardBehaviorHandler[str], /
    ) -> None:
        """
        Public. Sets the handler for incorrect flags when entering a command
        :param _: handler for incorrect flags when entering a command
        :return: None
        """
        self._incorrect_input_syntax_handler = _

    def set_repeated_input_flags_handler(
        self, _: NonStandardBehaviorHandler[str], /
    ) -> None:
        """
        Public. Sets the handler for repeated flags when entering a command
        :param _: handler for repeated flags when entering a command
        :return: None
        """
        self._repeated_input_flags_handler = _

    def set_unknown_command_handler(
        self, _: NonStandardBehaviorHandler[InputCommand], /
    ) -> None:
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

    def set_exit_command_handler(
        self, _: NonStandardBehaviorHandler[Response], /
    ) -> None:
        """
        Public. Sets the handler for exit command when entering a command
        :param _: handler for exit command when entering a command
        :return: None
        """
        self._exit_command_handler = _

    def _print_command_group_description(self) -> None:
        """
        Private. Prints the description of the available commands
        :return: None
        """
        for registered_router in self.registered_routers:
            self._print_func('\n'+registered_router.title)
            for command_handler in registered_router.command_handlers:
                handled_command = command_handler.handled_command
                self._print_func(
                    self._description_message_gen(
                        handled_command.trigger,
                        handled_command.description,
                    )
                )

    def _print_static_framed_text(self, text: str) -> None:
        """
        Private. Outputs text by framing it in a static or dynamic split strip
        :param text: framed text
        :return: None
        """
        match self._dividing_line:
            case StaticDividingLine() as dividing_line:
                self._print_func(
                    dividing_line.get_full_static_line(
                        is_override=self._override_system_messages
                    )
                )
                print(text.strip("\n"))
                self._print_func(
                    dividing_line.get_full_static_line(
                        is_override=self._override_system_messages
                    )
                )
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
                print('\n' + text.strip("\n") + '\n')
            case _:
                raise NotImplementedError(f'Dividing line with type {self._dividing_line} is not implemented')

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

        @self.system_router.command(self._exit_command)
        def _(response: Response) -> None:
            self._exit_command_handler(response)

        self.registered_routers.add_registered_router(self.system_router)
    
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
        matches_startswith_cmd: Matches = sorted(
            cmd for cmd in all_commands if unknown_command.startswith(cmd)
        )

        matches: Matches = matches_startswith_unknown_command or matches_startswith_cmd

        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            return sorted(matches, key=lambda cmd: len(cmd))[0]
        else:
            return None

    def _setup_default_view(self) -> None:
        """
        Private. Sets up default app view
        :return: None
        """
        if isinstance(self._prompt, str):
            self._prompt = f"\n<gray><b>{self._prompt}</b></gray>"
        self._initial_message = (
            "\n" + f"[bold red]{text2art(self._initial_message, font='tarty1')}"
        )
        self._farewell_message = (
            "[bold red]\n\n"
            + str(text2art(self._farewell_message, font="chanky"))  # pyright: ignore[reportUnknownArgumentType]
            + "\n[/bold red]\n"
            + "[red i]github.com/koloideal/Argenta[/red i] | [red bold i]made by kolo[/red bold i]\n"
        )
        self._description_message_gen = lambda command, description: (
            f"[bold red]{escape('[' + command + ']')}[/bold red] "
            f"[blue dim]*=*=*[/blue dim] "
            f"[bold yellow italic]{escape(description)}"
        )
        self._incorrect_input_syntax_handler = lambda raw_command: self._print_func(
            f"[red bold]Incorrect flag syntax: {escape(raw_command)}"
        )
        self._repeated_input_flags_handler = lambda raw_command: self._print_func(
            f"[red bold]Repeated input flags: {escape(raw_command)}"
        )
        self._empty_input_command_handler = lambda: self._print_func(
            "[red bold]Empty input command"
        )

        def unknown_command_handler(command: InputCommand) -> None:
            cmd_trg: str = command.trigger
            mst_sim_cmd: str | None = self._most_similar_command(cmd_trg)
            first_part_of_text = (
                f"[red]Unknown command:[/red] [blue]{escape(cmd_trg)}[/blue]"
            )
            second_part_of_text = (
                ("[red], most similar:[/red] " + ("[blue]" + mst_sim_cmd + "[/blue]"))
                if mst_sim_cmd
                else ""
            )
            self._print_func(first_part_of_text + second_part_of_text)

        self._unknown_command_handler = unknown_command_handler

    def _pre_cycle_setup(self) -> None:
        """
        Private. Configures various aspects of the application before the start of the cycle
        :return: None
        """
        self._setup_system_router()
        self._validate_routers_for_collisions()
        self._autocompleter.initial_setup(self.registered_routers.get_triggers())

        self._print_func(self._initial_message)
        self._print_func('\n'.join(self._messages_on_startup))

        if not self._repeat_command_groups_printing:
            self._print_command_group_description()

    def _process_exist_and_valid_command(self, input_command: InputCommand) -> None:
        processing_router = self.registered_routers.get_router_by_trigger(input_command.trigger.lower())
        
        if not processing_router:
            raise RuntimeError(f"Router for '{input_command.trigger}' not found. Panic!")

        match (self._dividing_line, processing_router.disable_redirect_stdout):
            case (DynamicDividingLine(), False):
                stdout_result = self._capture_stdout(
                    lambda: processing_router.finds_appropriate_handler(input_command)
                )
                clear_text = _ANSI_ESCAPE_RE.sub("", stdout_result)
                max_length_line = max([len(line) for line in clear_text.split("\n")])
                max_length_line = (
                    max_length_line
                    if 10 <= max_length_line <= 100
                    else 100
                    if max_length_line > 100
                    else 10
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
            case (None, bool()):
                processing_router.finds_appropriate_handler(input_command)
            case _:
                raise NotImplementedError(f'Dividing line with type {self._dividing_line} is not implemented')


AVAILABLE_DIVIDING_LINES: TypeAlias = StaticDividingLine | DynamicDividingLine
DEFAULT_PRINT_FUNC: Printer = Console().print
DEFAULT_EXIT_COMMAND: Command = Command("q", description="Exit command")


class App(BaseApp):
    def __init__(
        self,
        *,
        prompt: str | HTML = ">>> ",
        initial_message: str = "Argenta\n",
        farewell_message: str = "\nSee you\n",
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
        if not self._override_system_messages:
            self._setup_default_view()

    def run_polling(self) -> None:
        """
        Private. Starts the user input processing cycle
        :return: None
        """
        self._pre_cycle_setup()
        while True:
            if self._repeat_command_groups_printing:
                self._print_command_group_description()

            raw_command: str = self._autocompleter.prompt(self._prompt)
            print() # post-prompt gap

            try:
                input_command: InputCommand = InputCommand.parse(raw_command=raw_command)
            except InputCommandException as error: # noqa F841
                stderr_result = self._capture_stdout(
                    lambda: self._error_handler(error, raw_command) # noqa F821 
                )
                self._print_static_framed_text(stderr_result)
                continue

            if self._is_exit_command(input_command):
                self.system_router.finds_appropriate_handler(input_command)
                return

            if self._is_unknown_command(input_command):
                stdout_res = self._capture_stdout(
                    lambda: self._unknown_command_handler(input_command)
                )
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
