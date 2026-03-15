from typer import Typer

from .commands import init_handler, new_handler, run_handler


def main() -> None:
    app = Typer()
    app.command(
        "run",
        help="Command to start the orchestrator repl; the path to the callable object is required",
        short_help="Start the orchestrator REPL",
        epilog="Example: run app/main.py:main",
    )(run_handler)

    app.command(
        "init",
        help="Creates a flat/src boilerplate architecture in an existing project",
        short_help="Initialize architecture in existing project",
        epilog="Make sure you are in the project root before running this command.",
    )(init_handler)

    app.command(
        "new",
        help="Creates a project and in it flat/src boilerplate architecture",
        short_help="Create a new project with boilerplate",
        epilog="This will create a new directory with the project structure.",
    )(new_handler)

    app()


if __name__ == "__main__":
    main()
