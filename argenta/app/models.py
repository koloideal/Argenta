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
from argenta.app.exceptions import NoRegisteredHandlersException
from argenta.app.registered_routers.entity import RegisteredRouters



class BaseApp:
    def __init__(self,
                 prompt: str,
                 initial_message: str,
                 farewell_message: str,
                 exit_command: Command,
                 system_router_title: str | None,
                 ignore_command_register: bool,
                 dividing_line: StaticDividingLine | DynamicDividingLine,
                 repeat_command_groups: bool,
                 override_system_messages: bool,
                 autocompleter: AutoCompleter,
                 print_func: Callable[[str], None]) -> None:

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


        self._description_message_gen: Callable[[str, str], str] = lambda command, description: f'[{command}] *=*=* {description}'
        self._registered_routers: RegisteredRouters = RegisteredRouters()
        self._messages_on_startup: list[str] = []

        self._all_registered_triggers_in_lower: list[str] = []
        self._all_registered_triggers_in_default_case: list[str] = []

        self._invalid_input_flags_handler: Callable[[str], None] = lambda raw_command: print_func(f'Incorrect flag syntax: {raw_command}')
        self._repeated_input_flags_handler: Callable[[str], None] = lambda raw_command: print_func(f'Repeated input flags: {raw_command}')
        self._empty_input_command_handler: Callable[[], None] = lambda: print_func('Empty input command')
        self._unknown_command_handler: Callable[[InputCommand], None] = lambda command: print_func(f"Unknown command: {command.get_trigger()}")
        self._exit_command_handler: Callable[[], None] = lambda: print_func(self._farewell_message)


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


    def _print_command_group_description(self):
        for registered_router in self._registered_routers:
            if registered_router.get_title():
                self._print_func(registered_router.get_title())
            for command_handler in registered_router.get_command_handlers():
                self._print_func(self._description_message_gen(
                        command_handler.get_handled_command().get_trigger(),
                        command_handler.get_handled_command().get_description()))
            self._print_func('')


    def _print_framed_text(self, text: str):
        if isinstance(self._dividing_line, StaticDividingLine):
            self._print_func(self._dividing_line.get_full_static_line(self._override_system_messages))
            self._print_func(text)
            self._print_func(self._dividing_line.get_full_static_line(self._override_system_messages))

        elif isinstance(self._dividing_line, DynamicDividingLine):
            clear_text = re.sub(r'\u001b\[[0-9;]*m', '', text)
            max_length_line = max([len(line) for line in clear_text.split('\n')])
            max_length_line = max_length_line if 10 <= max_length_line <= 80 else 80 if max_length_line > 80 else 10

            self._print_func(self._dividing_line.get_full_dynamic_line(max_length_line, self._override_system_messages))
            print(text.strip('\n'))
            self._print_func(self._dividing_line.get_full_dynamic_line(max_length_line, self._override_system_messages))


    def _is_exit_command(self, command: InputCommand):
        if self._ignore_command_register:
            if command.get_trigger().lower() == self._exit_command.get_trigger().lower():
                return True
            elif command.get_trigger().lower() in [x.lower() for x in self._exit_command.get_aliases()]:
                return True
        else:
            if command.get_trigger() == self._exit_command.get_trigger():
                return True
            elif command.get_trigger() in self._exit_command.get_aliases():
                return True
        return False


    def _is_unknown_command(self, command: InputCommand):
        input_command_trigger = command.get_trigger()
        if self._ignore_command_register:
            if input_command_trigger.lower() in self._all_registered_triggers_in_lower:
                return False
        else:
            if input_command_trigger in self._all_registered_triggers_in_default_case:
                return False

        with redirect_stdout(io.StringIO()) as f:
            self._unknown_command_handler(command)
            res: str = f.getvalue()
        self._print_framed_text(res)
        return True


    def _error_handler(self, error: BaseInputCommandException, raw_command: str) -> None:
        match error:
            case UnprocessedInputFlagException():
                self._invalid_input_flags_handler(raw_command)
            case RepeatedInputFlagsException():
                self._repeated_input_flags_handler(raw_command)
            case EmptyInputCommandException():
                self._empty_input_command_handler()


    def _validate_included_routers(self) -> None:
        for router in self._registered_routers:
            if not router.get_command_handlers():
                raise NoRegisteredHandlersException(router.get_name())


    def _setup_system_router(self):
        system_router.set_title(self._system_router_title)

        @system_router.command(self._exit_command)
        def exit_command():
            self._exit_command_handler()

        if system_router not in self._registered_routers.get_registered_routers():
            system_router.set_ignore_command_register(self._ignore_command_register)
            self._registered_routers.add_registered_router(system_router)


    def _setup_default_view(self):
        if not self._override_system_messages:
            self._initial_message = f'\n[bold red]{text2art(self._initial_message, font='tarty1')}\n\n'
            self._farewell_message = (f'[bold red]\n{text2art(f'\n{self._farewell_message}\n', font='chanky')}[/bold red]\n'
                                      f'[red i]github.com/koloideal/Argenta[/red i] | [red bold i]made by kolo[/red bold i]\n')
            self._description_message_gen = lambda command, description: (f'[bold red]{escape('[' + command + ']')}[/bold red] '
                                                                          f'[blue dim]*=*=*[/blue dim] '
                                                                          f'[bold yellow italic]{escape(description)}')
            self._invalid_input_flags_handler = lambda raw_command: self._print_func(f'[red bold]Incorrect flag syntax: {escape(raw_command)}')
            self._repeated_input_flags_handler = lambda raw_command: self._print_func(f'[red bold]Repeated input flags: {escape(raw_command)}')
            self._empty_input_command_handler = lambda: self._print_func('[red bold]Empty input command')
            self._unknown_command_handler = lambda command: self._print_func(f"[red bold]Unknown command: {escape(command.get_trigger())}")


    def _pre_cycle_setup(self):
        self._setup_default_view()
        self._setup_system_router()
        self._validate_included_routers()

        for router_entity in self._registered_routers:
            self._all_registered_triggers_in_default_case.extend(router_entity.get_triggers())
            self._all_registered_triggers_in_default_case.extend(router_entity.get_aliases())

            self._all_registered_triggers_in_lower.extend([x.lower() for x in router_entity.get_triggers()])
            self._all_registered_triggers_in_lower.extend([x.lower() for x in router_entity.get_aliases()])

        self._autocompleter.initial_setup(self._all_registered_triggers_in_lower)

        self._print_func(self._initial_message)

        for message in self._messages_on_startup:
            self._print_func(message)
        if self._messages_on_startup:
            print('\n\n')

        if not self._repeat_command_groups_description:
            self._print_command_group_description()



