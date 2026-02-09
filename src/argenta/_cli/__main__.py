from typer import Typer

from .commands import run_handler, init_handler


def main():
    app = Typer()
    app.command("run")(run_handler)
    app.command("init")(init_handler)
    app()

if __name__ == '__main__':
    main()