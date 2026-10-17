import os

from dishka import Container
from rich.console import Console

from argenta._cli.commands._entrypoint import (
    resolve_callable_entrypoint,
    split_entrypoint_spec,
)
from argenta.orchestrator.entity import RunnerConfig


def run_handler(container: Container, entrypoint_path: str) -> None:
    runner_config = container.get(RunnerConfig)
    os.environ[runner_config.runner_env_var] = "1"
    console = container.get(Console)
    spec = split_entrypoint_spec(
        entrypoint_path,
        console,
        format_hint='"<path/to/file.py>:<callable>" or "<path.to.module>:<callable>"',
    )
    resolve_callable_entrypoint(spec, console).instance_object()
