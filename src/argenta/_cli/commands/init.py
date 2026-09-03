__all__ = ["init_handler"]

from pathlib import Path
from typing import Literal

from ._templates import (
    FLAT_HANDLERS_TEMPLATE,
    FLAT_MAIN_TEMPLATE,
    GITIGNORE_CONTENT,
    SRC_HANDLER_TEMPLATE,
    SRC_MAIN_TEMPLATE,
    SRC_ROUTERS_TEMPLATE,
    create_file,
)


def init_handler(arch: Literal["flat", "src"] = "flat") -> None:
    cwd = Path.cwd()
    project_name = cwd.name.lower().replace(" ", "_")

    create_file(cwd / ".gitignore", GITIGNORE_CONTENT)

    if arch == "flat":
        create_file(cwd / "main.py", FLAT_MAIN_TEMPLATE)
        create_file(cwd / "handlers.py", FLAT_HANDLERS_TEMPLATE)

    elif arch == "src":
        base_pkg = cwd / "src" / project_name / "application"

        create_file(base_pkg / "__main__.py", SRC_MAIN_TEMPLATE)
        create_file(base_pkg / "routers.py", SRC_ROUTERS_TEMPLATE)
        create_file(base_pkg / "handlers" / "hello_world_handler.py", SRC_HANDLER_TEMPLATE)

        create_file(cwd / "src" / "__init__.py", "")
        create_file(cwd / "src" / project_name / "__init__.py", "")
        create_file(base_pkg / "__init__.py", "")
        create_file(base_pkg / "handlers" / "__init__.py", "")

    print("\nInitialization complete.")
