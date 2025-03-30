import _io
from unittest.mock import patch, MagicMock
import unittest
import io
import re

from argenta.app import App
from argenta.command import Command
from argenta.router import Router
from argenta.command.flag.registered_flag import FlagsGroup
from argenta.command.flag.registered_flag.defaults import DefaultFlags



class TestSystemHandlerNormalWork(unittest.TestCase):
    @patch("builtins.input", side_effect=["help", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_incorrect_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print('test command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn("\nUnknown command: help\n", output)


    @patch("builtins.input", side_effect=["TeSt", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_incorrect_command2(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print('test command')

        app = App(ignore_command_register=False)
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\nUnknown command: TeSt\n', output)


    @patch("builtins.input", side_effect=["test --help", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_unregistered_flag(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print(f'test command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\nUndefined or incorrect input registered_flag: --help\n', output)


    @patch("builtins.input", side_effect=["test --port 22", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_unregistered_flag2(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print('test command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\nUndefined or incorrect input registered_flag: --port 22\n', output)


    @patch("builtins.input", side_effect=["test --host 192.168.32.1 --port 132", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_one_correct_flag_an_one_incorrect_flag(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        flags = FlagsGroup(DefaultFlags.HOST)

        @router.command(Command('test', flags=flags))
        def test(args: dict):
            print(f'connecting to host {args["host"]["value"]}')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\nUndefined or incorrect input registered_flag: --port 132\n', output)


    @patch("builtins.input", side_effect=["test", "some", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_one_correct_command_and_one_incorrect_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print(f'test command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertRegex(output, re.compile(r'\ntest command\n(.|\n)*\nUnknown command: some\n'))


    @patch("builtins.input", side_effect=["test", "some", "more", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_two_correct_commands_and_one_incorrect_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print(f'test command')

        @router.command(Command('more'))
        def test():
            print(f'more command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertRegex(output, re.compile(r'\ntest command\n(.|\n)*\nUnknown command: some\n(.|\n)*\nmore command'))


    @patch("builtins.input", side_effect=["test 535 --port", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_incorrect_flag(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print(f'test command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn("\nIncorrect registered_flag syntax: \"test 535 --port\"\n", output)


    @patch("builtins.input", side_effect=["", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_empty_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print(f'test command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn("\nEmpty input command\n", output)


    @patch("builtins.input", side_effect=["test --port 22 --port 33", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_repeated_flags(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test', flags=DefaultFlags.PORT))
        def test(args):
            print('test command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn("\nRepeated input flags: \"test --port 22 --port 33\"", output)
