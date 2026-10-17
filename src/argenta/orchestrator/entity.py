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
    a2ui_transport_env_var: str = "ARGENTA_A2UI_TRANSPORT"
    a2ui_ws_transport: str = "ws"
    a2ui_ws_port_env_var: str = "ARGENTA_A2UI_WS_PORT"
    a2ui_ws_default_host: str = "127.0.0.1"
    a2ui_ws_default_port: int = 8765
    a2ui_verbose_env_var: str = "ARGENTA_A2UI_VERBOSE"


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
        via `argenta run --a2ui`, delegates to run_agent over the selected transport
        :param app: a running application
        :return: None
        """
        if os.getenv(self._runner_config.mode_env_var) == self._runner_config.a2ui_mode:
            verbose = bool(os.getenv(self._runner_config.a2ui_verbose_env_var))
            self.run_agent(app, self._resolve_agent_transport(), verbose=verbose)
            return

        container = make_container(
            SystemProvider(), *self._custom_providers, context={ArgParser: self._arg_parser}
        )
        setup_dishka(app, container, auto_inject=self._auto_inject_handlers)

        with container:
            REPLRuntime(app).run()

    def run_agent(
        self,
        app: App,
        transport: Transport,
        config: A2UIConfig | None = None,
        *,
        verbose: bool = False,
    ) -> None:
        """
        Public. Runs the application as an A2UI agent: emits a surface built
        from the registered commands and dispatches incoming actions through
        the regular command handling path

        Construct the App with ``override_system_messages=True`` so system
        output is rendered as plain text — Rich markup is meaningless for
        non-terminal renderers
        :param app: a running application
        :param transport: the A2UI message transport
        :param config: optional A2UI surface and envelope configuration
        :param verbose: log the agent lifecycle to stderr
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
            AgentRuntime(app, transport, container.get(A2UIConfig), verbose=verbose).run()

    def _resolve_agent_transport(self) -> Transport:
        """Private. Builds the agent transport selected via `argenta run` flags"""
        config = self._runner_config
        if os.getenv(config.a2ui_transport_env_var) == config.a2ui_ws_transport:
            port_raw = os.getenv(config.a2ui_ws_port_env_var)
            port = int(port_raw) if port_raw else config.a2ui_ws_default_port
            verbose = bool(os.getenv(config.a2ui_verbose_env_var))
            return self._build_ws_transport(config.a2ui_ws_default_host, port, verbose)
        return StdioTransport()

    def _build_ws_transport(self, host: str, port: int, verbose: bool) -> Transport:
        """Private. Builds the WebSocket transport; `websockets` is an optional
        dependency, so the module is imported only when ws mode is requested"""
        try:
            from argenta.a2ui.transport.websocket import WebSocketTransport
        except ImportError as error:
            raise RuntimeError(
                "A2UI WebSocket transport requires the 'websockets' package: "
                "pip install 'argenta[a2ui]'"
            ) from error
        return WebSocketTransport(host=host, port=port, verbose=verbose)
