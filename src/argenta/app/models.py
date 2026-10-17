import difflib
from collections.abc import Callable
from functools import partial
from typing import Never

from argenta.app._default_printer import DefaultPrinter
from argenta.app.autocompleter import AutoCompleter
from argenta.app.behavior_handlers.models import (
    BehaviorHandlersFabric,
    BehaviorHandlersSettersMixin,
)
from argenta.app.dividing_line.models import DynamicDividingLine, StaticDividingLine
from argenta.app.presentation.ascii_art import BundledFont, FigletFont, FigletFontLoader
from argenta.app.presentation.renderers import PlainRenderer, Renderer, RichRenderer
from argenta.app.presentation.viewers import Viewer
from argenta.app.protocols import Printer
from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.command.exceptions import (
    InputCommandException,
    RepeatedInputFlagsException,
    UnprocessedInputFlagException,
)
from argenta.command.models import Command, InputCommand
from argenta.router import Router
from argenta.router.exceptions import RepeatedAliasNameException, RepeatedTriggerNameException

type Matches = list[str] | list[Never]

DEFAULT_EXIT_COMMAND = Command("q", description="Exit command")


class App(BehaviorHandlersSettersMixin):
    def __init__(
        self,
        *,
        prompt: str = ">>> ",
        initial_message: str = "Argenta",
        farewell_message: str = "See you",
        exit_command: Command = DEFAULT_EXIT_COMMAND,
        system_router_title: str = "System points:",
        dividing_line: StaticDividingLine | DynamicDividingLine | None = None,
        repeat_command_groups_printing: bool = False,
        override_system_messages: bool = False,
        autocompleter: AutoCompleter | None = None,
        printer: Printer | None = None,
        initial_message_font: FigletFont | None = None,
        farewell_message_font: FigletFont | None = None,
    ) -> None:
        """
        Public. The essence of the application itself.
        Configures and manages all aspects of the behavior
        and presentation of the user interacting with the user
        :param prompt: displayed before entering the command
        :param initial_message: displayed at the start of the app
        :param farewell_message: displayed at the end of the app
        :param exit_command: the entity of the command that will be terminated when entered
        :param system_router_title: system router title
        :param dividing_line: the entity of the dividing line
        :param repeat_command_groups_printing: whether to repeat
               the available commands and their description
        :param override_system_messages: whether to redefine
               the default formatting of system messages
        :param autocompleter: the entity of the autocompleter
        :param printer: system messages text output function
        :param initial_message_font: FIGlet font for the initial message
        :param farewell_message_font: FIGlet font for the farewell message
        :return: None
        """
        font_loader = FigletFontLoader()
        initial_font = initial_message_font or font_loader.load_bundled(BundledFont.TARTY1)
        farewell_font = farewell_message_font or font_loader.load_bundled(BundledFont.CHUNKY)

        self.prompt: str = prompt
        self.repeat_command_groups_printing: bool = repeat_command_groups_printing
        self.registered_routers: RegisteredRouters = RegisteredRouters()

        self._printer: Printer = printer or DefaultPrinter()
        self._exit_command: Command = exit_command
        self._autocompleter: AutoCompleter = autocompleter or AutoCompleter()
        self._dividing_line: StaticDividingLine | DynamicDividingLine | None = dividing_line
        self._override_system_messages: bool = override_system_messages
        self._system_router: Router = Router(title=system_router_title)
        self._messages_on_startup: list[str] = []

        self._renderer: Renderer = (
            PlainRenderer()
            if self._override_system_messages
            else RichRenderer(
                initial_message_font=initial_font,
                farewell_message_font=farewell_font,
            )
        )

        self._viewer: Viewer = Viewer(
            printer=self._printer,
            renderer=self._renderer,
            dividing_line=self._dividing_line,
            override_system_messages=self._override_system_messages,
        )
        self._handlers_fabric: BehaviorHandlersFabric = BehaviorHandlersFabric(
            printer=self._printer,
            renderer=self._renderer,
            most_similar_command_getter=self._most_similar_command,
        )

        self._initial_message: str = self._renderer.render_initial_message(initial_message)
        rendered_farewell = self._renderer.render_farewell_message(farewell_message)

        super().__init__(
            description_message_generator=(
                self._handlers_fabric.generate_description_message_generator()
            ),
            incorrect_input_syntax_handler=(
                self._handlers_fabric.generate_incorrect_input_syntax_handler()
            ),
            repeated_input_flags_handler=(
                self._handlers_fabric.generate_repeated_input_flags_handler()
            ),
            empty_input_command_handler=(
                self._handlers_fabric.generate_empty_input_command_handler()
            ),
            unknown_command_handler=self._handlers_fabric.generate_unknown_command_handler(),
            exit_command_handler=self._handlers_fabric.generate_exit_command_handler(
                rendered_farewell
            ),
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

    @property
    def printer(self) -> Printer:
        """Public. System messages text output function used by runtimes"""
        return self._printer

    @property
    def autocompleter(self) -> AutoCompleter:
        """Public. Input autocompleter used by interactive runtimes"""
        return self._autocompleter

    @property
    def renderer(self) -> Renderer:
        """Public. Renderer used by runtimes for prompts and messages"""
        return self._renderer

    @property
    def viewer(self) -> Viewer:
        """Public. Viewer used by runtimes to present framed output"""
        return self._viewer

    @property
    def exit_command(self) -> Command:
        """Public. The command whose trigger exits the running application"""
        return self._exit_command

    @property
    def initial_message(self) -> str:
        """Public. Rendered message shown before the run loop starts"""
        return self._initial_message

    def add_message_on_startup(self, message: str) -> None:
        """
        Public. Adds a message that will be displayed when the application is launched
        :param message: the message being added
        :return: None
        """
        self._messages_on_startup.append(message)

    def prepare_for_run(self) -> None:
        """
        Public. Registers the system router, validates router collisions
        and shows the configured startup presentation; called by runtimes
        once before entering their run loop
        :return: None
        """
        self._setup_system_router()
        self._validate_routers_for_collisions()

        if self._messages_on_startup:
            self._viewer.view_messages_on_startup(self._messages_on_startup)

        if not self.repeat_command_groups_printing:
            self._viewer.view_command_groups_description(
                self.description_message_generator, self.registered_routers
            )

    def dispatch_input_command(self, input_command: InputCommand) -> bool:
        """
        Public. Routes an entered command through the dispatch path:
        unknown and exit commands go to their behavior handlers, valid
        commands go to the appropriate router handler
        :param input_command: the command to dispatch
        :return: True when the exit command was dispatched
        """
        if self._is_unknown_command(input_command):
            self._viewer.view_framed_text_from_generator(
                output_text_generator=partial(self._unknown_command_handler, input_command)
            )
            return False

        if self._is_exit_command(input_command):
            self._system_router.finds_appropriate_handler(input_command)
            return True

        self._process_exist_and_valid_command(input_command)
        return False

    def handle_input_error(self, error: InputCommandException, raw_command: str) -> None:
        """
        Public. Routes an input parsing error to the configured
        behavior handler and presents it framed
        :param error: the parsing error
        :param raw_command: the raw input that failed to parse
        :return: None
        """
        output_generator: Callable[[], None]
        if isinstance(error, UnprocessedInputFlagException):
            output_generator = partial(self._incorrect_input_syntax_handler, raw_command)
        elif isinstance(error, RepeatedInputFlagsException):
            output_generator = partial(self._repeated_input_flags_handler, raw_command)
        else:
            output_generator = self._empty_input_command_handler
        self._viewer.view_framed_text_from_generator(output_text_generator=output_generator)

    def _is_exit_command(self, command: InputCommand) -> bool:
        return (
            self._system_router.command_handlers.get_command_handler_by_trigger(
                command.trigger.lower()
            )
            is not None
        )

    def _is_unknown_command(self, input_command: InputCommand) -> bool:
        return self.registered_routers.get_router_by_trigger(input_command.trigger.lower()) is None

    def _validate_routers_for_collisions(self) -> None:
        seen_names: set[str] = set()

        for router_entity in self.registered_routers:
            trigger_collisions = seen_names.intersection(router_entity.triggers)
            if trigger_collisions:
                raise RepeatedTriggerNameException(trigger_collisions)

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
        self._system_router.command(self.exit_command)(self._exit_command_handler)
        self.registered_routers.add_registered_router(self._system_router)

    def _process_exist_and_valid_command(self, input_command: InputCommand) -> None:
        processing_router = self.registered_routers.get_router_by_trigger(
            input_command.trigger.lower()
        )

        if not processing_router:
            raise RuntimeError(f"Router for '{input_command.trigger}' not found. Panic!")

        self.viewer.view_framed_text_from_generator(
            output_text_generator=lambda: processing_router.finds_appropriate_handler(
                input_command
            ),
            is_stdout_redirected_by_router=processing_router.is_redirect_stdout_disabled,
        )
