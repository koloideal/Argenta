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


def new_handler(
    container: Container, project_name: str, arch: Literal["flat", "src"] = "flat"
) -> None:
    console = container.get(Console)

    _validate_project_name(project_name, console)
    base_dir = _prepare_project_dir(project_name, arch, console)
    _scaffold_project(base_dir, project_name, arch, console)

    console.print(f"\nProject '{project_name}' created successfully! 🚀")


def _validate_project_name(project_name: str, console: Console) -> None:
    if project_name in (".", "..") or "/" in project_name or "\\" in project_name:
        console.print(f'[bold red]Error:[/bold red] "{project_name}" is not a valid project name')
        sys.exit(1)


def _prepare_project_dir(project_name: str, arch: Literal["flat", "src"], console: Console) -> Path:
    base_dir = Path.cwd() / project_name

    if base_dir.exists():
        console.print(f"[bold red]Error:[/bold red] Directory '{project_name}' already exists.")
        sys.exit(1)

    if arch == "src" and not sanitize_package_name(project_name).isidentifier():
        console.print(
            f'[bold red]Error:[/bold red] cannot derive a valid package name from "{project_name}"'
        )
        sys.exit(1)

    base_dir.mkdir()
    console.print(f"Initialized project directory: {base_dir}")
    return base_dir


def _scaffold_project(
    base_dir: Path, project_name: str, arch: Literal["flat", "src"], console: Console
) -> None:
    create_file(base_dir / ".gitignore", GITIGNORE_CONTENT, console)

    if arch == "flat":
        _create_flat_layout(base_dir, console)
    elif arch == "src":
        pkg_name = sanitize_package_name(project_name)
        _create_src_layout(base_dir, pkg_name, console)


def _create_flat_layout(base_dir: Path, console: Console) -> None:
    create_file(base_dir / "main.py", FLAT_MAIN_TEMPLATE, console)
    create_file(base_dir / "handlers.py", FLAT_HANDLERS_TEMPLATE, console)


def _create_src_layout(base_dir: Path, pkg_name: str, console: Console) -> None:
    app_pkg = base_dir / SRC_DIR_NAME / pkg_name / "application"

    create_file(app_pkg / "__main__.py", SRC_MAIN_TEMPLATE, console)
    create_file(app_pkg / "routers.py", SRC_ROUTERS_TEMPLATE, console)
    create_file(app_pkg / "handlers" / "hello_world_handler.py", SRC_HANDLER_TEMPLATE, console)

    create_file(base_dir / SRC_DIR_NAME / INIT_FILE_NAME, "", console)
    create_file(base_dir / SRC_DIR_NAME / pkg_name / INIT_FILE_NAME, "", console)
    create_file(app_pkg / INIT_FILE_NAME, "", console)
    create_file(app_pkg / "handlers" / INIT_FILE_NAME, "", console)
