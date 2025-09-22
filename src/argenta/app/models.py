from typing import Never, Optional
from rich.console import Console
from rich.markup import escape
from art import text2art
from contextlib import redirect_stdout
import io
import re

from argenta.app.protocols import DescriptionMessageGenerator, Printer, Handler, EmptyHandler
from argenta.command.models import Command, InputCommand
from argenta.router import Router
from argenta.router.defaults import system_router
from argenta.app.autocompleter import AutoCompleter
from argenta.app.dividing_line.models import StaticDividingLine, DynamicDividingLine
from argenta.command.exceptions import (
    UnprocessedInputFlagException,
    RepeatedInputFlagsException,
    EmptyInputCommandException,
    BaseInputCommandException,
)
from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.response import Response


class BaseApp:
    def __init__(self, *, prompt: str,
                 initial_message: str,
                 farewell_message: str,
                 exit_command: Command,
                 system_router_title: Optional[str],
                 ignore_command_register: bool,
                 dividing_line: StaticDividingLine | DynamicDividingLine,
                 repeat_command_groups: bool,
                 override_system_messages: bool,
                 autocompleter: AutoCompleter,
                 print_func: Printer) -> None:
        self._prompt = prompt
        self._print_func = print_func
        self._exit_command = exit_command
        self._system_router_title = system_router_title
        self._dividing_line = dividing_line
        self._ignore_command_register = ignore_command_register
        self._repeat_command_groups_description = repeat_command_groups
        self._override_system_messages = override_system_messages
        self._autocompleter = autocompleter

        self._farewell_message = farewell_message
        self._initial_message = initial_message

        self._description_message_gen: DescriptionMessageGenerator = lambda command, description: f"{command} *=*=* {description}"
        self._registered_routers: RegisteredRouters = RegisteredRouters()
        self._messages_on_startup: list[str] = []

        self._matching_lower_triggers_with_routers: dict[str, Router] = {}
        self._matching_default_triggers_with_routers: dict[str, Router] = {}

        if self._ignore_command_register:
            self._current_matching_triggers_with_routers: dict[str, Router] = self._matching_lower_triggers_with_routers
        else:
            self._current_matching_triggers_with_routers: dict[str, Router] = self._matching_default_triggers_with_routers

        self._incorrect_input_syntax_handler: Handler[str] = lambda _: print_func(f"Incorrect flag syntax: {_}")
        self._repeated_input_flags_handler: Handler[str] = lambda _: print_func(f"Repeated input flags: {_}")
        self._empty_input_command_handler: EmptyHandler = lambda: print_func("Empty input command")
        self._unknown_command_handler: Handler[InputCommand] = lambda _: print_func(f"Unknown command: {_.get_trigger()}")
        self._exit_command_handler: Handler[Response] = lambda _: print_func(self._farewell_message)

    def set_description_message_pattern(self, _: DescriptionMessageGenerator, /) -> None:
        """
        Public. Sets the output pattern of the available commands
        :param _: output pattern of the available commands
        :return: None
        """
        self._description_message_gen: DescriptionMessageGenerator = _

    def set_incorrect_input_syntax_handler(self, _: Handler[str], /) -> None:
        """
        Public. Sets the handler for incorrect flags when entering a command
        :param _: handler for incorrect flags when entering a command
        :return: None
        """
        self._incorrect_input_syntax_handler = _

    def set_repeated_input_flags_handler(self, _: Handler[str], /) -> None:
        """
        Public. Sets the handler for repeated flags when entering a command
        :param _: handler for repeated flags when entering a command
        :return: None
        """
        self._repeated_input_flags_handler = _

    def set_unknown_command_handler(self, _: Handler[InputCommand], /) -> None:
        """
        Public. Sets the handler for unknown commands when entering a command
        :param _: handler for unknown commands when entering a command
        :return: None
        """
        self._unknown_command_handler = _

    def set_empty_command_handler(self, _: EmptyHandler, /) -> None:
        """
        Public. Sets the handler for empty commands when entering a command
        :param _: handler for empty commands when entering a command
        :return: None
        """
        self._empty_input_command_handler = _

    def set_exit_command_handler(self, _: Handler[Response], /) -> None:
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
        for registered_router in self._registered_routers:
            if registered_router.title:
                self._print_func(registered_router.title)
            for command_handler in registered_router.get_command_handlers():
                handled_command = command_handler.get_handled_command()
                self._print_func(
                    self._description_message_gen(
                        handled_command.get_trigger(),
                        handled_command.get_description(),
                    )
                )
            self._print_func("")

    def _print_framed_text(self, text: str) -> None:
        """
        Private. Outputs text by framing it in a static or dynamic split strip
        :param text: framed text
        :return: None
        """
        if isinstance(self._dividing_line, DynamicDividingLine):
            clear_text = re.sub(r"\u001b\[[0-9;]*m", "", text)
            max_length_line = max([len(line) for line in clear_text.split("\n")])
            max_length_line = (
                max_length_line
                if 10 <= max_length_line <= 80
                else 80
                if max_length_line > 80
                else 10
            )

            self._print_func(
                self._dividing_line.get_full_dynamic_line(
                    length=max_length_line, is_override=self._override_system_messages
                )
            )
            print(text.strip("\n"))
            self._print_func(
                self._dividing_line.get_full_dynamic_line(
                    length=max_length_line, is_override=self._override_system_messages
                )
            )
        
        elif isinstance(self._dividing_line, StaticDividingLine): # pyright: ignore[reportUnnecessaryIsInstance]
            self._print_func(
                self._dividing_line.get_full_static_line(is_override=self._override_system_messages)
            )
            print(text.strip("\n"))
            self._print_func(
                self._dividing_line.get_full_static_line(is_override=self._override_system_messages)
            )

        else:
            raise NotImplementedError

    def _is_exit_command(self, command: InputCommand) -> bool:
        """
        Private. Checks if the given command is an exit command
        :param command: command to check
        :return: is it an exit command or not as bool
        """
        trigger = command.get_trigger()
        exit_trigger = self._exit_command.get_trigger()
        if self._ignore_command_register:
            if (
                trigger.lower() == exit_trigger.lower()
            ):
                return True
            elif trigger.lower() in [
                x.lower() for x in self._exit_command.get_aliases()
            ]:
                return True
        else:
            if trigger == exit_trigger:
                return True
            elif trigger in self._exit_command.get_aliases():
                return True
        return False

    def _is_unknown_command(self, command: InputCommand) -> bool:
        """
        Private. Checks if the given command is an unknown command
        :param command: command to check
        :return: is it an unknown command or not as bool
        """
        input_command_trigger = command.get_trigger()
        if self._ignore_command_register:
            if input_command_trigger.lower() in list(self._current_matching_triggers_with_routers.keys()):
                return False
        else:
            if input_command_trigger in list(self._current_matching_triggers_with_routers.keys()):
                return False
        return True

    def _error_handler(
        self, error: BaseInputCommandException, raw_command: str
    ) -> None:
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
        elif isinstance(error, EmptyInputCommandException):
            self._empty_input_command_handler()

    def _setup_system_router(self) -> None:
        """
        Private. Sets up system router
        :return: None
        """
        system_router.title = self._system_router_title

        @system_router.command(self._exit_command)
        def _(response: Response) -> None:
            self._exit_command_handler(response)

        if system_router not in self._registered_routers.get_registered_routers():
            system_router.set_command_register_ignore(self._ignore_command_register)
            self._registered_routers.add_registered_router(system_router)

    def _most_similar_command(self, unknown_command: str) -> str | None:
        all_commands = list(self._current_matching_triggers_with_routers.keys())

        matches: list[str] | list[Never] = sorted(
            cmd for cmd in all_commands if cmd.startswith(unknown_command)
        )
        if not matches:
            matches: list[str] | list[Never] = sorted(
                cmd for cmd in all_commands if unknown_command.startswith(cmd)
            )
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
        self._prompt = f"[italic dim bold]{self._prompt}"
        self._initial_message = ("\n" + f"[bold red]{text2art(self._initial_message, font='tarty1')}" + "\n")
        self._farewell_message = (
            "[bold red]\n\n" +
            str(text2art(self._farewell_message, font="chanky")) +
            "\n[/bold red]\n" +
            "[red i]github.com/koloideal/Argenta[/red i] | [red bold i]made by kolo[/red bold i]\n"
        )
        self._description_message_gen = lambda command, description: (
            f"[bold red]{escape('[' + command + ']')}[/bold red] "
            f"[blue dim]*=*=*[/blue dim] "
            f"[bold yellow italic]{escape(description)}"
        )
        self._incorrect_input_syntax_handler = lambda raw_command: self._print_func(f"[red bold]Incorrect flag syntax: {escape(raw_command)}")
        self._repeated_input_flags_handler = lambda raw_command: self._print_func(f"[red bold]Repeated input flags: {escape(raw_command)}")
        self._empty_input_command_handler = lambda: self._print_func("[red bold]Empty input command")

        def unknown_command_handler(command: InputCommand) -> None:
            cmd_trg: str = command.get_trigger()
            mst_sim_cmd: str | None = self._most_similar_command(cmd_trg)
            first_part_of_text = f"[red]Unknown command:[/red] [blue]{escape(cmd_trg)}[/blue]"
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

        for router_entity in self._registered_routers:
            router_triggers = router_entity.get_triggers()
            router_aliases = router_entity.get_aliases()
            combined = router_triggers + router_aliases

            for trigger in combined:
                self._matching_default_triggers_with_routers[trigger] = router_entity
                self._matching_lower_triggers_with_routers[trigger.lower()] = router_entity

        self._autocompleter.initial_setup(list(self._current_matching_triggers_with_routers.keys()))

        seen = {}
        for item in list(self._current_matching_triggers_with_routers.keys()):
            if item in seen:
                Console().print(f"\n[b red]WARNING:[/b red] Overlapping trigger or alias: [b blue]{item}[/b blue]")
            else:
                seen[item] = True

        if not self._override_system_messages:
            self._setup_default_view()

        self._print_func(self._initial_message)

        for message in self._messages_on_startup:
            self._print_func(message)
        if self._messages_on_startup:
            print("\n")
        if not self._repeat_command_groups_description:
            self._print_command_group_description()


