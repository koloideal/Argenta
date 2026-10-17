from rich.console import Console

from argenta import Command, Response, Router
from argenta.command import Flag
from argenta.command.flag import ValidationStatus

work_router: Router = Router(title="Base points:")
console = Console()


@work_router.command(Command("greet", flags=Flag("name"), description="Greet the user by name"))
def greet_handler(response: Response) -> None:
    name_flag = response.input_flags.get_flag_by_name("name", with_status=ValidationStatus.VALID)
    if name_flag:
        console.print(f"[bold cyan]Hello,[/bold cyan] [magenta]{name_flag.input_value}[/magenta]!")
    else:
        console.print("[bold cyan]Hello, world![/bold cyan]")
