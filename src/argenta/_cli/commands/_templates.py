__all__ = [
    "GITIGNORE_CONTENT",
    "FLAT_MAIN_TEMPLATE",
    "FLAT_HANDLERS_TEMPLATE",
    "SRC_MAIN_TEMPLATE",
    "SRC_ROUTERS_TEMPLATE",
    "SRC_HANDLER_TEMPLATE",
    "create_file",
]

from pathlib import Path

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


def create_file(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip(), encoding="utf-8")
    else:
        print(f"Skipped: {path} (already exists)")
