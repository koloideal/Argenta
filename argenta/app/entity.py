from typing import Callable
from inspect import getfullargspec
from rich.console import Console
from art import text2art
import re

from argenta.command.models import Command, InputCommand
from argenta.router import Router
from argenta.router.defaults import system_router
from argenta.command.exceptions import (UnprocessedInputFlagException,
                                        RepeatedInputFlagsException,
                                        EmptyInputCommandException,
                                        BaseInputCommandException)
from argenta.app.exceptions import (InvalidRouterInstanceException,
                         InvalidDescriptionMessagePatternException,
                         NoRegisteredRoutersException,
                         NoRegisteredHandlersException,
                         IncorrectNumberOfHandlerArgsException)
from argenta.app.registered_routers.entity import RegisteredRouters


class App:
    def __init__(self,
                 prompt: str = '[italic dim bold]What do you want to do?\n',
                 initial_message: str = f'\n[bold red]{text2art('Argenta', font='tarty1')}\n\n',
                 farewell_message: str = f'[bold red]\n{text2art('\nSee   you\n', font='chanky')}[/bold red]\n'
                                         f'[red i]github.com/koloideal/Argenta[/red i] | '
                                         f'[red bold i]made by kolo[/red bold i]\n',
                 exit_command: str = 'Q',
                 exit_command_description: str = 'Exit command',
                 system_points_title: str = 'System points:',
                 ignore_exit_command_register: bool = True,
                 ignore_command_register: bool = True,
                 line_separate: str = f'\n[dim]{"--"*25}\n',
                 command_group_description_separate: str = '',
                 repeat_command_groups: bool = True,
                 print_func: Callable[[str], None] = Console().print) -> None:
        self._prompt = prompt
        self._print_func = print_func
        self._exit_command = exit_command
        self._exit_command_description = exit_command_description
        self._system_points_title = system_points_title
        self._ignore_exit_command_register = ignore_exit_command_register
        self._farewell_message = farewell_message
        self._initial_message = initial_message
        self._line_separate = line_separate
        self._command_group_description_separate = command_group_description_separate
        self._ignore_command_register = ignore_command_register
        self._repeat_command_groups_description = repeat_command_groups

        self._description_message_pattern: str = '[bold red][{command}][/bold red] [blue dim]*=*=*[/blue dim] [bold yellow italic]{description}'
        self._registered_routers: RegisteredRouters = RegisteredRouters()
        self._invalid_input_flags_handler: Callable[[str], None] = lambda raw_command: print_func(f'[red bold]Incorrect flag syntax: {raw_command}')
        self._repeated_input_flags_handler: Callable[[str], None] = lambda raw_command: print_func(f'[red bold]Repeated input flags: {raw_command}')
        self._empty_input_command_handler: Callable[[], None] = lambda: print_func('[red bold]Empty input command')
        self._unknown_command_handler: Callable[[InputCommand], None] = lambda command: print_func(f"[red bold]Unknown command: {command.get_trigger()}")
        self._exit_command_handler: Callable[[], None] = lambda: print_func(self._farewell_message)
        self._messages_on_startup = []


    def start_polling(self) -> None:
        self._setup_system_router()
        self._validate_number_of_routers()
        self._validate_included_routers()

        self._print_func(self._initial_message)

        for message in self._messages_on_startup:
            self._print_func(message)

        if not self._repeat_command_groups_description:
            self._print_command_group_description()

        while True:
            if self._repeat_command_groups_description:
                self._print_command_group_description()

            raw_command: str = Console().input(self._prompt)

            try:
                input_command: InputCommand = InputCommand.parse(raw_command=raw_command)
            except BaseInputCommandException as error:
                self._print_func(self._line_separate)
                self._error_handler(error, raw_command)
                self._print_func(self._line_separate)

                if not self._repeat_command_groups_description:
                    self._print_func(self._prompt)
                continue

            if self._is_exit_command(input_command):
                return

            self._print_func(self._line_separate)

            if self._is_unknown_command(input_command):
                self._print_func(self._line_separate)
                if not self._repeat_command_groups_description:
                    self._print_func(self._prompt)
                continue

            for registered_router in self._registered_routers:
                registered_router.input_command_handler(input_command)

            self._print_func(self._line_separate)
            if not self._repeat_command_groups_description:
                self._print_func(self._prompt)


    def set_initial_message(self, message: str) -> None:
        self._initial_message: str = message


    def set_farewell_message(self, message: str) -> None:
        self._farewell_message: str = message


    def set_description_message_pattern(self, pattern: str) -> None:
        first_check = re.match(r'.*{command}.*', pattern)
        second_check = re.match(r'.*{description}.*', pattern)

        if bool(first_check) and bool(second_check):
            self._description_message_pattern: str = pattern
        else:
            raise InvalidDescriptionMessagePatternException(pattern)


    def set_invalid_input_flags_handler(self, handler: Callable[[str], None]) -> None:
        args = getfullargspec(handler).args
        if len(args) != 1:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._invalid_input_flags_handler = handler


    def set_repeated_input_flags_handler(self, handler: Callable[[str], None]) -> None:
        args = getfullargspec(handler).args
        if len(args) != 1:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._repeated_input_flags_handler = handler


    def set_unknown_command_handler(self, handler: Callable[[str], None]) -> None:
        args = getfullargspec(handler).args
        if len(args) != 1:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._unknown_command_handler = handler


    def set_empty_command_handler(self, handler: Callable[[], None]) -> None:
        args = getfullargspec(handler).args
        if len(args) != 0:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._empty_input_command_handler = handler


    def set_exit_command_handler(self, handler: Callable[[], None]) -> None:
        args = getfullargspec(handler).args
        if len(args) != 0:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._exit_command_handler = handler


    def add_message_on_startup(self, message: str) -> None:
        self._messages_on_startup.append(message)


    def include_router(self, router: Router) -> None:
        if not isinstance(router, Router):
            raise InvalidRouterInstanceException()

        router.set_ignore_command_register(self._ignore_command_register)
        self._registered_routers.add_registered_router(router)


    def include_routers(self, *routers: Router) -> None:
        for router in routers:
            self.include_router(router)


    def _validate_number_of_routers(self) -> None:
        if not self._registered_routers:
            raise NoRegisteredRoutersException()


    def _validate_included_routers(self) -> None:
        for router in self._registered_routers:
            if not router.get_command_handlers():
                raise NoRegisteredHandlersException(router.get_name())


    def _setup_system_router(self):
        system_router.set_title(self._system_points_title)
        @system_router.command(Command(trigger=self._exit_command,
                                       description=self._exit_command_description))
        def exit_command():
            self._exit_command_handler()

        if system_router not in self._registered_routers.get_registered_routers():
            self.include_router(system_router)


    def _is_exit_command(self, command: InputCommand):
        if command.get_trigger().lower() == self._exit_command.lower():
            if self._ignore_exit_command_register:
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
                if handled_command_trigger.lower() == command.get_trigger().lower():
                    if self._ignore_command_register:
                        return False
                    elif handled_command_trigger == command.get_trigger():
                        return False
        self._unknown_command_handler(command)
        return True


    def _print_command_group_description(self):
        for registered_router in self._registered_routers:
            self._print_func(registered_router.get_title())
            for command_handler in registered_router.get_command_handlers():
                self._print_func(self._description_message_pattern.format(
                        command=command_handler.get_handled_command().get_trigger(),
                        description=command_handler.get_handled_command().get_description()))
            self._print_func(self._command_group_description_separate)


    def _error_handler(self, error: BaseInputCommandException, raw_command: str) -> None:
        match error:
            case UnprocessedInputFlagException():
                self._invalid_input_flags_handler(raw_command)
            case RepeatedInputFlagsException():
                self._repeated_input_flags_handler(raw_command)
            case EmptyInputCommandException():
                self._empty_input_command_handler()


