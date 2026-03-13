__all__ = ["init_handler"]

from pathlib import Path
from typing import Literal

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
def start_handler(response: Response):
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

router.command('hello')(hello_handler)
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


def init_handler(with_arch: Literal["flat", "src"] = "flat") -> None:
    cwd = Path.cwd()
    project_name = cwd.name.lower().replace(" ", "_")

    create_file(cwd / ".gitignore", GITIGNORE_CONTENT)

    if with_arch == "flat":
        create_file(cwd / "main.py", FLAT_MAIN_TEMPLATE)
        create_file(cwd / "handlers.py", FLAT_HANDLERS_TEMPLATE)

    elif with_arch == "src":
        base_pkg = cwd / "src" / project_name / "application"

        create_file(base_pkg / "__main__.py", SRC_MAIN_TEMPLATE)
        create_file(base_pkg / "routers.py", SRC_ROUTERS_TEMPLATE)
        create_file(base_pkg / "handlers" / "hello_world_handler.py", SRC_HANDLER_TEMPLATE)

        create_file(cwd / "src" / "__init__.py", "")
        create_file(cwd / "src" / project_name / "__init__.py", "")
        create_file(base_pkg / "__init__.py", "")
        create_file(base_pkg / "handlers" / "__init__.py", "")

    print("\nInitialization complete.")
