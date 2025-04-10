from typing import Callable
from rich.console import Console
from rich.markup import escape
from art import text2art
from contextlib import redirect_stdout
import io
import re

from argenta.command.models import Command, InputCommand
from argenta.router import Router
from argenta.router.defaults import system_router
from argenta.app.autocompleter import AutoCompleter
from argenta.app.dividing_line.models import StaticDividingLine, DynamicDividingLine
from argenta.command.exceptions import (UnprocessedInputFlagException,
                                        RepeatedInputFlagsException,
                                        EmptyInputCommandException,
                                        BaseInputCommandException)
from argenta.app.exceptions import (InvalidRouterInstanceException,
                                    NoRegisteredRoutersException,
                                    NoRegisteredHandlersException)
from argenta.app.registered_routers.entity import RegisteredRouters



class AppInit:
    def __init__(self,
                 prompt: str = '[italic dim bold]What do you want to do?\n',
                 initial_message: str = '\nArgenta\n',
                 farewell_message: str = '\nSee you\n',
                 exit_command: Command = Command('Q', 'Exit command'),
                 system_points_title: str | None = 'System points:',
                 ignore_command_register: bool = True,
                 dividing_line: StaticDividingLine | DynamicDividingLine = StaticDividingLine(),
                 repeat_command_groups: bool = True,
                 full_override_system_messages: bool = False,
                 autocompleter: AutoCompleter = AutoCompleter(),
                 print_func: Callable[[str], None] = Console().print) -> None:
        self._prompt = prompt
        self._print_func = print_func
        self._exit_command = exit_command
        self._system_points_title = system_points_title
        self._dividing_line = dividing_line
        self._ignore_command_register = ignore_command_register
        self._repeat_command_groups_description = repeat_command_groups
        self._full_override_system_messages = full_override_system_messages
        self._autocompleter = autocompleter

        self._farewell_message = farewell_message
        self._initial_message = initial_message


        self._description_message_gen: Callable[[str, str], str] = lambda command, description: f'[bold red]{escape('['+command+']')}[/bold red] [blue dim]*=*=*[/blue dim] [bold yellow italic]{escape(description)}'
        self._registered_routers: RegisteredRouters = RegisteredRouters()
        self._messages_on_startup = []

        self._invalid_input_flags_handler: Callable[[str], None] = lambda raw_command: print_func(f'[red bold]Incorrect flag syntax: {raw_command}')
        self._repeated_input_flags_handler: Callable[[str], None] = lambda raw_command: print_func(f'[red bold]Repeated input flags: {raw_command}')
        self._empty_input_command_handler: Callable[[], None] = lambda: print_func('[red bold]Empty input command')
        self._unknown_command_handler: Callable[[InputCommand], None] = lambda command: print_func(f"[red bold]Unknown command: {command.get_trigger()}")
        self._exit_command_handler: Callable[[], None] = lambda: print_func(self._farewell_message)


class AppSetters(AppInit):
    def set_description_message_pattern(self, pattern: Callable[[str, str], str]) -> None:
        self._description_message_gen: Callable[[str, str], str] = pattern


    def set_invalid_input_flags_handler(self, handler: Callable[[str], None]) -> None:
        self._invalid_input_flags_handler = handler


    def set_repeated_input_flags_handler(self, handler: Callable[[str], None]) -> None:
        self._repeated_input_flags_handler = handler


    def set_unknown_command_handler(self, handler: Callable[[str], None]) -> None:
        self._unknown_command_handler = handler


    def set_empty_command_handler(self, handler: Callable[[], None]) -> None:
        self._empty_input_command_handler = handler


    def set_exit_command_handler(self, handler: Callable[[], None]) -> None:
        self._exit_command_handler = handler


class AppPrinters(AppInit):
    def _print_command_group_description(self):
        for registered_router in self._registered_routers:
            if registered_router.get_title():
                self._print_func(registered_router.get_title())
            for command_handler in registered_router.get_command_handlers():
                self._print_func(self._description_message_gen(
                        command_handler.get_handled_command().get_trigger(),
                        command_handler.get_handled_command().get_description()))
            self._print_func('')


    def _print_framed_text_with_dynamic_line(self, text: str):
        clear_text = re.sub(r'\u001b\[[0-9;]*m', '', text)
        max_length_line = max([len(line) for line in clear_text.split('\n')])
        max_length_line = max_length_line if 10 <= max_length_line <= 80 else 80 if max_length_line > 80 else 10
        self._print_func(self._dividing_line.get_full_line(max_length_line))
        print(text.strip('\n'))
        self._print_func(self._dividing_line.get_full_line(max_length_line))


