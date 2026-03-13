__all__ = ["run_handler"]

import os
from pathlib import Path
import sys

from ..infrastructure.entrypoint_resolver.entity import (
    CallableEntryPoint,
    EntrypointResolver,
    ResolveFromStringError,
)


def run_handler(entrypoint_path: str) -> None:
    os.environ["RUN_FROM_ARGENTA_RUNNER"] = "1"
    entrypoint_path, _, entrypoint_callable_name = entrypoint_path.partition(":")
    if not entrypoint_callable_name:
        raise ResolveFromStringError(
            "Path to callable object that run orchestrator repl must be in the format <path/to/file.py>:<object_name>"
        )
        
    if str(Path.cwd()) not in sys.path:
        sys.path.insert(0, str(Path.cwd()))

    runner = EntrypointResolver(entrypoint_path).parse_entrypoint_with_type(
        entrypoint_callable_name, CallableEntryPoint
    )

    runner.instance_object()
