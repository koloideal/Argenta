"""Framed REPL: every output is boxed by a dynamic dividing line.

uv run python -m repl_framed.main
"""

from typing import Final

from argenta import App, Orchestrator
from argenta.repl import DynamicDividingLine, REPLConfig
from repl_framed.routers import admin_router, ops_router

_FRAME_PADDING: Final = 2
_COMMAND_GROUPS_GAP: Final = 3

app: App = App(
    initial_message="Ops Deck",
    prompt="ops> ",
    farewell_message="All services left running",
)
orchestrator: Orchestrator = Orchestrator()

_layout = REPLConfig(
    dividing_line=DynamicDividingLine("="),
    prompt_gap=1,
    frame_padding=_FRAME_PADDING,
    startup_messages_gap=1,
    command_groups_gap=_COMMAND_GROUPS_GAP,
)


def main() -> None:
    app.include_routers(ops_router, admin_router)
    orchestrator.run_repl(app, _layout)


if __name__ == "__main__":
    main()
