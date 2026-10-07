__all__ = ["info_handler"]

import platform
import sys
from importlib.metadata import version

from art import text2art  # pyright: ignore[reportUnknownVariableType]
from dishka import Container
from rich import box
from rich.console import Console
from rich.padding import Padding
from rich.table import Table


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
    table.add_row("Platform", f"{platform.system()} {platform.release()} ({platform.machine()})")
    table.add_row("Docs", "https://argenta.readthedocs.io")

    console.print(f"[bold red]{text2art('Argenta', font='tarty1')}[/bold red]")
    console.print(Padding(table, pad=(2, 5)))
    console.print(Padding("[i]made with ❤ by [b]kolo[/b][/i]", pad=(0, 17)))
