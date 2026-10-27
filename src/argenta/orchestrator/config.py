from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RunnerConfig:
    """
    Environment bridge between the `argenta` CLI commands and the Orchestrator:
    the CLI sets these variables and the Orchestrator reads them
    """

    runner_env_var: str = "RUN_FROM_ARGENTA_RUNNER"
    mode_env_var: str = "ARGENTA_RUN_MODE"
    a2ui_mode: str = "a2ui"
    a2ui_transport_env_var: str = "ARGENTA_A2UI_TRANSPORT"
    a2ui_ws_transport: str = "ws"
    a2ui_sse_transport: str = "sse"
    a2ui_socket_transport: str = "socket"
    a2ui_poll_transport: str = "poll"
    a2ui_grpc_transport: str = "grpc"
    a2ui_socket_path_env_var: str = "ARGENTA_A2UI_SOCKET_PATH"
    a2ui_port_env_var: str = "ARGENTA_A2UI_PORT"
    a2ui_default_host: str = "127.0.0.1"
    a2ui_default_port: int = 8765
    a2ui_verbose_env_var: str = "ARGENTA_A2UI_VERBOSE"
    a2ui_grpc_stop_timeout: float = 10
