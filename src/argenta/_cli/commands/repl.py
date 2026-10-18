import os
import sys
from dataclasses import dataclass
from importlib.util import find_spec

from dishka import Container
from rich.console import Console

from argenta._cli.commands._entrypoint import (
    resolve_callable_entrypoint,
    split_entrypoint_spec,
)
from argenta._cli.commands._reload import resolve_watch_root, supervise_cli
from argenta.orchestrator.entity import RunnerConfig


@dataclass(frozen=True, slots=True)
class ReplRunOptions:
    """Private. Options of the `argenta repl` command"""

    hot_reload: bool = False


def _ensure_watchfiles(console: Console) -> None:
    """Private. The --reload option watches python files via watchfiles"""
    if find_spec("watchfiles") is None:
        console.print(
            "[bold red]Error:[/bold red] --reload requires the optional "
            "'watchfiles' dependency — install it with `pip install watchfiles` "
            r"or `pip install 'argenta\[cli]'`"
        )
        sys.exit(1)


def _child_args(entrypoint_path: str) -> list[str]:
    return [sys.executable, "-m", "argenta._cli", "repl", entrypoint_path]


def _reload_supervised(spec_path: str, entrypoint_path: str, console: Console) -> None:
    watch_root = resolve_watch_root(spec_path)
    if watch_root is None:
        console.print(
            "[bold red]Error:[/bold red] cannot resolve a directory to watch for --reload"
        )
        sys.exit(1)
    stderr = Console(stderr=True)
    stderr.print(f"repl: watching {watch_root} for changes")
    sys.exit(supervise_cli(_child_args(entrypoint_path), watch_root, stderr, "repl"))


def repl_handler(container: Container, entrypoint_path: str, options: ReplRunOptions) -> None:
    console = container.get(Console)
    spec = split_entrypoint_spec(
        entrypoint_path,
        console,
        format_hint='"<path/to/file.py>:<callable>" or "<path.to.module>:<callable>"',
    )
    if options.hot_reload:
        _ensure_watchfiles(console)
        _reload_supervised(spec.file_path, entrypoint_path, console)
    runner_config = container.get(RunnerConfig)
    os.environ[runner_config.runner_env_var] = "1"
    resolve_callable_entrypoint(spec, console).instance_object()
