__all__ = ["run_handler"]

import os

from rich.console import Console

from ..infrastructure.entrypoint_resolver.entity import (
    CallableEntryPoint,
    EntrypointResolver,
)
from ..infrastructure.entrypoint_resolver.exceptions import (
    EntrypointError,
    ResolveFromStringError,
)


def run_handler(entrypoint_path: str) -> None:
    os.environ["RUN_FROM_ARGENTA_RUNNER"] = "1"
    file_path, _, callable_name = entrypoint_path.partition(":")
    if not callable_name:
        Console().print(
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
        Console().print(f"[bold red]Error:[/bold red] {e}")
        raise SystemExit(1)
