__all__ = ["build_handler"]

import os
import subprocess
import sys
from pathlib import Path

from rich.console import Console


def build_handler(entry_point: str, output_name: str | None = None) -> None:
    console = Console()
    file_path, _, callable_name = entry_point.partition(":")

    if not file_path or not callable_name:
        console.print(
            f'[bold red]Error:[/bold red] "{entry_point}" must be in format "<path/to/file.py>:<callable>"'
        )
        raise SystemExit(1)

    path = Path(file_path).resolve()

    if not path.exists():
        console.print(f'[bold red]Error:[/bold red] File "{file_path}" not found')
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
        f"--jobs={os.cpu_count()}",
        "--lto=no",
        "--include-windows-runtime-dlls=no",
    ]

    if is_main_module:
        args.append("--python-flag=-m")

    args.append(target)

    result = subprocess.run(args, check=False)

    if result.returncode != 0:
        console.print("[bold red]Build failed.[/bold red]")
        raise SystemExit(result.returncode)

    console.print(f"[bold green]Done![/bold green] Binary: [cyan]{name}[/cyan]")
