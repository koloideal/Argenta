from importlib.metadata import version
from typing import Annotated, Literal

import typer

from argenta._cli import commands
from argenta._cli.di import create_cli_container

app = typer.Typer(
    name="argenta",
    help="Argenta CLI — scaffold, run, inspect, and build CLI apps.",
    no_args_is_help=True,
)


def _version_callback(show_version: bool) -> None:
    if show_version:
        typer.echo(f"argenta {version('argenta')}")
        raise typer.Exit()


@app.callback()
def _root(
    ctx: typer.Context,
    version_flag: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            callback=_version_callback,
            is_eager=True,
            help="Show Argenta version and exit.",
        ),
    ] = False,
) -> None:
    """Argenta CLI — scaffold, run, inspect, and build CLI apps."""
    if ctx.obj is None:
        ctx.obj = create_cli_container()


@app.command(
    "run",
    help="Start the orchestrator REPL from a callable entrypoint.",
    short_help="Start the orchestrator REPL",
    epilog="Example: argenta run app/main.py:main",
)
def _run(
    ctx: typer.Context,
    entrypoint_path: Annotated[
        str, typer.Argument(help="Entrypoint as <path/to/file.py>:<callable>")
    ],
) -> None:
    commands.run_handler(ctx.obj, entrypoint_path)


@app.command(
    "init",
    help="Scaffold a flat or src boilerplate in the current project directory.",
    short_help="Initialize architecture in existing project",
    epilog="Run from the project root. Example: argenta init --arch src",
)
def _init(
    ctx: typer.Context,
    arch: Annotated[
        Literal["flat", "src"], typer.Option("--arch", help="Architecture: flat or src")
    ] = "flat",
) -> None:
    commands.init_handler(ctx.obj, arch)


@app.command(
    "new",
    help="Create a new project directory with a flat or src boilerplate.",
    short_help="Create a new project with boilerplate",
    epilog="Example: argenta new my-app --arch src",
)
def _new(
    ctx: typer.Context,
    project_name: Annotated[str, typer.Argument(help="Name of the new project directory")],
    arch: Annotated[
        Literal["flat", "src"], typer.Option("--arch", help="Architecture: flat or src")
    ] = "flat",
) -> None:
    commands.new_handler(ctx.obj, project_name, arch)


@app.command(
    "routes",
    help="Display all registered routes, commands, aliases, and flags. "
    "Accepts an App instance or a callable returning App.",
    short_help="Show registered routes and commands",
    epilog="Examples:\n  argenta routes app/main.py:app\n  argenta routes app/main.py:create_app",
)
def _routes(
    ctx: typer.Context,
    entrypoint_path: Annotated[
        str, typer.Argument(help="Entrypoint as <path/to/file.py>:<app_or_callable>")
    ],
) -> None:
    commands.routes_handler(ctx.obj, entrypoint_path)


@app.command(
    name="info",
    help="Display Argenta version, Python version, and platform info.",
    short_help="Show Argenta version and environment info",
)
def _show_info(ctx: typer.Context) -> None:
    commands.info_handler(ctx.obj)


@app.command(
    name="build",
    help="Compile a project entrypoint into a standalone binary using Nuitka. "
    "Any Nuitka flags can be passed after a `--` separator, e.g. "
    "`argenta build app/main.py:main -- --lto=yes --include-package=numpy`.",
    short_help="Build a standalone binary",
    epilog=(
        "Examples:\n"
        "  argenta build app/main.py:main --output myapp\n"
        "  argenta build app/main.py:main -- --lto=yes --include-data-files=assets/*=assets/"
    ),
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def _build(
    ctx: typer.Context,
    entry_point: Annotated[str, typer.Argument(help="Entrypoint as <path/to/file.py>:<callable>")],
    output_name: Annotated[
        str | None, typer.Option("--output", "-o", help="Output binary name")
    ] = None,
) -> None:
    commands.build_handler(
        ctx.obj, entry_point, output_name=output_name, extra_nuitka_args=ctx.args
    )


fonts_app = typer.Typer(
    name="fonts",
    help="Manage FIGlet banner fonts: list, fetch, and compile.",
    no_args_is_help=True,
)
app.add_typer(fonts_app, name="fonts")


@fonts_app.command(
    name="list",
    help="List FIGlet fonts available for download from the known collections.",
    short_help="List downloadable fonts",
)
def _list_fonts(ctx: typer.Context) -> None:
    commands.list_fonts_handler(ctx.obj)


@fonts_app.command(
    name="fetch",
    help="Download a FIGlet font (.flf) from a community collection or a direct URL.",
    short_help="Download a FIGlet font",
    epilog=(
        "Examples:\n"
        "  argenta fonts fetch slant\n"
        "  argenta fonts fetch slant --output-dir fonts/\n"
        "  argenta fonts fetch https://example.com/fonts/doom.flf"
    ),
)
def _fetch_font(
    ctx: typer.Context,
    font: Annotated[str, typer.Argument(help="Font name or direct .flf URL")],
    output_dir: Annotated[
        str | None, typer.Option("--output-dir", "-o", help="Directory to save the font")
    ] = None,
) -> None:
    commands.fetch_font_handler(ctx.obj, font, output_dir)


@fonts_app.command(
    name="compile",
    help="Compile a .flf FIGlet font into a fast-loading .flfd dump.",
    short_help="Compile a FIGlet font",
    epilog=(
        "Examples:\n"
        "  argenta fonts compile fonts/slant.flf\n"
        "  argenta fonts compile fonts/slant.flf --output dist/slant.flfd"
    ),
)
def _compile_font(
    ctx: typer.Context,
    font_path: Annotated[str, typer.Argument(help="Path to the .flf font file")],
    output_path: Annotated[
        str | None, typer.Option("--output", "-o", help="Output .flfd file path")
    ] = None,
) -> None:
    commands.compile_font_handler(ctx.obj, font_path, output_path)


def main() -> None:
    with create_cli_container() as container:
        app(obj=container)


if __name__ == "__main__":
    main()
