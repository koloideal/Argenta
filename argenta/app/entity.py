from typing import Callable
from ..router.entity import Router
from .exceptions import (InvalidRouterInstanceException,
                         InvalidDescriptionMessagePatternException,
                         OnlyOneMainRouterIsAllowedException,
                         MissingMainRouterException,
                         MissingHandlersForUnknownCommandsOnMainRouterException,
                         HandlerForUnknownCommandsCanOnlyBeDeclaredForMainRouterException)


class App:
    def __init__(self,
                 prompt: str = 'Enter a command',
                 exit_command: str = 'q',
                 ignore_exit_command_register: bool = True,
                 initial_greeting: str = '\nHello, I am Argenta\n',
                 farewell_message: str = 'GoodBye',
                 line_separate: str = '',
                 command_group_description_separate: str = '',
                 print_func: Callable[[str], None] = print) -> None:
        self.prompt = prompt
        self.print_func = print_func
        self.exit_command = exit_command
        self.ignore_exit_command_register = ignore_exit_command_register
        self.farewell_message = farewell_message
        self.initial_greeting = initial_greeting
        self.line_separate = line_separate
        self.command_group_description_separate = command_group_description_separate

        self._routers: list[Router] = []
        self._registered_commands: list[dict[str, str | list[dict[str, Callable[[], None] | str]] | Router]] = []
        self._main_app_router: Router | None = None
        self._description_message_pattern: str = '[{command}] *=*=* {description}'


    def start_polling(self) -> None:
        self.print_func(self.initial_greeting)
        self._validate_main_router()

        while True:
            self._print_command_group_description()
            self.print_func(self.prompt)

            command: str = input()

            self._checking_command_for_exit_command(command)
            self.print_func(self.line_separate)

            is_unknown_command: bool = self._check_is_command_unknown(command)

            if is_unknown_command:
                continue

            for router in self._routers:
                router.input_command_handler(command)
            self.print_func(self.line_separate)
            self.print_func(self.command_group_description_separate)


    def set_initial_greeting(self, greeting: str) -> None:
        self.initial_greeting: str = greeting


    def set_farewell_message(self, message: str) -> None:
        self.farewell_message: str = message


    def set_description_message_pattern(self, pattern: str) -> None:
        try:
            pattern.format(command='command',
                           description='description')
        except KeyError:
            raise InvalidDescriptionMessagePatternException(pattern)
        self._description_message_pattern: str = pattern


    def _validate_main_router(self):
        if not self._main_app_router:
            raise MissingMainRouterException()

        if not self._main_app_router.unknown_command_func:
            raise MissingHandlersForUnknownCommandsOnMainRouterException()

        for router in self._routers:
            if router.unknown_command_func and self._main_app_router is not router:
                raise HandlerForUnknownCommandsCanOnlyBeDeclaredForMainRouterException()


    def _checking_command_for_exit_command(self, command: str):
        if command.lower() == self.exit_command.lower():
            if self.ignore_exit_command_register:
                self.print_func(self.farewell_message)
                exit(0)
            else:
                if command == self.exit_command:
                    self.print_func(self.farewell_message)
                    exit(0)


    def _check_is_command_unknown(self, command: str):
        registered_commands: list[dict[str, str | list[dict[str, Callable[[], None] | str]] | Router]] = self._registered_commands
        for router in registered_commands:
            for command_entity in router['commands']:
                if command_entity['command'].lower() == command.lower():
                    if router['router'].ignore_command_register:
                        return False
                    else:
                        if command_entity['command'] == command:
                            return False
        self._main_app_router.unknown_command_handler(command)
        self.print_func(self.line_separate)
        self.print_func(self.command_group_description_separate)
        return True


    def _print_command_group_description(self):
        for router in self._registered_commands:
            self.print_func(router['name'])
            for command_entity in router['commands']:
                self.print_func(self._description_message_pattern.format(
                        command=command_entity['command'],
                        description=command_entity['description']
                    )
                )
            self.print_func(self.command_group_description_separate)


    def include_router(self, router: Router, is_main: bool = False) -> None:
        if not isinstance(router, Router):
            raise InvalidRouterInstanceException()

        if is_main:
            if not self._main_app_router:
                self._main_app_router = router
                router.set_router_as_main()
            else:
                raise OnlyOneMainRouterIsAllowedException(router)

        self._routers.append(router)

        registered_commands: list[dict[str, Callable[[], None] | str]] = router.get_registered_commands()
        self._registered_commands.append({'name': router.get_name(),
                                         'router': router,
                                         'commands': registered_commands})

