from rich.console import Console

from argenta import Command, Response, Router

router = Router(title="Quickstart Example")
console = Console()


@router.command(Command("hello", description="Say hello"))
def hello_handler(response: Response) -> None:
    console.print("[bold green]Hello, world![/bold green] :wave:")
