from importlib.metadata import version

import typer
from typer import Typer

from .commands import (
    build_handler,
    info_handler,
    init_handler,
    new_handler,
    routes_handler,
    run_handler,
)

app = Typer(
    name="argenta",
    help="Argenta CLI — scaffold, run, inspect, and build CLI apps.",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"argenta {version('argenta')}")
        raise typer.Exit()


@app.callback()
def _root(
    version_flag: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        is_eager=True,
        help="Show Argenta version and exit.",
    ),
) -> None:
    """Argenta CLI — scaffold, run, inspect, and build CLI apps."""


@app.command(
    "run",
    help="Start the orchestrator REPL from a callable entrypoint.",
    short_help="Start the orchestrator REPL",
    epilog="Example: argenta run app/main.py:main",
)
def _run(entrypoint_path: str = typer.Argument(help="Entrypoint as <path/to/file.py>:<callable>")) -> None:
    run_handler(entrypoint_path)


@app.command(
    "init",
    help="Scaffold a flat or src boilerplate in the current project directory.",
    short_help="Initialize architecture in existing project",
    epilog="Run from the project root. Example: argenta init --with-arch src",
)
def _init(with_arch: str = typer.Option("flat", "--with-arch", help="Architecture: flat or src")) -> None:
    init_handler(with_arch=with_arch)  # type: ignore[arg-type]


@app.command(
    "new",
    help="Create a new project directory with a flat or src boilerplate.",
    short_help="Create a new project with boilerplate",
    epilog="Example: argenta new my-app --with-arch src",
)
def _new(
    project_name: str = typer.Argument(help="Name of the new project directory"),
    with_arch: str = typer.Option("flat", "--with-arch", help="Architecture: flat or src"),
) -> None:
    new_handler(project_name=project_name, with_arch=with_arch)  # type: ignore[arg-type]


@app.command(
    "routes",
    help="Display all registered routes, commands, aliases, and flags. Accepts an App instance or a callable returning App.",
    short_help="Show registered routes and commands",
    epilog="Examples:\n  argenta routes app/main.py:app\n  argenta routes app/main.py:create_app",
)
def _routes(entrypoint_path: str = typer.Argument(help="Entrypoint as <path/to/file.py>:<app_or_callable>")) -> None:
    routes_handler(entrypoint_path)


@app.command(
    name="info",
    help="Display Argenta version, Python version, and platform info.",
    short_help="Show Argenta version and environment info",
)
def _info() -> None:
    info_handler()


@app.command(
    name="build",
    help="Compile a project entrypoint into a standalone binary using Nuitka.",
    short_help="Build a standalone binary",
    epilog="Example: argenta build app/main.py:main --output myapp",
)
def _build(
    entry_point: str = typer.Argument(help="Entrypoint as <path/to/file.py>:<callable>"),
    output_name: str | None = typer.Option(None, "--output", "-o", help="Output binary name"),
) -> None:
    build_handler(entry_point=entry_point, output_name=output_name)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
