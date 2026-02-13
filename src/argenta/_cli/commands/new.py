__all__ = ["new_handler"]

import sys
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


def new_handler(project_name: str, with_arch: Literal["flat", "src"] = "flat") -> None:
    base_dir = Path.cwd() / project_name

    if base_dir.exists():
        print(f"Error: Directory '{project_name}' already exists.")
        sys.exit(1)

    base_dir.mkdir(parents=True)
    print(f"Initialized project directory: {base_dir}")

    create_file(base_dir / ".gitignore", GITIGNORE_CONTENT)

    if with_arch == "flat":
        create_file(base_dir / "main.py", FLAT_MAIN_TEMPLATE)
        create_file(base_dir / "handlers.py", FLAT_HANDLERS_TEMPLATE)

    elif with_arch == "src":
        pkg_name = project_name.lower().replace(" ", "_").replace("-", "_")
        app_pkg = base_dir / "src" / pkg_name / "application"

        create_file(app_pkg / "__main__.py", SRC_MAIN_TEMPLATE)
        create_file(app_pkg / "routers.py", SRC_ROUTERS_TEMPLATE)
        create_file(app_pkg / "handlers" / "hello_world_handler.py", SRC_HANDLER_TEMPLATE)

        create_file(base_dir / "src" / "__init__.py", "")
        create_file(base_dir / "src" / pkg_name / "__init__.py", "")
        create_file(app_pkg / "__init__.py", "")
        create_file(app_pkg / "handlers" / "__init__.py", "")

    print(f"\nProject '{project_name}' created successfully! 🚀")
