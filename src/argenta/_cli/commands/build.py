__all__ = ["build_handler"]

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

from dishka import Container
from rich.console import Console

from argenta._cli.infrastructure.entrypoint_resolver.entity import (
    CallableEntryPoint,
    EntrypointResolver,
)
from argenta._cli.infrastructure.entrypoint_resolver.exceptions import (
    EntrypointError,
    ResolveFromStringError,
)


def build_handler(
    container: Container,
    entry_point: str,
    output_name: str | None = None,
    extra_nuitka_args: list[str] | None = None,
) -> None:
    console = container.get(Console)
    file_path, sep, callable_name = entry_point.rpartition(":")

    if not sep or not file_path or not callable_name:
        console.print(
            f'[bold red]Error:[/bold red] "{entry_point}" must be in format "<path/to/file.py>:<callable>"'
        )
        raise SystemExit(1)

    if importlib.util.find_spec("nuitka") is None:
        console.print(
            "[bold red]Error:[/bold red] nuitka is required for the build command. "
            "Install it via 'pip install argenta[cli]' or 'pip install nuitka[onefile]'"
        )
        raise SystemExit(1)

    try:
        runner = EntrypointResolver[CallableEntryPoint](file_path).parse_entrypoint_with_type(
            callable_name
        )
    except (ResolveFromStringError, EntrypointError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise SystemExit(1)

    path = Path(runner.raw_path)

    if not path.exists() or path.suffix != ".py":
        console.print(
            f'[bold red]Error:[/bold red] cannot resolve "{runner.raw_path}" to a Python file'
        )
        raise SystemExit(1)

    is_main_module = path.name == "__main__.py"
    target = str(path.parent) if is_main_module else str(path)
    name = output_name or (path.parent.name if is_main_module else path.stem)

    console.print(
        f"[bold green]Building[/bold green] [cyan]{entry_point}[/cyan] → [cyan]{name}[/cyan]"
    )

    args = [
        sys.executable,
        "-m",
        "nuitka",
        "--standalone",
        "--onefile",
        f"--output-filename={name}",
        f"--jobs={os.cpu_count() or 1}",
        "--lto=no",
        "--include-windows-runtime-dlls=no",
    ]

    if is_main_module:
        args.append("--python-flag=-m")

    # User-provided Nuitka flags are appended last, so they can override
    # Argenta's defaults (e.g. --lto=yes, --jobs=1) and add anything else
    # Nuitka supports (--include-package, --include-data-files, --enable-plugin, ...).
    if extra_nuitka_args:
        args.extend(extra_nuitka_args)

    args.append(target)

    result = subprocess.run(args, check=False)

    if result.returncode != 0:
        console.print("[bold red]Build failed.[/bold red]")
        raise SystemExit(result.returncode)

    console.print(f"[bold green]Done![/bold green] Binary: [cyan]{name}[/cyan]")
