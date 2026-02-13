__all__ = ["App"]

import difflib
from typing import Never, TypeAlias

from rich.console import Console

from argenta.app.autocompleter import AutoCompleter
from argenta.app.behavior_handlers.models import (BehaviorHandlersFabric,
                                                  BehaviorHandlersSettersMixin)
from argenta.app.dividing_line.models import DynamicDividingLine, StaticDividingLine
from argenta.app.presentation.renderers import PlainRenderer, Renderer, RichRenderer
from argenta.app.presentation.viewers import Viewer
from argenta.app.protocols import Printer
from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.command.exceptions import (InputCommandException,
                                        RepeatedInputFlagsException,
                                        UnprocessedInputFlagException)
from argenta.command.models import Command, InputCommand
from argenta.response import Response
from argenta.router import Router
from argenta.router.exceptions import (RepeatedAliasNameException,
                                       RepeatedTriggerNameException)

Matches: TypeAlias = list[str] | list[Never]


class BaseApp(BehaviorHandlersSettersMixin):
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
        printer: Printer,
    ) -> None:
        self._prompt: str = prompt
        self._printer: Printer = printer
        self._exit_command: Command = exit_command
        self._dividing_line: StaticDividingLine | DynamicDividingLine | None = dividing_line
        self._repeat_command_groups_printing: bool = repeat_command_groups_printing
        self._override_system_messages: bool = override_system_messages
        self._autocompleter: AutoCompleter = autocompleter
        self._system_router: Router = Router(title=system_router_title)

        self.registered_routers: RegisteredRouters = RegisteredRouters()
        self._messages_on_startup: list[str] = []

        self._renderer: Renderer = PlainRenderer() if self._override_system_messages else RichRenderer()

        self._viewer: Viewer = Viewer(
            printer=self._printer,
            renderer=self._renderer,
            dividing_line=self._dividing_line,
            override_system_messages=self._override_system_messages,
        )
        self._handlers_fabric: BehaviorHandlersFabric = BehaviorHandlersFabric(
            printer=self._printer,
            renderer=self._renderer,
            most_similar_command_getter=self._most_similar_command
        )

        self._initial_message: str = self._renderer.render_initial_message(initial_message)
        self._farewell_message: str = self._renderer.render_farewell_message(farewell_message)

        super().__init__(
            description_message_generator = self._handlers_fabric.generate_description_message_generator(),
            incorrect_input_syntax_handler = self._handlers_fabric.generate_incorrect_input_syntax_handler(),
            repeated_input_flags_handler = self._handlers_fabric.generate_repeated_input_flags_handler(),
            empty_input_command_handler = self._handlers_fabric.generate_empty_input_command_handler(),
            unknown_command_handler = self._handlers_fabric.generate_unknown_command_handler(),
            exit_command_handler = self._handlers_fabric.generate_exit_command_handler(self._farewell_message)
        )

    def _is_exit_command(self, command: InputCommand) -> bool:
        if not self._system_router.command_handlers.get_command_handler_by_trigger(command.trigger.lower()):
            return False
        return True

    def _is_unknown_command(self, input_command: InputCommand) -> bool:
        if not self.registered_routers.get_router_by_trigger(input_command.trigger.lower()):
            return True
        return False

    def _error_handler(self, error: InputCommandException, raw_command: str) -> None:
        if isinstance(error, UnprocessedInputFlagException):
            self._incorrect_input_syntax_handler(raw_command)
        elif isinstance(error, RepeatedInputFlagsException):
            self._repeated_input_flags_handler(raw_command)
        else:
            self._empty_input_command_handler()

    def _validate_routers_for_collisions(self) -> None:
        seen_names: set[str] = set()

        for router_entity in self.registered_routers:
            if not seen_names.isdisjoint(router_entity.triggers):
                raise RepeatedTriggerNameException()

            alias_collisions = seen_names.intersection(router_entity.aliases)
            if alias_collisions:
                raise RepeatedAliasNameException(alias_collisions)

            seen_names.update(router_entity.triggers)
            seen_names.update(router_entity.aliases)

    def _most_similar_command(self, unknown_command: str) -> str | None:
        all_commands = self.registered_routers.get_triggers()
        matches = difflib.get_close_matches(unknown_command, all_commands, n=1)
        return matches[0] if matches else None

    def _setup_system_router(self) -> None:
        @self._system_router.command(self._exit_command)
        def _(response: Response) -> None:
            self._exit_command_handler(response)

        self.registered_routers.add_registered_router(self._system_router)

    def _pre_cycle_setup(self) -> None:
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

        self._viewer.view_framed_text_from_generator(
            output_text_generator=lambda: processing_router.finds_appropriate_handler(input_command),
            is_stdout_redirected_by_router=processing_router.is_redirect_stdout_disabled
        )

    def _run_repl(self) -> None:
        self._viewer.view_initial_message(self._initial_message)
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
                self._viewer.view_framed_text_from_generator(
                    output_text_generator=lambda: self._error_handler(error, raw_command) # noqa
                )
                continue

            if self._is_unknown_command(input_command):
                self._viewer.view_framed_text_from_generator(
                    output_text_generator=lambda: self._unknown_command_handler(input_command)
                )
                continue

            if self._is_exit_command(input_command):
                self._system_router.finds_appropriate_handler(input_command)
                return

            self._process_exist_and_valid_command(input_command)


class App(BaseApp):
    def __init__(
        self,
        *,
        prompt: str = ">>> ",
        initial_message: str = "Argenta",
        farewell_message: str = "See you",
        exit_command: Command = Command("q", description="Exit command"),
        system_router_title: str = "System points:",
        dividing_line: StaticDividingLine | DynamicDividingLine | None = None,
        repeat_command_groups_printing: bool = False,
        override_system_messages: bool = False,
        autocompleter: AutoCompleter | None = None,
        printer: Printer = Console().print,
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
        :param printer: system messages text output function
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
            printer=printer,
        )

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
