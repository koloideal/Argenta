__all__ = ["Orchestrator"]

from argenta.app import App

from argenta.orchestrator.argparser import ArgParser
from argenta.di.integration import setup_dishka
from argenta.di.providers import SystemProvider

from dishka import Provider, make_container


DEFAULT_ARGPARSER: ArgParser = ArgParser(processed_args=[])


class Orchestrator:
    def __init__(self, arg_parser: ArgParser = DEFAULT_ARGPARSER,
                 custom_providers: list[Provider] = [],
                 auto_inject_handlers: bool = True):
        """
        Public. An orchestrator and configurator that defines the behavior of an integrated system, one level higher than the App
        :param arg_parser: Cmd argument parser and configurator at startup
        :return: None
        """
        self._arg_parser: ArgParser = arg_parser
        self._custom_providers: list[Provider] = custom_providers
        self._auto_inject_handlers: bool = auto_inject_handlers

    def start_polling(self, app: App) -> None:
        """
        Public. Starting the user input processing cycle
        :param app: a running application
        :return: None
        """
        container = make_container(SystemProvider(self._arg_parser), *self._custom_providers)
        setup_dishka(app, container, auto_inject=self._auto_inject_handlers)

        app.run_polling()
