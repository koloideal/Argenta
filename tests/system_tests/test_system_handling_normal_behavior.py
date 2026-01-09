import re
import sys
from collections.abc import Iterator

import pytest

from argenta import App, Orchestrator, Router
from argenta.command import Command, PredefinedFlags
from argenta.command.flag import Flag
from argenta.command.flag.flags import Flags
from argenta.command.flag.models import PossibleValues, ValidationStatus
from argenta.response import Response


@pytest.fixture(autouse=True)
def patch_argv(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, 'argv', ['program.py'])


def _mock_input(inputs: Iterator[str]) -> str:
    return next(inputs)


# ============================================================================
# Tests for basic command execution
# ============================================================================


def test_simple_command_executes_successfully(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test'))
    def test(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('test command')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert '\ntest command\n' in output


def test_two_commands_execute_sequentially(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test", "some", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test'))
    def test(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('test command')

    @router.command(Command('some'))
    def test2(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('some command')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert re.search(r'\ntest command\n(.|\n)*\nsome command\n', output)


def test_three_commands_execute_sequentially(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test", "some", "more", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test'))
    def test(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('test command')

    @router.command(Command('some'))
    def test1(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('some command')

    @router.command(Command('more'))
    def test2(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('more command')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert re.search(r'\ntest command\n(.|\n)*\nsome command\n(.|\n)*\nmore command', output)


# ============================================================================
# Tests for custom flag handling
# ============================================================================


def test_custom_flag_without_value_is_recognized(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test --help", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()
    flag = Flag('help', prefix='--', possible_values=PossibleValues.NEITHER)

    @router.command(Command('test', flags=flag))
    def test(response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        valid_flag = response.input_flags.get_flag_by_name('help')
        if valid_flag and valid_flag.status == ValidationStatus.VALID:
            print(f'\nhelp for {valid_flag.name} flag\n')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert '\nhelp for help flag\n' in output


def test_custom_flag_with_regex_validation_accepts_valid_value(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test --port 22", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()
    flag = Flag('port', prefix='--', possible_values=re.compile(r'^\d{1,5}$'))

    @router.command(Command('test', flags=flag))
    def test(response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        valid_flag = response.input_flags.get_flag_by_name('port')
        if valid_flag and valid_flag.status == ValidationStatus.VALID:
            print(f'flag value for {valid_flag.name} flag : {valid_flag.input_value}')

    app = App(override_system_messages=True, repeat_command_groups_printing=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert '\nflag value for port flag : 22\n' in output


# ============================================================================
# Tests for predefined flag handling
# ============================================================================


def test_predefined_short_help_flag_is_recognized(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test -H", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()
    flag = PredefinedFlags.SHORT_HELP

    @router.command(Command('test', flags=flag))
    def test(response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        valid_flag = response.input_flags.get_flag_by_name('H')
        if valid_flag and valid_flag.status == ValidationStatus.VALID:
            print(f'help for {valid_flag.name} flag')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert '\nhelp for H flag\n' in output


def test_predefined_info_flag_is_recognized(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test --info", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()
    flag = PredefinedFlags.INFO

    @router.command(Command('test', flags=flag))
    def test(response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        valid_flag = response.input_flags.get_flag_by_name('info')
        if valid_flag and valid_flag.status == ValidationStatus.VALID:
            print('info about test command')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert '\ninfo about test command\n' in output


def test_predefined_host_flag_with_value_is_recognized(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test --host 192.168.0.1", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()
    flag = PredefinedFlags.HOST

    @router.command(Command('test', flags=flag))
    def test(response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        valid_flag = response.input_flags.get_flag_by_name('host')
        if valid_flag and valid_flag.status == ValidationStatus.VALID:
            print(f'connecting to host {valid_flag.input_value}')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert '\nconnecting to host 192.168.0.1\n' in output


# ============================================================================
# Tests for multiple flag handling
# ============================================================================


def test_two_predefined_flags_are_recognized_together(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test --host 192.168.32.1 --port 132", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()
    flags = Flags([PredefinedFlags.HOST, PredefinedFlags.PORT])

    @router.command(Command('test', flags=flags))
    def test(response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        host_flag = response.input_flags.get_flag_by_name('host')
        port_flag = response.input_flags.get_flag_by_name('port')
        if (host_flag and host_flag.status == ValidationStatus.VALID) and (port_flag and port_flag.status == ValidationStatus.VALID):
            print(f'connecting to host {host_flag.input_value} and port {port_flag.input_value}')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert '\nconnecting to host 192.168.32.1 and port 132\n' in output
