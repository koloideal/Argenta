__all__ = ["routes_handler"]

from collections import defaultdict

from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from ..infrastructure.entrypoint_resolver.entity import (
    EntryPointAsApp,
    EntrypointResolver,
    ResolveFromStringError,
)


def routes_handler(entrypoint_path: str) -> None:
    entrypoint_path, _, entrypoint_callable_name = entrypoint_path.partition(":")
    if not entrypoint_callable_name:
        raise ResolveFromStringError(
            "Path to callable object that run orchestrator repl must be in the format <path/to/file.py>:<object_name>"
        )

    app_instance = EntrypointResolver[EntryPointAsApp](entrypoint_path).parse_entrypoint_with_type(
        entrypoint_callable_name
    )

    app = app_instance.instance_object
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
            router_node.add(f"⚡ [cyan]Command:[/cyan] [bold]{trigger}[/bold] | [cyan]description:[/cyan] [bold]{description}[/bold] ")

    stats_text = (
        f"📁 [bold]Total Routers:[/bold] {stats['routers']}\n"
        f"⚡ [bold]Total Commands:[/bold] {stats['commands']}"
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
