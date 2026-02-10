from typer import Typer

from .commands import run_handler, init_handler, new_handler


def main() -> None:
    app = Typer()
    app.command("run", help='Command to start the orchestrator repl; the path to the orchestrator is required')(run_handler)
    app.command("init", help="Creates a flat/src boilerplate architecture in an existing project")(init_handler)
    app.command("new", help="Creates a project and in it flat/src boilerplate architecture")(new_handler)
    app()

if __name__ == '__main__':
    main()