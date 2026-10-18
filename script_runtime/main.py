"""Replays session.txt of the inventory app into a markdown transcript.

uv run python -m script_runtime.main > transcript.md
"""

import sys
from pathlib import Path
from typing import Final

from dual_runtime.app import build_app
from dual_runtime.routers import inventory_router
from script_runtime.layout import MarkdownLayout
from script_runtime.runtime import ScriptRuntime

_SCRIPT_PATH: Final = Path(__file__).parent / "session.txt"


def main() -> None:
    app = build_app(plain=True)
    app.include_router(inventory_router)
    ScriptRuntime(app, MarkdownLayout(sys.stdout)).run(_SCRIPT_PATH)


if __name__ == "__main__":
    main()