class App(BaseApp):
    def __init__(self,
                 prompt: str = '[italic dim bold]What do you want to do?\n',
                 initial_message: str = '\nArgenta\n',
                 farewell_message: str = '\nSee you\n',
                 exit_command: Command = Command('Q', 'Exit command'),
                 system_router_title: str | None = 'System points:',
                 ignore_command_register: bool = True,
                 dividing_line: StaticDividingLine | DynamicDividingLine = StaticDividingLine(),
                 repeat_command_groups: bool = True,
                 override_system_messages: bool = False,
                 autocompleter: AutoCompleter = AutoCompleter(),
                 print_func: Callable[[str], None] = Console().print) -> None:
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
        super().__init__(prompt=prompt,
                         initial_message=initial_message,
                         farewell_message=farewell_message,
                         exit_command=exit_command,
                         system_router_title=system_router_title,
                         ignore_command_register=ignore_command_register,
                         dividing_line=dividing_line,
                         repeat_command_groups=repeat_command_groups,
                         override_system_messages=override_system_messages,
                         autocompleter=autocompleter,
                         print_func=print_func)


    def run_polling(self) -> None:
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
                system_router.input_command_handler(input_command)
                self._autocompleter.exit_setup()
                return

            if self._is_unknown_command(input_command):
                continue

            with redirect_stdout(io.StringIO()) as f:
                for registered_router in self._registered_routers:
                    registered_router.input_command_handler(input_command)
                res: str = f.getvalue()
            self._print_framed_text(res)

            if not self._repeat_command_groups_description:
                self._print_func(self._prompt)


    def include_router(self, router: Router) -> None:
        router.set_ignore_command_register(self._ignore_command_register)
        self._registered_routers.add_registered_router(router)


    def include_routers(self, *routers: Router) -> None:
        for router in routers:
            self.include_router(router)


    def add_message_on_startup(self, message: str) -> None:
        self._messages_on_startup.append(message)

