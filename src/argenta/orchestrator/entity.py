import os
from dataclasses import dataclass

from dishka import Provider, make_container

from argenta.a2ui import A2UIConfig, AgentRuntime, StdioTransport, Transport
from argenta.a2ui.provider import A2UIProvider
from argenta.app import App
from argenta.di.integration import setup_dishka
from argenta.di.providers import SystemProvider
from argenta.orchestrator.argparser import ArgParser
from argenta.repl import REPLRuntime


@dataclass(frozen=True, slots=True)
class RunnerConfig:
    """
    Environment bridge between `argenta run` and the Orchestrator:
    the CLI sets these variables and the Orchestrator reads them
    """

    runner_env_var: str = "RUN_FROM_ARGENTA_RUNNER"
    mode_env_var: str = "ARGENTA_RUN_MODE"
    a2ui_mode: str = "a2ui"


class Orchestrator:
    def __init__(
        self,
        arg_parser: ArgParser | None = None,
        custom_providers: list[Provider] | None = None,
        auto_inject_handlers: bool = True,
        runner_config: RunnerConfig | None = None,
    ):
        """
        Public. An orchestrator and configurator that defines the behavior
        of an integrated system, one level higher than the App
        :param arg_parser: Cmd argument parser and configurator at startup
        :param runner_config: environment bridge configuration used
               when the application is started via `argenta run`
        :return: None
        """
        self._runner_config: RunnerConfig = runner_config or RunnerConfig()
        self._arg_parser: ArgParser | None = (
            None if os.getenv(self._runner_config.runner_env_var) else arg_parser
        )
        self._custom_providers: list[Provider] = custom_providers or []
        self._auto_inject_handlers: bool = auto_inject_handlers

        if self._arg_parser is not None:
            self._arg_parser._parse_args()

    def run_repl(self, app: App) -> None:
        """
        Public. Starting the user input processing cycle; when started
        via `argenta run --a2ui`, delegates to run_agent over stdio JSONL
        :param app: a running application
        :return: None
        """
        if os.getenv(self._runner_config.mode_env_var) == self._runner_config.a2ui_mode:
            self.run_agent(app, StdioTransport())
            return

        container = make_container(
            SystemProvider(), *self._custom_providers, context={ArgParser: self._arg_parser}
        )
        setup_dishka(app, container, auto_inject=self._auto_inject_handlers)

        with container:
            REPLRuntime(app).run()

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
