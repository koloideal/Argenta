import _io
from unittest.mock import patch, MagicMock
import unittest
import io
import re

from argenta.app import App
from argenta.command import Command
from argenta.router import Router
from argenta.command.flag import Flag, FlagsGroup
from argenta.command.flag.defaults import DefaultFlags



class TestSystemHandlerNormalWork(unittest.TestCase):
    @patch("builtins.input", side_effect=["test", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print('test command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\ntest command\n', output)


    @patch("builtins.input", side_effect=["TeSt", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command2(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print('test command')

        app = App(ignore_command_register=True)
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\ntest command\n', output)


    @patch("builtins.input", side_effect=["test --help", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_custom_flag(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        flag = Flag('help', '--', False)

        @router.command(Command('test', flags=flag))
        def test(args: dict):
            print(f'\nhelp for {args['help']['name']} flag\n')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\nhelp for help flag\n', output)

    @patch("builtins.input", side_effect=["test --port 22", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_custom_flag2(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        flag = Flag('port', '--', re.compile(r'^\d{1,5}$'))

        @router.command(Command('test', flags=flag))
        def test(args: dict):
            print(f'flag value for {args['port']['name']} flag : {args["port"]["value"]}')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\nflag value for port flag : 22\n', output)


    @patch("builtins.input", side_effect=["test -h", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_default_flag(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        flag = DefaultFlags.short_help_flag

        @router.command(Command('test', flags=flag))
        def test(args: dict):
            print(f'help for {args['h']['name']} flag')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\nhelp for h flag\n', output)


    @patch("builtins.input", side_effect=["test --info", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_default_flag2(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        flag = DefaultFlags.info_flag

        @router.command(Command('test', flags=flag))
        def test(args: dict):
            if args.get('info'):
                print('info about test command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\ninfo about test command\n', output)


    @patch("builtins.input", side_effect=["test --host 192.168.0.1", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_default_flag3(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        flag = DefaultFlags.host_flag

        @router.command(Command('test', flags=flag))
        def test(args: dict):
            print(f'connecting to host {args["host"]["value"]}')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\nconnecting to host 192.168.0.1\n', output)


    @patch("builtins.input", side_effect=["test --host 192.168.32.1 --port 132", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_two_flags(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        flags = FlagsGroup(DefaultFlags.host_flag, DefaultFlags.port_flag)

        @router.command(Command('test', flags=flags))
        def test(args: dict):
            print(f'connecting to host {args["host"]["value"]} and port {args["port"]["value"]}')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertIn('\nconnecting to host 192.168.32.1 and port 132\n', output)


    @patch("builtins.input", side_effect=["test", "some", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_two_correct_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print(f'test command')

        @router.command(Command('some'))
        def test():
            print(f'some command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertRegex(output, re.compile(r'\ntest command\n(.|\n)*\nsome command\n'))


    @patch("builtins.input", side_effect=["test", "some", "more", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_three_correct_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()

        @router.command(Command('test'))
        def test():
            print(f'test command')

        @router.command(Command('some'))
        def test():
            print(f'some command')

        @router.command(Command('more'))
        def test():
            print(f'more command')

        app = App()
        app.include_router(router)
        app.start_polling()

        output = mock_stdout.getvalue()

        self.assertRegex(output, re.compile(r'\ntest command\n(.|\n)*\nsome command\n(.|\n)*\nmore command'))
