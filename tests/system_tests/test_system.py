import _io
from unittest.mock import patch, MagicMock
import unittest
import io

from argenta.app import App
from argenta.command import Command
from argenta.router import Router



class TestSystem(unittest.TestCase):
    @patch("builtins.input", side_effect=["test", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_run_shell_output(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print('test command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('test command', output)


