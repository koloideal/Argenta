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
class A2UIRunOptions:
    """Private. Options of the `argenta a2ui` command"""

    transport: str = "ws"
    port: int | None = None
    socket_path: str | None = None
    verbose: bool = False
    hot_reload: bool = False


def _ensure_a2ui_extra(console: Console) -> None:
    """Private. The a2ui command needs the optional extra installed"""
    missing = [pkg for pkg in ("websockets", "watchfiles") if find_spec(pkg) is None]
    if missing:
        missing_report = ", ".join(missing)
        console.print(
            "[bold red]Error:[/bold red] the a2ui command requires optional "
            f"dependencies (missing: {missing_report}) — "
            r"install them with `pip install 'argenta\[a2ui]'`"
        )
        sys.exit(1)


def _child_args(entrypoint_path: str, options: A2UIRunOptions) -> list[str]:
    args = [sys.executable, "-m", "argenta._cli", "a2ui", "--transport", options.transport]
    if options.port is not None:
        args += ["--port", str(options.port)]
    if options.socket_path is not None:
        args += ["--socket-path", options.socket_path]
    if options.verbose:
        args += ["--verbose"]
    args.append(entrypoint_path)
    return args


def _reload_supervised(
    spec_path: str, entrypoint_path: str, options: A2UIRunOptions, console: Console
) -> None:
    watch_root = resolve_watch_root(spec_path)
    if watch_root is None:
        console.print(
            "[bold red]Error:[/bold red] cannot resolve a directory to watch for --reload"
        )
        sys.exit(1)
    stderr = Console(stderr=True)
    stderr.print(f"a2ui: watching {watch_root} for changes")
    sys.exit(supervise_cli(_child_args(entrypoint_path, options), watch_root, stderr, "a2ui"))


def a2ui_handler(container: Container, entrypoint_path: str, options: A2UIRunOptions) -> None:
    console = container.get(Console)
    _ensure_a2ui_extra(console)
    spec = split_entrypoint_spec(
        entrypoint_path,
        console,
        format_hint='"<path/to/file.py>:<callable>" or "<path.to.module>:<callable>"',
    )
    if options.hot_reload:
        _reload_supervised(spec.file_path, entrypoint_path, options, console)
    runner_config = container.get(RunnerConfig)
    os.environ[runner_config.runner_env_var] = "1"
    os.environ[runner_config.mode_env_var] = runner_config.a2ui_mode
    os.environ[runner_config.a2ui_transport_env_var] = options.transport
    if options.port is not None:
        os.environ[runner_config.a2ui_port_env_var] = str(options.port)
    if options.socket_path is not None:
        os.environ[runner_config.a2ui_socket_path_env_var] = options.socket_path
    if options.verbose:
        os.environ[runner_config.a2ui_verbose_env_var] = "1"
    resolve_callable_entrypoint(spec, console).instance_object()
