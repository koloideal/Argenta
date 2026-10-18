"""Runs the same application as a terminal REPL or as an A2UI agent.

uv run python -m dual_runtime.main repl
uv run python -m dual_runtime.main agent [sse | ws]
"""

import sys
from typing import Final

from argenta import Orchestrator
from argenta.a2ui import A2UIConfig
from argenta.a2ui.transport import SSETransport, Transport
from argenta.repl import REPLConfig, StaticDividingLine
from dual_runtime.app import build_app
from dual_runtime.routers import inventory_router

_USAGE: Final = "usage: python -m dual_runtime.main [repl | agent [sse | ws]]"

_CARDS_PER_ROW: Final = 3
_MAX_LOG_ENTRIES: Final = 50

_agent_config = A2UIConfig(
    cards_per_row=_CARDS_PER_ROW,
    max_log_entries=_MAX_LOG_ENTRIES,
    theme={
        "primaryColor": "#7c3aed",
        "backgroundColor": "#111827",
        "fontFamily": "JetBrains Mono, monospace",
    },
)

_repl_config = REPLConfig(dividing_line=StaticDividingLine("-"))


def _make_transport(name: str) -> Transport:
    if name == "ws":
        from argenta.a2ui.transport.websocket import WebSocketTransport

        return WebSocketTransport(verbose=True)
    return SSETransport(verbose=True)


def _run_repl() -> None:
    app = build_app(plain=False)
    app.include_router(inventory_router)
    Orchestrator().run_repl(app, _repl_config)


def _run_agent(transport_name: str) -> None:
    app = build_app(plain=True)
    app.include_router(inventory_router)
    Orchestrator().run_agent(app, _make_transport(transport_name), _agent_config, verbose=True)


def _agent_transport_name(argv: list[str]) -> str:
    name = argv[1] if len(argv) > 1 else "sse"
    if name not in {"sse", "ws"}:
        sys.exit(_USAGE)
    return name


def main(argv: list[str]) -> None:
    mode = argv[0] if argv else "repl"
    if mode == "repl":
        _run_repl()
    elif mode == "agent":
        _run_agent(_agent_transport_name(argv))
    else:
        sys.exit(_USAGE)


if __name__ == "__main__":
    main(sys.argv[1:])
