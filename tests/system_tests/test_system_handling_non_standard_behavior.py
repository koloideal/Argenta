import _io
from unittest.mock import patch, MagicMock
from unittest import TestCase
import io
import re

from argenta.app import App
from argenta.command import Command
from argenta.router import Router
from argenta.command.flag.flags.models import Flags
from argenta.command.flag.defaults import PredefinedFlags
from argenta.orchestrator import Orchestrator
from argenta.response import Response



class TestSystemHandlerNormalWork(TestCase):
    @patch("builtins.input", side_effect=["help", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_incorrect_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response):
            print('test command')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        app.set_unknown_command_handler(lambda command: print(f'Unknown command: {command.get_trigger()}'))
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn("\nUnknown command: help\n", output)


    @patch("builtins.input", side_effect=["TeSt", "Q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_incorrect_command2(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response):
            print('test command')

        app = App(ignore_command_register=False,
                  override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        app.set_unknown_command_handler(lambda command: print(f'Unknown command: {command.get_trigger()}'))
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\nUnknown command: TeSt\n', output)


    @patch("builtins.input", side_effect=["test --help", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_unregistered_flag(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response):
            print(f'test command with undefined flag: {response.undefined_flags.get_flag('help').get_string_entity()}')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\ntest command with undefined flag: --help\n', output)


    @patch("builtins.input", side_effect=["test --port 22", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_unregistered_flag2(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response):
            flag = response.undefined_flags.get_flag("port")
            print(f'test command with undefined flag with value: {flag.get_string_entity()} {flag.get_value()}')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\ntest command with undefined flag with value: --port 22\n', output)


    @patch("builtins.input", side_effect=["test --host 192.168.32.1 --port 132", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_one_correct_flag_an_one_incorrect_flag(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()
        flags = Flags(PredefinedFlags.HOST)

        @router.command(Command('test', flags=flags))
        def test(response: Response):
            flag = response.undefined_flags.get_flag("port")
            print(f'connecting to host with flag: {flag.get_string_entity()} {flag.get_value()}')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\nconnecting to host with flag: --port 132\n', output)


    @patch("builtins.input", side_effect=["test", "some", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_one_correct_command_and_one_incorrect_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response):
            print(f'test command')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        app.set_unknown_command_handler(lambda command: print(f'Unknown command: {command.get_trigger()}'))
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertRegex(output, re.compile(r'\ntest command\n(.|\n)*\nUnknown command: some'))


    @patch("builtins.input", side_effect=["test", "some", "more", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_two_correct_commands_and_one_incorrect_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response):
            print(f'test command')

        @router.command(Command('more'))
        def test(response: Response):
            print(f'more command')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        app.set_unknown_command_handler(lambda command: print(f'Unknown command: {command.get_trigger()}'))
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertRegex(output, re.compile(r'\ntest command\n(.|\n)*\nUnknown command: some\n(.|\n)*\nmore command'))


    @patch("builtins.input", side_effect=["test 535 --port", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_incorrect_flag(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response):
            print(f'test command')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        app.set_incorrect_input_syntax_handler(lambda command: print(f'Incorrect flag syntax: "{command}"'))
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn("\nIncorrect flag syntax: \"test 535 --port\"\n", output)


    @patch("builtins.input", side_effect=["", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_empty_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response):
            print(f'test command')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        app.set_empty_command_handler(lambda: print('Empty input command'))
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn("\nEmpty input command\n", output)


    @patch("builtins.input", side_effect=["test --port 22 --port 33", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_repeated_flags(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test', flags=PredefinedFlags.PORT))
        def test(response: Response):
            print('test command')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        app.set_repeated_input_flags_handler(lambda command: print(f'Repeated input flags: "{command}"'))
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn("\nRepeated input flags: \"test --port 22 --port 33\"\n", output)