class AppNonStandardHandlers(AppPrinters):
    def _is_exit_command(self, command: InputCommand):
        if command.get_trigger().lower() == self._exit_command.get_trigger().lower():
            if self._ignore_command_register:
                system_router.input_command_handler(command)
                return True
            elif command.get_trigger() == self._exit_command:
                system_router.input_command_handler(command)
                return True
        return False


    def _is_unknown_command(self, command: InputCommand):
        for router_entity in self._registered_routers:
            for command_handler in router_entity.get_command_handlers():
                handled_command_trigger = command_handler.get_handled_command().get_trigger()
                if handled_command_trigger.lower() == command.get_trigger().lower() and self._ignore_command_register:
                    return False
                elif handled_command_trigger == command.get_trigger():
                    return False
        if isinstance(self._dividing_line, StaticDividingLine):
            self._print_func(self._dividing_line.get_full_line())
            self._unknown_command_handler(command)
            self._print_func(self._dividing_line.get_full_line())
        elif isinstance(self._dividing_line, DynamicDividingLine):
            with redirect_stdout(io.StringIO()) as f:
                self._unknown_command_handler(command)
                res: str = f.getvalue()
            self._print_framed_text_with_dynamic_line(res)
        return True


    def _error_handler(self, error: BaseInputCommandException, raw_command: str) -> None:
        match error:
            case UnprocessedInputFlagException():
                self._invalid_input_flags_handler(raw_command)
            case RepeatedInputFlagsException():
                self._repeated_input_flags_handler(raw_command)
            case EmptyInputCommandException():
                self._empty_input_command_handler()


class AppValidators(AppInit):
    def _validate_number_of_routers(self) -> None:
        if not self._registered_routers:
            raise NoRegisteredRoutersException()


    def _validate_included_routers(self) -> None:
        for router in self._registered_routers:
            if not router.get_command_handlers():
                raise NoRegisteredHandlersException(router.get_name())


class AppSetups(AppValidators, AppPrinters):
    def _setup_system_router(self):
        system_router.set_title(self._system_points_title)

        @system_router.command(self._exit_command)
        def exit_command():
            self._exit_command_handler()

        if system_router not in self._registered_routers.get_registered_routers():
            system_router.set_ignore_command_register(self._ignore_command_register)
            self._registered_routers.add_registered_router(system_router)

    def _setup_default_view(self):
        if not self._full_override_system_messages:
            self._initial_message = f'\n[bold red]{text2art(self._initial_message, font='tarty1')}\n\n'
            self._farewell_message = (
                f'[bold red]\n{text2art(f'\n{self._farewell_message}\n', font='chanky')}[/bold red]\n'
                f'[red i]github.com/koloideal/Argenta[/red i] | [red bold i]made by kolo[/red bold i]\n')

    def _pre_cycle_setup(self):
        self._setup_default_view()
        self._setup_system_router()
        self._validate_number_of_routers()
        self._validate_included_routers()

        all_triggers: list[str] = []
        for router_entity in self._registered_routers:
            all_triggers.extend(router_entity.get_triggers())
        self._autocompleter.initial_setup(all_triggers)

        self._print_func(self._initial_message)

        for message in self._messages_on_startup:
            self._print_func(message)

        if not self._repeat_command_groups_description:
            self._print_command_group_description()


class App(AppSetters, AppNonStandardHandlers, AppSetups):
    def start_polling(self) -> None:
        self._pre_cycle_setup()
        while True:
            if self._repeat_command_groups_description:
                self._print_command_group_description()

            raw_command: str = Console().input(self._prompt)

            try:
                input_command: InputCommand = InputCommand.parse(raw_command=raw_command)
            except BaseInputCommandException as error:
                if isinstance(self._dividing_line, StaticDividingLine):
                    self._print_func(self._dividing_line.get_full_line())
                    self._error_handler(error, raw_command)
                    self._print_func(self._dividing_line.get_full_line())
                elif isinstance(self._dividing_line, DynamicDividingLine):
                    with redirect_stdout(io.StringIO()) as f:
                        self._error_handler(error, raw_command)
                        res: str = f.getvalue()
                    self._print_framed_text_with_dynamic_line(res)
                continue

            if self._is_exit_command(input_command):
                self._autocompleter.exit_setup()
                return

            if self._is_unknown_command(input_command):
                continue

            if isinstance(self._dividing_line, StaticDividingLine):
                self._print_func(self._dividing_line.get_full_line())
                for registered_router in self._registered_routers:
                    registered_router.input_command_handler(input_command)
                self._print_func(self._dividing_line.get_full_line())
            elif isinstance(self._dividing_line, DynamicDividingLine):
                with redirect_stdout(io.StringIO()) as f:
                    for registered_router in self._registered_routers:
                        registered_router.input_command_handler(input_command)
                    res: str = f.getvalue()
                self._print_framed_text_with_dynamic_line(res)

            if not self._repeat_command_groups_description:
                self._print_func(self._prompt)


    def include_router(self, router: Router) -> None:
        if not isinstance(router, Router):
            raise InvalidRouterInstanceException()

        router.set_ignore_command_register(self._ignore_command_register)
        self._registered_routers.add_registered_router(router)


    def include_routers(self, *routers: Router) -> None:
        for router in routers:
            self.include_router(router)


    def add_message_on_startup(self, message: str) -> None:
        self._messages_on_startup.append(message)

