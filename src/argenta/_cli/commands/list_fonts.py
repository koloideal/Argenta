import sys

from dishka import Container
from rich.columns import Columns
from rich.console import Console

from argenta.app.presentation.ascii_art import FigletFontException, FigletFontFetcher


def list_fonts_handler(container: Container) -> None:
    console = container.get(Console)
    try:
        names = FigletFontFetcher().list_available()
    except FigletFontException as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        sys.exit(1)
    console.print(f"[bold]{len(names)} fonts available[/bold]")
    console.print(Columns(names))
