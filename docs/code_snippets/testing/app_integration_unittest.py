import io
import unittest
from contextlib import redirect_stdout

from argenta import App, Router, Command, Response
from argenta.command import InputCommand


class TestAppIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.app = App(override_system_messages=True, repeat_command_groups=False)
        self.router = Router(title="App")

        @self.router.command(Command("HELP", description="Show help"))
        def help_cmd(response: Response):
            print("Available commands: HELP")

        _ = help_cmd  # appease linter: function is registered via decorator

        self.app.include_router(self.router)

    def test_help_command(self):
        with redirect_stdout(io.StringIO()) as stdout:
            self.router.finds_appropriate_handler(InputCommand.parse("HELP"))
        self.assertIn("Available commands:", stdout.getvalue())
