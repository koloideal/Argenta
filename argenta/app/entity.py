from typing import Callable
from ..command.entity import Command
from argenta.command.input_comand.entity import InputCommand
from argenta.command.input_comand.exceptions import InvalidInputFlagsException
from ..router.entity import Router
from .exceptions import (InvalidRouterInstanceException,
                         InvalidDescriptionMessagePatternException,
                         OnlyOneMainRouterIsAllowedException,
                         MissingMainRouterException,
                         MissingHandlerForUnknownCommandsException,
                         HandlerForUnknownCommandsOnNonMainRouterException,
                         NoRegisteredRoutersException,
                         NoRegisteredHandlersException,
                         RepeatedCommandInDifferentRoutersException)


class App:
    def __init__(self,
                 prompt: str = 'Enter a command',
                 initial_message: str = '\nHello, I am Argenta\n',
                 farewell_message: str = '\nGoodBye\n',
                 invalid_input_flags_message: str = 'Invalid input flags',
                 exit_command: str = 'Q',
                 exit_command_description: str = 'Exit command',
                 exit_command_title: str = 'System points:',
                 ignore_exit_command_register: bool = True,
                 ignore_command_register: bool = False,
                 line_separate: str = '',
                 command_group_description_separate: str = '',
                 repeat_command_groups: bool = True,
                 print_func: Callable[[str], None] = print) -> None:
        self.prompt = prompt
        self.print_func = print_func
        self.exit_command = exit_command
        self.exit_command_description = exit_command_description
        self.exit_command_title = exit_command_title
        self.ignore_exit_command_register = ignore_exit_command_register
        self.farewell_message = farewell_message
        self.initial_message = initial_message
        self.invalid_input_flags_message = invalid_input_flags_message
        self.line_separate = line_separate
        self.command_group_description_separate = command_group_description_separate
        self.ignore_command_register = ignore_command_register
        self.repeat_command_groups = repeat_command_groups

        self._routers: list[Router] = []
        self._registered_router_entities: list[dict[str, str | list[dict[str, Callable[[], None] | Command]] | Router]] = []
        self._app_main_router: Router | None = None
        self._description_message_pattern: str = '[{command}] *=*=* {description}'


    def start_polling(self) -> None:
        self._validate_number_of_routers()
        self._validate_included_routers()
        self._validate_main_router()
        self._validate_all_router_commands()

        self.print_func(self.initial_message)

        if not self.repeat_command_groups:
            self._print_command_group_description()
            self.print_func(self.prompt)

        while True:
            if self.repeat_command_groups:
                self._print_command_group_description()
                self.print_func(self.prompt)

            raw_command: str = input()
            try:
                command: Command = InputCommand.parse(raw_command=raw_command)
            except InvalidInputFlagsException:
                self.print_func(self.line_separate)
                self.print_func(self.command_group_description_separate)
                if not self.repeat_command_groups:
                    self.print_func(self.prompt)
                continue


            self._checking_command_for_exit_command(command.get_string_entity())
            self.print_func(self.line_separate)

            is_unknown_command: bool = self._check_is_command_unknown(command.get_string_entity())
            if is_unknown_command:
                if not self.repeat_command_groups:
                    self.print_func(self.prompt)
                continue

            for router in self._routers:
                router.input_command_handler(command)

            self.print_func(self.line_separate)
            self.print_func(self.command_group_description_separate)
            if not self.repeat_command_groups:
                self.print_func(self.prompt)


    def set_initial_message(self, message: str) -> None:
        self.initial_message: str = message


    def set_farewell_message(self, message: str) -> None:
        self.farewell_message: str = message


    def set_description_message_pattern(self, pattern: str) -> None:
        try:
            pattern.format(command='command',
                           description='description')
        except KeyError:
            raise InvalidDescriptionMessagePatternException(pattern)
        self._description_message_pattern: str = pattern


    def get_main_router(self) -> Router:
        return self._app_main_router


    def get_all_app_commands(self) -> list[str]:
        all_commands: list[str] = []
        for router in self._routers:
            all_commands.extend(router.get_all_commands())

        return all_commands


    def include_router(self, router: Router, is_main: True | False = False) -> None:
        if not isinstance(router, Router):
            raise InvalidRouterInstanceException()

        if is_main:
            if not self._app_main_router:
                self._app_main_router = router
                router.set_router_as_main()
            else:
                raise OnlyOneMainRouterIsAllowedException(self._app_main_router.get_name())

        router.set_ignore_command_register(self.ignore_command_register)
        self._routers.append(router)

        command_entities: list[dict[str, Callable[[], None] | Command]] = router.get_command_entities()
        self._registered_router_entities.append({'name': router.get_name(),
                                                 'title': router.get_title(),
                                                 'entity': router,
                                                 'commands': command_entities})


    def _validate_number_of_routers(self) -> None:
        if not self._routers:
            raise NoRegisteredRoutersException()


    def _validate_included_routers(self) -> None:
        for router in self._routers:
            if not router.get_command_entities():
                raise NoRegisteredHandlersException(router.get_name())


    def _validate_main_router(self):
        if not self._app_main_router:
            if len(self._routers) > 1:
                raise MissingMainRouterException()
            else:
                router = self._routers[0]
                router.set_router_as_main()
                self._app_main_router = router

        if not self._app_main_router.unknown_command_func:
            raise MissingHandlerForUnknownCommandsException()

        for router in self._routers:
            if router.unknown_command_func and self._app_main_router is not router:
                raise HandlerForUnknownCommandsOnNonMainRouterException()


    def _validate_all_router_commands(self) -> None:
        for idx in range(len(self._registered_router_entities)):
            current_router: Router = self._registered_router_entities[idx]['entity']
            routers_without_current_router = self._registered_router_entities.copy()
            routers_without_current_router.pop(idx)

            current_router_all_commands: list[str] = current_router.get_all_commands()

            for router_entity in routers_without_current_router:
                if len(set(current_router_all_commands).intersection(set(router_entity['entity'].get_all_commands()))) > 0:
                    raise RepeatedCommandInDifferentRoutersException()
                if self.ignore_command_register:
                    if len(set([x.lower() for x in current_router_all_commands]).intersection(set([x.lower() for x in router_entity['entity'].get_all_commands()]))) > 0:
                        raise RepeatedCommandInDifferentRoutersException()


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
        registered_router_entities: list[dict[str, str | list[dict[str, Callable[[], None] | Command]] | Router]] = self._registered_router_entities
        for router_entity in registered_router_entities:
            for command_entity in router_entity['commands']:
                if command_entity['command'].get_string_entity().lower() == command.lower():
                    if self.ignore_command_register:
                        return False
                    else:
                        if command_entity['command'] == command:
                            return False
        self._app_main_router.unknown_command_handler(command)
        self.print_func(self.line_separate)
        self.print_func(self.command_group_description_separate)
        return True


    def _print_command_group_description(self):
        for router_entity in self._registered_router_entities:
            self.print_func(router_entity['title'])
            for command_entity in router_entity['commands']:
                self.print_func(self._description_message_pattern.format(
                        command=command_entity['command'].get_string_entity(),
                        description=command_entity['command'].get_description()
                    )
                )
            self.print_func(self.command_group_description_separate)

        self.print_func(self.exit_command_title)
        self.print_func(self._description_message_pattern.format(
                command=self.exit_command,
                description=self.exit_command_description
            )
        )
        self.print_func(self.command_group_description_separate)

