__all__ = ["new_handler"]

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


def new_handler(
    container: Container, project_name: str, arch: Literal["flat", "src"] = "flat"
) -> None:
    console = container.get(Console)

    if project_name in (".", "..") or "/" in project_name or "\\" in project_name:
        console.print(f'[bold red]Error:[/bold red] "{project_name}" is not a valid project name')
        raise SystemExit(1)

    base_dir = Path.cwd() / project_name

    if base_dir.exists():
        console.print(f"[bold red]Error:[/bold red] Directory '{project_name}' already exists.")
        raise SystemExit(1)

    pkg_name = sanitize_package_name(project_name)
    if arch == "src" and not pkg_name.isidentifier():
        console.print(
            f'[bold red]Error:[/bold red] cannot derive a valid package name from "{project_name}"'
        )
        raise SystemExit(1)

    base_dir.mkdir()
    console.print(f"Initialized project directory: {base_dir}")

    create_file(base_dir / ".gitignore", GITIGNORE_CONTENT, console)

    if arch == "flat":
        create_file(base_dir / "main.py", FLAT_MAIN_TEMPLATE, console)
        create_file(base_dir / "handlers.py", FLAT_HANDLERS_TEMPLATE, console)

    elif arch == "src":
        app_pkg = base_dir / "src" / pkg_name / "application"

        create_file(app_pkg / "__main__.py", SRC_MAIN_TEMPLATE, console)
        create_file(app_pkg / "routers.py", SRC_ROUTERS_TEMPLATE, console)
        create_file(app_pkg / "handlers" / "hello_world_handler.py", SRC_HANDLER_TEMPLATE, console)

        create_file(base_dir / "src" / "__init__.py", "", console)
        create_file(base_dir / "src" / pkg_name / "__init__.py", "", console)
        create_file(app_pkg / "__init__.py", "", console)
        create_file(app_pkg / "handlers" / "__init__.py", "", console)

    console.print(f"\nProject '{project_name}' created successfully! 🚀")
