__all__ = ["run_handler"]

import os

from dishka import Container
from rich.console import Console

from argenta._cli.infrastructure.entrypoint_resolver.entity import (
    CallableEntryPoint,
    EntrypointResolver,
)
from argenta._cli.infrastructure.entrypoint_resolver.exceptions import (
    EntrypointError,
    ResolveFromStringError,
)


def run_handler(container: Container, entrypoint_path: str) -> None:
    os.environ["RUN_FROM_ARGENTA_RUNNER"] = "1"
    console = container.get(Console)
    file_path, sep, callable_name = entrypoint_path.rpartition(":")
    if not sep or not file_path or not callable_name:
        console.print(
            f'[bold red]Error:[/bold red] "{entrypoint_path}" must be in format '
            f'"<path/to/file.py>:<callable>" or "<path.to.module>:<callable>"'
        )
        raise SystemExit(1)

    try:
        runner = EntrypointResolver[CallableEntryPoint](file_path).parse_entrypoint_with_type(
            callable_name
        )
        runner.instance_object()
    except (ResolveFromStringError, EntrypointError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise SystemExit(1)
