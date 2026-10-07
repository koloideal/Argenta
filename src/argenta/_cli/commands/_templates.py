__all__ = [
    "FLAT_HANDLERS_TEMPLATE",
    "FLAT_MAIN_TEMPLATE",
    "GITIGNORE_CONTENT",
    "SRC_HANDLER_TEMPLATE",
    "SRC_MAIN_TEMPLATE",
    "SRC_ROUTERS_TEMPLATE",
    "create_file",
    "sanitize_package_name",
]

from pathlib import Path

from rich.console import Console

GITIGNORE_CONTENT = """
__pycache__/
*.py[cod]
.env
.venv/
env/
"""

FLAT_MAIN_TEMPLATE = """
from argenta import Orchestrator, App

from handlers import router


def main():
    app = App()
    app.include_router(router)

    orchestrator = Orchestrator()
    orchestrator.run_repl(app)

if __name__ == "__main__":
    main()
"""

FLAT_HANDLERS_TEMPLATE = """
from argenta import Router, Response

router = Router("Hello command")

@router.command("hello")
def hello_handler(response: Response):
    print("Hello world!")
"""

SRC_MAIN_TEMPLATE = """
from argenta import Orchestrator, App

from .routers import router


def main():
    app = App()
    app.include_router(router)

    orchestrator = Orchestrator()
    orchestrator.run_repl(app)

if __name__ == "__main__":
    main()
"""

SRC_ROUTERS_TEMPLATE = """
from argenta import Router
from .handlers.hello_world_handler import hello_handler

router = Router()

router.command("hello")(hello_handler)
"""

SRC_HANDLER_TEMPLATE = """
from argenta import Response


def hello_handler(response: Response) -> None:
    print("Hello world!")
"""


def sanitize_package_name(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_")


def create_file(path: Path, content: str, console: Console) -> None:
    if path.exists():
        console.print(f"[yellow]Skipped:[/yellow] {path} (already exists)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    stripped = content.strip()
    path.write_text(stripped + "\n" if stripped else "", encoding="utf-8")