class App(BaseApp):
    def __init__(
        self, *,
        prompt: str = "What do you want to do?\n\n",
        initial_message: str = "Argenta\n",
        farewell_message: str = "\nSee you\n",
        exit_command: Command = Command("Q", description="Exit command"),
        system_router_title: str | None = "System points:",
        ignore_command_register: bool = True,
        dividing_line: StaticDividingLine | DynamicDividingLine = StaticDividingLine(),
        repeat_command_groups: bool = True,
        override_system_messages: bool = False,
        autocompleter: AutoCompleter = AutoCompleter(),
        print_func: Printer = Console().print,
    ) -> None:
        """
        Public. The essence of the application itself.
        Configures and manages all aspects of the behavior and presentation of the user interacting with the user
        :param prompt: displayed before entering the command
        :param initial_message: displayed at the start of the app
        :param farewell_message: displayed at the end of the app
        :param exit_command: the entity of the command that will be terminated when entered
        :param system_router_title: system router title
        :param ignore_command_register: whether to ignore the case of the entered commands
        :param dividing_line: the entity of the dividing line
        :param repeat_command_groups: whether to repeat the available commands and their description
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
            ignore_command_register=ignore_command_register,
            dividing_line=dividing_line,
            repeat_command_groups=repeat_command_groups,
            override_system_messages=override_system_messages,
            autocompleter=autocompleter,
            print_func=print_func,
        )

    def run_polling(self) -> None:
        """
        Private. Starts the user input processing cycle
        :return: None
        """
        self._pre_cycle_setup()
        while True:
            if self._repeat_command_groups_description:
                self._print_command_group_description()

            raw_command: str = Console().input(self._prompt)

            try:
                input_command: InputCommand = InputCommand.parse(raw_command=raw_command)
            except BaseInputCommandException as error:
                with redirect_stdout(io.StringIO()) as f:
                    self._error_handler(error, raw_command)
                    res: str = f.getvalue()
                self._print_framed_text(res)
                continue

            if self._is_exit_command(input_command):
                system_router.finds_appropriate_handler(input_command)
                self._autocompleter.exit_setup(list(self._current_matching_triggers_with_routers.keys()))
                return

            if self._is_unknown_command(input_command):
                with redirect_stdout(io.StringIO()) as f:
                    self._unknown_command_handler(input_command)
                    res2: str = f.getvalue()
                self._print_framed_text(res2)
                continue

            processing_router = self._current_matching_triggers_with_routers[input_command.get_trigger().lower()]

            if processing_router.disable_redirect_stdout:
                if isinstance(self._dividing_line, StaticDividingLine):
                    self._print_func(self._dividing_line.get_full_static_line(is_override=self._override_system_messages))
                    processing_router.finds_appropriate_handler(input_command)
                    self._print_func(self._dividing_line.get_full_static_line(is_override=self._override_system_messages))
                else:
                    self._print_func(StaticDividingLine(self._dividing_line.get_unit_part()).get_full_static_line(is_override=self._override_system_messages))
                    processing_router.finds_appropriate_handler(input_command)
                    self._print_func(StaticDividingLine(self._dividing_line.get_unit_part()).get_full_static_line(is_override=self._override_system_messages))
            else:
                with redirect_stdout(io.StringIO()) as f:
                    processing_router.finds_appropriate_handler(input_command)
                    res3: str = f.getvalue()
                if res3:
                    self._print_framed_text(res3)

    def include_router(self, router: Router) -> None:
        """
        Public. Registers the router in the application
        :param router: registered router
        :return: None
        """
        router.set_command_register_ignore(self._ignore_command_register)
        self._registered_routers.add_registered_router(router)

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
