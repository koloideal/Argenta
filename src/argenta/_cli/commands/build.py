import os
import subprocess
import sys
from dataclasses import dataclass
from importlib.util import find_spec
from pathlib import Path

from dishka import Container
from rich.console import Console

from argenta._cli.commands._entrypoint import (
    resolve_callable_entrypoint,
    split_entrypoint_spec,
)


def build_handler(
    container: Container,
    entry_point: str,
    output_name: str | None = None,
    extra_nuitka_args: list[str] | None = None,
) -> None:
    console = container.get(Console)
    spec = split_entrypoint_spec(entry_point, console, format_hint='"<path/to/file.py>:<callable>"')
    _ensure_nuitka(console)
    runner = resolve_callable_entrypoint(spec, console)
    build_target = _resolve_build_target(runner.raw_path, output_name, console)
    _run_build(console, entry_point, build_target, extra_nuitka_args)


def _ensure_nuitka(console: Console) -> None:
    if find_spec("nuitka") is None:
        console.print(
            "[bold red]Error:[/bold red] nuitka is required for the build command. "
            "Install it via 'pip install argenta[cli]' or 'pip install nuitka[onefile]'"
        )
        sys.exit(1)


@dataclass(frozen=True, slots=True)
class _BuildTarget:
    target: str
    name: str
    is_main_module: bool


def _resolve_build_target(raw_path: str, output_name: str | None, console: Console) -> _BuildTarget:
    path = Path(raw_path)

    if not path.exists() or path.suffix != ".py":
        console.print(f'[bold red]Error:[/bold red] cannot resolve "{raw_path}" to a Python file')
        sys.exit(1)

    is_main_module = path.name == "__main__.py"
    target = str(path.parent) if is_main_module else str(path)
    default_name = path.parent.name if is_main_module else path.stem
    return _BuildTarget(target, output_name or default_name, is_main_module)


def _run_build(
    console: Console,
    entry_point: str,
    build_target: _BuildTarget,
    extra_args: list[str] | None,
) -> None:
    console.print(
        f"[bold green]Building[/bold green] [cyan]{entry_point}[/cyan] →"
        f" [cyan]{build_target.name}[/cyan]"
    )

    completed = subprocess.run(_nuitka_args(build_target, extra_args), check=False)

    if completed.returncode != 0:
        console.print("[bold red]Build failed.[/bold red]")
        sys.exit(completed.returncode)

    console.print(f"[bold green]Done![/bold green] Binary: [cyan]{build_target.name}[/cyan]")


def _nuitka_args(build_target: _BuildTarget, extra_args: list[str] | None) -> list[str]:
    cpu_count = os.cpu_count() or 1
    args = [
        sys.executable,
        "-m",
        "nuitka",
        "--standalone",
        "--onefile",
        f"--output-filename={build_target.name}",
        f"--jobs={cpu_count}",
        "--lto=no",
        "--include-windows-runtime-dlls=no",
    ]

    if build_target.is_main_module:
        args.append("--python-flag=-m")

    # User-provided Nuitka flags are appended last, so they can override
    # Argenta's defaults (e.g. --lto=yes, --jobs=1) and add anything else
    # Nuitka supports (--include-package, --include-data-files, --enable-plugin, ...).
    if extra_args:
        args.extend(extra_args)

    args.append(build_target.target)
    return args
