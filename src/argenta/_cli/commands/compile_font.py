import sys
from pathlib import Path

from dishka import Container
from rich.console import Console

from argenta.app.presentation.ascii_art import FigletFontException, FigletFontLoader


def compile_font_handler(container: Container, font_path: str, output_path: str | None) -> None:
    console = container.get(Console)
    try:
        target = FigletFontLoader().compile(font_path, Path(output_path) if output_path else None)
    except FigletFontException as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        sys.exit(1)
    console.print(f"Compiled [bold cyan]{font_path}[/bold cyan] → [bold cyan]{target}[/bold cyan]")
