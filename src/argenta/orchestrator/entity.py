import os

from dishka import Provider, make_container

from argenta.a2ui import A2UIConfig, AgentRuntime, Transport
from argenta.a2ui.provider import A2UIProvider
from argenta.app import App
from argenta.di.integration import setup_dishka
from argenta.di.providers import SystemProvider
from argenta.orchestrator.argparser import ArgParser


class Orchestrator:
    def __init__(
        self,
        arg_parser: ArgParser | None = None,
        custom_providers: list[Provider] | None = None,
        auto_inject_handlers: bool = True,
    ):
        """
        Public. An orchestrator and configurator that defines the behavior
        of an integrated system, one level higher than the App
        :param arg_parser: Cmd argument parser and configurator at startup
        :return: None
        """
        self._arg_parser: ArgParser | None = (
            None if os.getenv("RUN_FROM_ARGENTA_RUNNER") else arg_parser
        )
        self._custom_providers: list[Provider] = custom_providers or []
        self._auto_inject_handlers: bool = auto_inject_handlers

        if self._arg_parser is not None:
            self._arg_parser._parse_args()

    def run_repl(self, app: App) -> None:
        """
        Public. Starting the user input processing cycle
        :param app: a running application
        :return: None
        """
        container = make_container(
            SystemProvider(), *self._custom_providers, context={ArgParser: self._arg_parser}
        )
        setup_dishka(app, container, auto_inject=self._auto_inject_handlers)

        with container:
            app._run_repl()

    def run_agent(self, app: App, transport: Transport, config: A2UIConfig | None = None) -> None:
        """
        Public. Runs the application as an A2UI agent: emits a surface built
        from the registered commands and dispatches incoming actions through
        the regular command handling path
        :param app: a running application
        :param transport: the A2UI message transport
        :param config: optional A2UI surface and envelope configuration
        :return: None
        """
        container = make_container(
            SystemProvider(),
            A2UIProvider(),
            *self._custom_providers,
            context={ArgParser: self._arg_parser, A2UIConfig: config or A2UIConfig()},
        )
        setup_dishka(app, container, auto_inject=self._auto_inject_handlers)

        with container:
            AgentRuntime(app, transport, container.get(A2UIConfig)).run()
