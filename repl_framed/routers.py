"""Monitoring and administration commands for the framed REPL example."""

from typing import Final

from rich.console import Console

from argenta import Command, Response, Router
from argenta.command import Flag, Flags
from argenta.command.flag import ValidationStatus

ops_router: Router = Router(title="Monitoring:")
admin_router: Router = Router(title="Administration:", disable_redirect_stdout=True)
console = Console()

_SERVICE_COLUMN: Final = 10
_LOG_LEVELS: Final = ("info", "warn", "error")


def _flag_input(response: Response, name: str) -> str:
    flag = response.input_flags.get_flag_by_name(name, with_status=ValidationStatus.VALID)
    return flag.input_value if flag else ""


@ops_router.command(Command("status", description="Show health of the services"))
def status_handler(response: Response) -> None:
    services = {
        "api": "[green]up[/green]",
        "worker": "[green]up[/green]",
        "scheduler": "[yellow]degraded[/yellow]",
    }
    for service, state in services.items():
        console.print(service.ljust(_SERVICE_COLUMN), state)


@ops_router.command(
    Command(
        "logs",
        flags=Flags([Flag("service"), Flag("level", possible_values=_LOG_LEVELS)]),
        description="Show the last log lines of a service",
    )
)
def logs_handler(response: Response) -> None:
    service = _flag_input(response, "service") or "api"
    level = _flag_input(response, "level") or "info"
    console.print(f"[dim]--- {service} / {level} ---[/dim]")
    console.print(f"12:00:01 [{level}] request handled in 42ms")
    console.print(f"12:00:02 [{level}] cache hit for key 'session'")
    console.print(f"12:00:03 [{level}] heartbeat ok")


@admin_router.command(
    Command("deploy", flags=Flag("version"), description="Deploy a version with confirmation")
)
def deploy_handler(response: Response) -> None:
    version = _flag_input(response, "version") or "latest"
    answer = console.input(f"Deploy {version} to production? [y/N] ")
    if answer.strip().lower() == "y":
        console.print(f"[green]Deployed {version}[/green]")
    else:
        console.print("[yellow]Aborted[/yellow]")
