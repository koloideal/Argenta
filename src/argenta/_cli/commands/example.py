import sys
from contextlib import suppress
from dataclasses import dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from dishka import Container
from rich.console import Console

from argenta._cli.commands._entrypoint import (
    resolve_callable_entrypoint,
    split_entrypoint_spec,
)
from argenta._cli.commands.a2ui import A2UIRunOptions, _ensure_transport_modules, a2ui_handler
from argenta._cli.commands.repl import ReplRunOptions, repl_handler

_EXAMPLES_ROOT = Path("examples")
_REPL_ENTRYPOINT = "examples/repl/app/main.py:main"
_AGENT_ENTRYPOINT = "examples/a2ui/agent.py:main"
_GRPC_CLIENT_ENTRYPOINT = "examples/a2ui/grpc_client.py:main"
_LIT_CLIENT_DIR = _EXAMPLES_ROOT / "a2ui" / "lit_client"
_LIT_CLIENT_HOST = "127.0.0.1"
_LIT_CLIENT_PORT = 8080


@dataclass(frozen=True, slots=True)
class ExampleOptions:
    """Private. Options of the `argenta example` command"""

    target: str | None
    client_kind: str | None
    transport: str = "sse"


def _require_examples(console: Console) -> None:
    """Private. The bundled examples are not shipped with the package;
    `argenta example` runs them from an Argenta checkout"""
    if not _EXAMPLES_ROOT.is_dir():
        console.print(
            "[bold red]Error:[/bold red] no `examples` directory here — "
            "run `argenta example` from an Argenta repository checkout"
        )
        sys.exit(1)


def _ensure_bare_repl(console: Console, options: ExampleOptions) -> None:
    """Private. `argenta example repl` accepts no further positionals"""
    if options.target or options.client_kind:
        console.print("[bold red]Error:[/bold red] 'repl' accepts no further arguments")
        sys.exit(1)


def _serve_lit_client(console: Console) -> None:
    """Private. Serves the bundled Lit client over local HTTP;
    the agent side is `argenta example a2ui agent`"""
    request_handler = partial(SimpleHTTPRequestHandler, directory=str(_LIT_CLIENT_DIR))
    url = f"http://{_LIT_CLIENT_HOST}:{_LIT_CLIENT_PORT}"
    console.print(f"serving the Lit client on {url} — Ctrl+C to stop")
    address = (_LIT_CLIENT_HOST, _LIT_CLIENT_PORT)
    with suppress(KeyboardInterrupt), ThreadingHTTPServer(address, request_handler) as server:
        server.serve_forever()


def _run_grpc_client(console: Console) -> None:
    """Private. The terminal gRPC client needs the a2ui extra"""
    _ensure_transport_modules(console, "grpc")
    spec = split_entrypoint_spec(
        _GRPC_CLIENT_ENTRYPOINT,
        console,
        format_hint='"<path/to/file.py>:<callable>" or "<path.to.module>:<callable>"',
    )
    resolve_callable_entrypoint(spec, console).instance_object()


def _run_client(console: Console, client_kind: str | None) -> None:
    """Private. Client side: the Lit browser app or the terminal gRPC client"""
    if client_kind == "grpc":
        _run_grpc_client(console)
        return
    _serve_lit_client(console)


def example_handler(container: Container, kind: str, options: ExampleOptions) -> None:
    console = container.get(Console)
    _require_examples(console)
    if kind == "repl":
        _ensure_bare_repl(console, options)
        repl_handler(container, _REPL_ENTRYPOINT, ReplRunOptions())
        return
    if options.target == "agent":
        if options.client_kind:
            console.print(
                "[bold red]Error:[/bold red] the a2ui agent accepts no client kind argument"
            )
            sys.exit(1)
        a2ui_handler(
            container,
            _AGENT_ENTRYPOINT,
            A2UIRunOptions(transport=options.transport, verbose=True),
        )
        return
    if options.target == "client":
        _run_client(console, options.client_kind)
        return
    console.print("[bold red]Error:[/bold red] 'a2ui' requires a target: 'agent' or 'client'")
    sys.exit(1)
