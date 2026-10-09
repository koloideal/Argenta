import os

from dishka import Container
from rich.console import Console

from argenta._cli.commands._entrypoint import (
    resolve_callable_entrypoint,
    split_entrypoint_spec,
)


def run_handler(container: Container, entrypoint_path: str) -> None:
    os.environ["RUN_FROM_ARGENTA_RUNNER"] = "1"
    console = container.get(Console)
    spec = split_entrypoint_spec(
        entrypoint_path,
        console,
        format_hint='"<path/to/file.py>:<callable>" or "<path.to.module>:<callable>"',
    )
    resolve_callable_entrypoint(spec, console).instance_object()
