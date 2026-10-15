import sys
from pathlib import Path

from dishka import Container
from rich.console import Console

from argenta.app.presentation.ascii_art import FigletFontException, FigletFontFetcher


def fetch_font_handler(container: Container, font: str, output_dir: str | None) -> None:
    console = container.get(Console)
    try:
        target = FigletFontFetcher().fetch(font, Path(output_dir) if output_dir else ".")
    except FigletFontException as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        sys.exit(1)
    console.print(f"Downloaded → [bold cyan]{target}[/bold cyan]")
    console.print(f"Compile for fast loading: [dim]argenta fonts compile {target}[/dim]")
