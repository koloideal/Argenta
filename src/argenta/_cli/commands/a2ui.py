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
from argenta.orchestrator.config import RunnerConfig


@dataclass(frozen=True, slots=True)
class A2UIRunOptions:
    """Private. Options of the `argenta a2ui` command"""

    transport: str = "sse"
    port: int | None = None
    socket_path: str | None = None
    verbose: bool = False
    hot_reload: bool = False


def _has_module(name: str) -> bool:
    """Private. find_spec raises ModuleNotFoundError for missing
    parents of dotted names (e.g. `google.protobuf`)"""
    try:
        return find_spec(name) is not None
    except ModuleNotFoundError:
        return False


def _ensure_transport_modules(console: Console, transport: str) -> None:
    """Private. ws/grpc need optional dependencies; the other transports
    are standard-library only"""
    modules = {"ws": ("websockets",), "grpc": ("grpc", "google.protobuf")}
    missing = [name for name in modules.get(transport, ()) if not _has_module(name)]
    if missing:
        missing_report = ", ".join(missing)
        console.print(
            f"[bold red]Error:[/bold red] the '{transport}' transport is missing "
            f"optional modules: {missing_report} — "
            r"install them with `uv add 'argenta\[a2ui]'`"
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
    _ensure_transport_modules(console, options.transport)
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
