import platform
import sys
from importlib.metadata import version

from dishka import Container
from rich import box
from rich.console import Console
from rich.padding import Padding
from rich.table import Table

from argenta.app.presentation.ascii_art import AsciiArtRenderer, BundledFont, FigletFontLoader


def info_handler(container: Container) -> None:
    console = container.get(Console)
    table = Table(
        box=box.SIMPLE,
        show_header=False,
        pad_edge=False,
        show_edge=False,
        expand=False,
    )

    table.add_column(style="bold cyan")
    table.add_column(style="white", justify="right")

    table.add_row("Argenta version", f"[bold red]{version('argenta')}[/bold red]")
    table.add_row("Python version", sys.version.split()[0])
    system_name = platform.system()
    release_name = platform.release()
    machine_name = platform.machine()
    table.add_row("Platform", f"{system_name} {release_name} ({machine_name})")
    table.add_row("Docs", "https://argenta.wiki")

    console.print(f"[bold red]{_render_banner()}[/bold red]")
    console.print(Padding(table, pad=(2, 5)))
    console.print(Padding("[i]made with ❤ by [b]kolo[/b][/i]", pad=(0, 17)))


def _render_banner() -> str:
    banner_font = FigletFontLoader().load_bundled(BundledFont.TARTY1)
    return AsciiArtRenderer().render("Argenta", banner_font)
