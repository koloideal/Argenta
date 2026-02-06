import io
from contextlib import redirect_stdout

from argenta import App, Router, Command, Response
from argenta.command import InputCommand


def test_simple_app() -> None:
    app = App(override_system_messages=True, repeat_command_groups_printing=False)
    router = Router(title="App")

    @router.command(Command("HELP", description="Show help"))
    def help_cmd(response: Response):
        print("Available commands: HELP")

    app.include_router(router)

    with redirect_stdout(io.StringIO()) as stdout:
        router.finds_appropriate_handler(InputCommand.parse("HELP"))

    assert "Available commands:" in stdout.getvalue()
