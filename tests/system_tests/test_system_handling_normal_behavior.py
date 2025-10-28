import io
import re
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

import _io

from argenta import App, Orchestrator, Router
from argenta.command import Command, PredefinedFlags
from argenta.command.flag import Flag
from argenta.command.flag.flags import Flags
from argenta.command.flag.models import PossibleValues, ValidationStatus
from argenta.response import Response


class PatchedArgvTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.patcher = patch.object(sys, 'argv', ['program.py'])
        self.mock_argv = self.patcher.start()
        self.addCleanup(self.patcher.stop)


class TestSystemHandlerNormalWork(PatchedArgvTestCase):
    @patch("builtins.input", side_effect=["test", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            print('test command')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\ntest command\n', output)


    @patch("builtins.input", side_effect=["TeSt", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command2(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            print('test command')

        app = App(ignore_command_register=True,
                  override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\ntest command\n', output)


    @patch("builtins.input", side_effect=["test --help", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_custom_flag(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()
        flag = Flag('help', prefix='--', possible_values=PossibleValues.NEITHER)

        @router.command(Command('test', flags=flag))
        def test(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            valid_flag = response.input_flags.get_flag_by_name('help')
            if valid_flag and valid_flag.status == ValidationStatus.VALID:
                print(f'\nhelp for {valid_flag.name} flag\n')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\nhelp for help flag\n', output)

    @patch("builtins.input", side_effect=["test --port 22", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_custom_flag2(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()
        flag = Flag('port', prefix='--', possible_values=re.compile(r'^\d{1,5}$'))

        @router.command(Command('test', flags=flag))
        def test(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            valid_flag = response.input_flags.get_flag_by_name('port')
            if valid_flag and valid_flag.status == ValidationStatus.VALID:
                print(f'flag value for {valid_flag.name} flag : {valid_flag.input_value}')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\nflag value for port flag : 22\n', output)


    @patch("builtins.input", side_effect=["test -H", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_default_flag(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()
        flag = PredefinedFlags.SHORT_HELP

        @router.command(Command('test', flags=flag))
        def test(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            valid_flag = response.input_flags.get_flag_by_name('H')
            if valid_flag and valid_flag.status == ValidationStatus.VALID:
                print(f'help for {valid_flag.name} flag')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\nhelp for H flag\n', output)


    @patch("builtins.input", side_effect=["test --info", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_default_flag2(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()
        flag = PredefinedFlags.INFO

        @router.command(Command('test', flags=flag))
        def test(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            valid_flag = response.input_flags.get_flag_by_name('info')
            if valid_flag and valid_flag.status == ValidationStatus.VALID:
                print('info about test command')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\ninfo about test command\n', output)


    @patch("builtins.input", side_effect=["test --host 192.168.0.1", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_default_flag3(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()
        flag = PredefinedFlags.HOST

        @router.command(Command('test', flags=flag))
        def test(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            valid_flag = response.input_flags.get_flag_by_name('host')
            if valid_flag and valid_flag.status == ValidationStatus.VALID:
                print(f'connecting to host {valid_flag.input_value}')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\nconnecting to host 192.168.0.1\n', output)


    @patch("builtins.input", side_effect=["test --host 192.168.32.1 --port 132", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_correct_command_with_two_flags(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()
        flags = Flags([PredefinedFlags.HOST, PredefinedFlags.PORT])

        @router.command(Command('test', flags=flags))
        def test(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            host_flag = response.input_flags.get_flag_by_name('host')
            port_flag = response.input_flags.get_flag_by_name('port')
            if (host_flag and host_flag.status == ValidationStatus.VALID) and (port_flag and port_flag.status == ValidationStatus.VALID):
                print(f'connecting to host {host_flag.input_value} and port {port_flag.input_value}')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertIn('\nconnecting to host 192.168.32.1 and port 132\n', output)


    @patch("builtins.input", side_effect=["test", "some", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_two_correct_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            print(f'test command')

        @router.command(Command('some'))
        def test2(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            print(f'some command')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertRegex(output, re.compile(r'\ntest command\n(.|\n)*\nsome command\n'))


    @patch("builtins.input", side_effect=["test", "some", "more", "q"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_input_three_correct_command(self, mock_stdout: _io.StringIO, magick_mock: MagicMock):
        router = Router()
        orchestrator = Orchestrator()

        @router.command(Command('test'))
        def test(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            print(f'test command')

        @router.command(Command('some'))
        def test1(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            print(f'some command')

        @router.command(Command('more'))
        def test2(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            print(f'more command')

        app = App(override_system_messages=True,
                  print_func=print)
        app.include_router(router)
        orchestrator.start_polling(app)

        output = mock_stdout.getvalue()

        self.assertRegex(output, re.compile(r'\ntest command\n(.|\n)*\nsome command\n(.|\n)*\nmore command'))
