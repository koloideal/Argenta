import sys
from pathlib import Path
from typing import Literal

from dishka import Container
from rich.console import Console

from argenta._cli.commands._scaffold import create_file, sanitize_package_name
from argenta._cli.commands._templates import (
    FLAT_HANDLERS_TEMPLATE,
    FLAT_MAIN_TEMPLATE,
    GITIGNORE_CONTENT,
    INIT_FILE_NAME,
    SRC_DIR_NAME,
    SRC_HANDLER_TEMPLATE,
    SRC_MAIN_TEMPLATE,
    SRC_ROUTERS_TEMPLATE,
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
        sys.exit(1)

    create_file(cwd / ".gitignore", GITIGNORE_CONTENT, console)

    if arch == "flat":
        _create_flat_layout(cwd, console)
    elif arch == "src":
        _create_src_layout(cwd, project_name, console)

    console.print("\nInitialization complete.")


def _create_flat_layout(base_dir: Path, console: Console) -> None:
    create_file(base_dir / "main.py", FLAT_MAIN_TEMPLATE, console)
    create_file(base_dir / "handlers.py", FLAT_HANDLERS_TEMPLATE, console)


def _create_src_layout(base_dir: Path, project_name: str, console: Console) -> None:
    base_pkg = base_dir / SRC_DIR_NAME / project_name / "application"

    create_file(base_pkg / "__main__.py", SRC_MAIN_TEMPLATE, console)
    create_file(base_pkg / "routers.py", SRC_ROUTERS_TEMPLATE, console)
    create_file(base_pkg / "handlers" / "hello_world_handler.py", SRC_HANDLER_TEMPLATE, console)

    create_file(base_dir / SRC_DIR_NAME / INIT_FILE_NAME, "", console)
    create_file(base_dir / SRC_DIR_NAME / project_name / INIT_FILE_NAME, "", console)
    create_file(base_pkg / INIT_FILE_NAME, "", console)
    create_file(base_pkg / "handlers" / INIT_FILE_NAME, "", console)
