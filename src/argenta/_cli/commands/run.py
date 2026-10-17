import os

from dishka import Container
from rich.console import Console

from argenta._cli.commands._entrypoint import (
    resolve_callable_entrypoint,
    split_entrypoint_spec,
)
from argenta.orchestrator.entity import RunnerConfig


def run_handler(
    container: Container,
    entrypoint_path: str,
    *,
    a2ui: bool,
    a2ui_transport: str = "stdio",
    a2ui_port: int | None = None,
) -> None:
    runner_config = container.get(RunnerConfig)
    os.environ[runner_config.runner_env_var] = "1"
    if a2ui:
        os.environ[runner_config.mode_env_var] = runner_config.a2ui_mode
        os.environ[runner_config.a2ui_transport_env_var] = a2ui_transport
        if a2ui_port is not None:
            os.environ[runner_config.a2ui_ws_port_env_var] = str(a2ui_port)
    console = container.get(Console)
    spec = split_entrypoint_spec(
        entrypoint_path,
        console,
        format_hint='"<path/to/file.py>:<callable>" or "<path.to.module>:<callable>"',
    )
    resolve_callable_entrypoint(spec, console).instance_object()
