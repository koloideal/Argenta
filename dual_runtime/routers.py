"""Inventory commands reused by the REPL, the agent and the script runtime."""

from typing import Final

from rich.console import Console

from argenta import Command, Response, Router
from argenta.command import Flag, Flags
from argenta.command.flag import ValidationStatus

inventory_router: Router = Router(title="Inventory:")
console = Console(highlight=False)

_ITEM_FLAG: Final = "item"

_stock: dict[str, int] = {"milk": 10, "bread": 4}


def _flag_input(response: Response, name: str) -> str:
    flag = response.input_flags.get_flag_by_name(name, with_status=ValidationStatus.VALID)
    return flag.input_value if flag else ""


def _quantity(response: Response) -> int | None:
    raw_quantity = _flag_input(response, "qty")
    try:
        return int(raw_quantity)
    except ValueError:
        console.print(f"[red]--qty must be an integer, got '{raw_quantity}'[/red]")
        return None


@inventory_router.command(Command("stock", description="List stock levels"))
def stock_handler(response: Response) -> None:
    for product, quantity in sorted(_stock.items()):
        console.print(f"{product}: [bold]{quantity}[/bold]")


@inventory_router.command(
    Command(
        "add",
        flags=Flags([Flag(_ITEM_FLAG), Flag("qty")]),
        description="Add units of a product to the stock",
    )
)
def add_handler(response: Response) -> None:
    product = _flag_input(response, _ITEM_FLAG)
    quantity = _quantity(response)
    if not product or quantity is None:
        console.print("[red]Usage: add --item <name> --qty <n>[/red]")
        return
    _stock[product] = _stock.get(product, 0) + quantity
    console.print(f"[green]{product}[/green]: {_stock[product]} in stock")


@inventory_router.command(
    Command(
        "ship",
        flags=Flags([Flag(_ITEM_FLAG), Flag("qty")]),
        description="Ship units of a product out of the stock",
    )
)
def ship_handler(response: Response) -> None:
    product = _flag_input(response, _ITEM_FLAG)
    quantity = _quantity(response)
    if not product or quantity is None:
        console.print("[red]Usage: ship --item <name> --qty <n>[/red]")
        return
    available = _stock.get(product, 0)
    if quantity > available:
        console.print(f"[red]Cannot ship {quantity} of {product}: only {available} left[/red]")
        return
    _stock[product] = available - quantity
    console.print(f"Shipped {quantity} of [green]{product}[/green], {_stock[product]} left")
