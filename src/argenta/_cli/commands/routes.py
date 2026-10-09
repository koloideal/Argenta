import sys
from collections import defaultdict

from dishka import Container
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from argenta._cli.commands._entrypoint import (
    EntrypointSpec,
    report_entrypoint_error,
    resolve_callable_entrypoint,
    split_entrypoint_spec,
)
from argenta._cli.infrastructure.entrypoint_resolver.entity import (
    EntryPointAsApp,
    EntrypointResolver,
)
from argenta._cli.infrastructure.entrypoint_resolver.exceptions import (
    EntrypointError,
    EntrypointNotAppInstanceError,
    ResolveFromStringError,
)
from argenta.app.models import App
from argenta.command.flag.models import Flag
from argenta.router.command_handler.entity import CommandHandler


def routes_handler(container: Container, entrypoint_path: str) -> None:
    console = container.get(Console)
    spec = split_entrypoint_spec(
        entrypoint_path,
        console,
        format_hint='"<path/to/file.py>:<app_object>" or "<path.to.module>:<app_object>"',
    )
    app_instance = _resolve_app(spec, console)
    tree, stats = _build_command_tree(app_instance)
    _print_routes(console, tree, stats)


def _print_routes(console: Console, tree: Tree, stats: dict[str, int]) -> None:
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


def _resolve_app(spec: EntrypointSpec, console: Console) -> App:
    try:
        return (
            EntrypointResolver[EntryPointAsApp](spec.file_path)
            .parse_entrypoint_with_type(spec.callable_name)
            .instance_object
        )
    except EntrypointNotAppInstanceError:
        return _resolve_app_from_callable(spec, console)
    except (ResolveFromStringError, EntrypointError) as error:
        report_entrypoint_error(console, error)


def _resolve_app_from_callable(spec: EntrypointSpec, console: Console) -> App:
    resolved = resolve_callable_entrypoint(spec, console).instance_object()
    if not isinstance(resolved, App):
        resolved_type_name = type(resolved).__name__
        console.print(
            f"[bold red]Error:[/bold red] callable must return an App instance,"
            f" got {resolved_type_name}"
        )
        sys.exit(1)
    return resolved


def _build_command_tree(app: App) -> tuple[Tree, dict[str, int]]:
    stats: dict[str, int] = defaultdict(int)
    tree = Tree(f"📦 [bold blue]App object:[/bold blue] {app!r}")

    for router in app.registered_routers:
        stats["routers"] += 1
        router_node = tree.add(f"📁 [bold green]Router:[/bold green] {router.title}")
        for command in router.command_handlers:
            _add_command_node(router_node, command, stats)

    return tree, stats


def _add_command_node(router_node: Tree, command: CommandHandler, stats: dict[str, int]) -> None:
    stats["commands"] += 1
    handled_command = command.handled_command
    cmd_node = router_node.add(f"⚡ [bold cyan]{handled_command.trigger}[/bold cyan]")

    if handled_command.description:
        cmd_node.add(f"📝 [dim]description:[/dim] {handled_command.description}")

    aliases = list(handled_command.aliases)
    if aliases:
        aliases_str = ", ".join(f"[yellow]{alias}[/yellow]" for alias in aliases)
        cmd_node.add(f"🔀 [dim]aliases:[/dim] {aliases_str}")
        stats["aliases"] += len(aliases)

    flags = list(handled_command.registered_flags)
    if flags:
        _add_flag_nodes(cmd_node, flags, stats)


def _add_flag_nodes(cmd_node: Tree, flags: list[Flag], stats: dict[str, int]) -> None:
    flags_node = cmd_node.add(f"🚩 [dim]flags:[/dim] ({len(flags)})")
    for flag in flags:
        possible = flag.possible_values
        flags_node.add(
            f"[magenta]{flag.prefix}{flag.name}[/magenta]"
            f"  [dim]possible_values:[/dim] [italic]{possible!r}[/italic]"
        )
    stats["flags"] += len(flags)
