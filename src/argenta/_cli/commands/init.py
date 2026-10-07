__all__ = ["init_handler"]

from pathlib import Path
from typing import Literal

from dishka import Container
from rich.console import Console

from argenta._cli.commands._templates import (
    FLAT_HANDLERS_TEMPLATE,
    FLAT_MAIN_TEMPLATE,
    GITIGNORE_CONTENT,
    SRC_HANDLER_TEMPLATE,
    SRC_MAIN_TEMPLATE,
    SRC_ROUTERS_TEMPLATE,
    create_file,
    sanitize_package_name,
)


def init_handler(container: Container, arch: Literal["flat", "src"] = "flat") -> None:
    console = container.get(Console)
    cwd = Path.cwd()
    project_name = sanitize_package_name(cwd.name)

    if arch == "src" and not project_name.isidentifier():
        console.print(
            f"[bold red]Error:[/bold red] cannot derive a valid package name "
            f'from directory "{cwd.name}"'
        )
        raise SystemExit(1)

    create_file(cwd / ".gitignore", GITIGNORE_CONTENT, console)

    if arch == "flat":
        create_file(cwd / "main.py", FLAT_MAIN_TEMPLATE, console)
        create_file(cwd / "handlers.py", FLAT_HANDLERS_TEMPLATE, console)

    elif arch == "src":
        base_pkg = cwd / "src" / project_name / "application"

        create_file(base_pkg / "__main__.py", SRC_MAIN_TEMPLATE, console)
        create_file(base_pkg / "routers.py", SRC_ROUTERS_TEMPLATE, console)
        create_file(base_pkg / "handlers" / "hello_world_handler.py", SRC_HANDLER_TEMPLATE, console)

        create_file(cwd / "src" / "__init__.py", "", console)
        create_file(cwd / "src" / project_name / "__init__.py", "", console)
        create_file(base_pkg / "__init__.py", "", console)
        create_file(base_pkg / "handlers" / "__init__.py", "", console)

    console.print("\nInitialization complete.")
