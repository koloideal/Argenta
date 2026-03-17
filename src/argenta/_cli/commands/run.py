__all__ = ["run_handler"]

import os

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
            "Path to callable object that run orchestrator repl must be in the format <path/to/file.py>:<object_name> or <path.to.module>:<object_name>"
        )

    runner = EntrypointResolver[CallableEntryPoint](entrypoint_path).parse_entrypoint_with_type(
        entrypoint_callable_name
    )

    runner.instance_object()
