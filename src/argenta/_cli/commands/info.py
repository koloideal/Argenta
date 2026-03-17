__all__ = ["info_handler"]

import sys
import platform
from importlib.metadata import version

from art import text2art  # pyright: ignore[reportUnknownVariableType]
from rich.console import Console
from rich.padding import Padding
from rich.table import Table
from rich import box


console = Console()


def info_handler() -> None:
    table = Table(
        box=box.SIMPLE,
        show_header=False,
        pad_edge=False,
        show_edge=False,
        expand=False,
    )

    table.add_column(style="bold cyan")
    table.add_column(style="white", justify="right")

    table.add_row("Argenta version", f'[bold red]{version("argenta")}[/bold red]')
    table.add_row("Python version", sys.version.split()[0])
    table.add_row("Platform", f"{platform.system()} {platform.release()} ({platform.machine()})")
    table.add_row("Docs", "https://argenta.readthedocs.io")
    
    console.print(f"[bold red]{text2art("Argenta", font='tarty1')}[/bold red]")
    console.print(Padding(table, pad=(2, 5)))
    console.print(Padding("[i]made with ❤ by [b]kolo[/b][/i]", pad=(0, 17)))
