import sys
from dataclasses import dataclass
from typing import NoReturn

from rich.console import Console

from argenta._cli.infrastructure.entrypoint_resolver.entity import (
    CallableEntryPoint,
    EntrypointResolver,
)
from argenta._cli.infrastructure.entrypoint_resolver.exceptions import (
    EntrypointError,
    ResolveFromStringError,
)


@dataclass(frozen=True, slots=True)
class EntrypointSpec:
    file_path: str
    callable_name: str


def split_entrypoint_spec(entrypoint: str, console: Console, *, format_hint: str) -> EntrypointSpec:
    file_path, sep, callable_name = entrypoint.rpartition(":")
    if not sep or not file_path or not callable_name:
        console.print(f'[bold red]Error:[/bold red] "{entrypoint}" must be in format {format_hint}')
        sys.exit(1)
    return EntrypointSpec(file_path, callable_name)


def resolve_callable_entrypoint(spec: EntrypointSpec, console: Console) -> CallableEntryPoint:
    try:
        return EntrypointResolver[CallableEntryPoint](spec.file_path).parse_entrypoint_with_type(
            spec.callable_name
        )
    except (ResolveFromStringError, EntrypointError) as error:
        report_entrypoint_error(console, error)


def report_entrypoint_error(
    console: Console, error: ResolveFromStringError | EntrypointError
) -> NoReturn:
    console.print(f"[bold red]Error:[/bold red] {error}")
    sys.exit(1)
