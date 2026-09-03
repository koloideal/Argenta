__all__ = ["new_handler"]

import sys
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


def new_handler(project_name: str, arch: Literal["flat", "src"] = "flat") -> None:
    base_dir = Path.cwd() / project_name

    if base_dir.exists():
        print(f"Error: Directory '{project_name}' already exists.")
        raise SystemExit(1)

    base_dir.mkdir(parents=True)
    print(f"Initialized project directory: {base_dir}")

    create_file(base_dir / ".gitignore", GITIGNORE_CONTENT)

    if arch == "flat":
        create_file(base_dir / "main.py", FLAT_MAIN_TEMPLATE)
        create_file(base_dir / "handlers.py", FLAT_HANDLERS_TEMPLATE)

    elif arch == "src":
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
