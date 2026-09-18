__all__ = ["routes_handler"]

from collections import defaultdict

from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from argenta.app.models import App

from ..infrastructure.entrypoint_resolver.entity import (
    CallableEntryPoint,
    EntryPointAsApp,
    EntrypointResolver,
)
from ..infrastructure.entrypoint_resolver.exceptions import (
    EntrypointError,
    EntrypointNotAppInstanceError,
    ResolveFromStringError,
)


def routes_handler(entrypoint_path: str) -> None:
    file_path, _, callable_name = entrypoint_path.partition(":")
    if not callable_name:
        Console().print(
            f'[bold red]Error:[/bold red] "{entrypoint_path}" must be in format '
            f'"<path/to/file.py>:<app_object>" or "<path.to.module>:<app_object>"'
        )
        raise SystemExit(1)

    try:
        app_instance = EntrypointResolver[EntryPointAsApp](file_path).parse_entrypoint_with_type(
            callable_name
        )
        app = app_instance.instance_object
    except EntrypointNotAppInstanceError:
        try:
            callable_entrypoint = EntrypointResolver[CallableEntryPoint](
                file_path
                ).parse_entrypoint_with_type(
                callable_name
            )
        except (ResolveFromStringError, EntrypointError) as e:
            Console().print(f"[bold red]Error:[/bold red] {e}")
            raise SystemExit(1)
        app = callable_entrypoint.instance_object()
        if not isinstance(app, App):
            Console().print(
                f"[bold red]Error:[/bold red] callable must return an App instance, got {type(app).__name__}"
            )
            raise SystemExit(1)
    except (ResolveFromStringError, EntrypointError) as e:
        Console().print(f"[bold red]Error:[/bold red] {e}")
        raise SystemExit(1)
    routers = app.registered_routers

    console = Console()
    stats: dict[str, int] = defaultdict(int)

    tree = Tree(f"📦 [bold blue]App object:[/bold blue] {app!r}")

    for router in routers:
        stats["routers"] += 1
        router_node = tree.add(f"📁 [bold green]Router:[/bold green] {router.title}")

        for command in router.command_handlers:
            stats["commands"] += 1
            trigger = command.handled_command.trigger
            description = command.handled_command.description
            aliases = list(command.handled_command.aliases)
            flags = list(command.handled_command.registered_flags)

            cmd_node = router_node.add(f"⚡ [bold cyan]{trigger}[/bold cyan]")

            if description:
                cmd_node.add(f"📝 [dim]description:[/dim] {description}")

            if aliases:
                aliases_str = ", ".join(f"[yellow]{a}[/yellow]" for a in aliases)
                cmd_node.add(f"🔀 [dim]aliases:[/dim] {aliases_str}")
                stats["aliases"] += len(aliases)

            if flags:
                flags_node = cmd_node.add(f"🚩 [dim]flags:[/dim] ({len(flags)})")
                for flag in flags:
                    possible = flag.possible_values
                    flags_node.add(
                        f"[magenta]{flag.prefix}{flag.name}[/magenta]"
                        f"  [dim]possible_values:[/dim] [italic]{possible!r}[/italic]"
                    )
                stats["flags"] += len(flags)

    stats_text = (
        f"📁 [bold]Total Routers:[/bold]  {stats['routers']}\n"
        f"⚡ [bold]Total Commands:[/bold] {stats['commands']}\n"
        f"🔀 [bold]Total Aliases:[/bold]  {stats['aliases']}\n"
        f"🚩 [bold]Total Flags:[/bold]    {stats['flags']}"
    )

    console.print(
        Panel(
            stats_text,
            title="[bold blue]App Stats[/bold blue]",
            expand=False,
            border_style="blue",
        )
    )
    console.print()
    console.print(tree)
