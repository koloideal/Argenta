"""Compact REPL: no dividing line, no gaps, plain system messages.

uv run python -m repl_compact.main
"""

from typing import Final

from argenta import App, Orchestrator
from argenta.repl import REPLConfig
from repl_compact.routers import notes_router

_NO_GAP: Final = 0

app: App = App(
    initial_message="Notes",
    farewell_message="Saved",
    prompt="notes> ",
    override_system_messages=True,
    printer=print,
)
orchestrator: Orchestrator = Orchestrator()

_layout = REPLConfig(
    dividing_line=None,
    prompt_gap=_NO_GAP,
    frame_padding=_NO_GAP,
    startup_messages_gap=_NO_GAP,
    command_groups_gap=_NO_GAP,
)


def main() -> None:
    app.include_router(notes_router)
    orchestrator.run_repl(app, _layout)


if __name__ == "__main__":
    main()
