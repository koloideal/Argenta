import os
from collections.abc import Callable

from argenta.a2ui import (
    LongPollTransport,
    SocketTransport,
    SSETransport,
    StdioTransport,
    Transport,
)
from argenta.orchestrator.config import RunnerConfig


def _build_ws_transport(host: str, port: int, verbose: bool) -> Transport:
    """Private. Builds the WebSocket transport; `websockets` is an optional
    dependency, so the module is imported only when ws mode is requested"""
    try:
        from argenta.a2ui.transport.websocket import WebSocketTransport
    except ImportError as error:
        raise RuntimeError(
            "A2UI WebSocket transport requires the 'websockets' package: uv add 'argenta[a2ui]'"
        ) from error
    return WebSocketTransport(host=host, port=port, verbose=verbose)


def _build_grpc_transport(config: RunnerConfig, port: int, verbose: bool) -> Transport:
    """Private. Builds the gRPC transport; `grpcio` is an optional
    dependency, so the module is imported only when grpc mode is requested"""
    try:
        from argenta.a2ui.transport.grpc import GrpcTransport
    except ImportError as error:
        raise RuntimeError(
            "A2UI gRPC transport requires the 'grpcio' and 'protobuf' packages: "
            "uv add 'argenta[a2ui]'"
        ) from error
    return GrpcTransport(
        host=config.a2ui_default_host,
        port=port,
        stop_timeout=config.a2ui_grpc_stop_timeout,
        verbose=verbose,
    )


def _server_port(config: RunnerConfig) -> int:
    """Private. Port for the network transports, env override or default"""
    port_raw = os.getenv(config.a2ui_port_env_var)
    return int(port_raw) if port_raw else config.a2ui_default_port


def _transport_builders(
    config: RunnerConfig, port: int, verbose: bool
) -> dict[str, Callable[[], Transport]]:
    """Private. Transport factories keyed by their `--transport` names;
    only the selected one is instantiated"""
    host = config.a2ui_default_host
    return {
        config.a2ui_ws_transport: lambda: _build_ws_transport(host, port, verbose),
        config.a2ui_sse_transport: lambda: SSETransport(host=host, port=port, verbose=verbose),
        config.a2ui_socket_transport: lambda: SocketTransport(
            host=host,
            port=port,
            path=os.getenv(config.a2ui_socket_path_env_var),
            verbose=verbose,
        ),
        config.a2ui_poll_transport: lambda: LongPollTransport(
            host=host, port=port, verbose=verbose
        ),
        config.a2ui_grpc_transport: lambda: _build_grpc_transport(config, port, verbose),
    }


def resolve_agent_transport(config: RunnerConfig) -> Transport:
    """Private. Builds the agent transport selected via `argenta a2ui` flags;
    unknown or missing names fall back to the stdio transport"""
    verbose = bool(os.getenv(config.a2ui_verbose_env_var))
    transport_name = os.getenv(config.a2ui_transport_env_var)
    builders = _transport_builders(config, _server_port(config), verbose)
    builder = builders.get(transport_name or "")
    if builder is None:
        return StdioTransport(verbose=verbose)
    return builder()
