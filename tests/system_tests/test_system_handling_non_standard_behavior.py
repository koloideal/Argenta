import re
import sys
from collections.abc import Iterator

import pytest

from argenta import App, Orchestrator, Router
from argenta.command import Command, PredefinedFlags
from argenta.command.flag.flags.models import Flags
from argenta.command.flag.models import ValidationStatus
from argenta.response import Response


@pytest.fixture(autouse=True)
def patch_argv(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, 'argv', ['program.py'])


def _mock_input(inputs: Iterator[str]) -> str:
    return next(inputs)


# ============================================================================
# Tests for empty input handling
# ============================================================================


def test_empty_input_triggers_empty_command_handler(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test'))
    def test(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('test command')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    app.set_empty_command_handler(lambda: print('Empty input command'))
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert "\nEmpty input command\n" in output


# ============================================================================
# Tests for unknown command handling
# ============================================================================


def test_unknown_command_triggers_unknown_command_handler(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["help", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test'))
    def test(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('test command')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    app.set_unknown_command_handler(lambda command: print(f'Unknown command: {command.trigger}'))
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert "\nUnknown command: help\n" in output


def test_mixed_valid_and_unknown_commands_handled_correctly(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test", "some", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test'))
    def test(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('test command')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    app.set_unknown_command_handler(lambda command: print(f'Unknown command: {command.trigger}'))
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert re.search(r'\ntest command\n(.|\n)*\nUnknown command: some', output)


def test_multiple_commands_with_unknown_command_in_between(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test", "some", "more", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test'))
    def test(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('test command')

    @router.command(Command('more'))
    def test1(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('more command')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    app.set_unknown_command_handler(lambda command: print(f'Unknown command: {command.trigger}'))
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert re.search(r'\ntest command\n(.|\n)*\nUnknown command: some\n(.|\n)*\nmore command', output)


# ============================================================================
# Tests for unregistered flag handling
# ============================================================================


def test_unregistered_flag_without_value_is_accessible(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test --help", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test'))
    def test(response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        undefined_flag = response.input_flags.get_flag_by_name('help')
        if undefined_flag and undefined_flag.status == ValidationStatus.UNDEFINED:
            print(f'test command with undefined flag: {undefined_flag.string_entity}')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert '\ntest command with undefined flag: --help\n' in output


def test_unregistered_flag_with_value_is_accessible(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test --port 22", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test'))
    def test(response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        undefined_flag = response.input_flags.get_flag_by_name("port")
        if undefined_flag and undefined_flag.status == ValidationStatus.UNDEFINED:
            print(f'test command with undefined flag with value: {undefined_flag.string_entity} {undefined_flag.input_value}')
        else:
            raise

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert '\ntest command with undefined flag with value: --port 22\n' in output


def test_registered_and_unregistered_flags_coexist(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test --host 192.168.32.1 --port 132", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()
    flags = Flags([PredefinedFlags.HOST])

    @router.command(Command('test', flags=flags))
    def test(response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        undefined_flag = response.input_flags.get_flag_by_name("port")
        if undefined_flag and undefined_flag.status == ValidationStatus.UNDEFINED:
            print(f'connecting to host with flag: {undefined_flag.string_entity} {undefined_flag.input_value}')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert '\nconnecting to host with flag: --port 132\n' in output


# ============================================================================
# Tests for incorrect flag syntax handling
# ============================================================================


def test_flag_without_value_triggers_incorrect_syntax_handler(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test 535 --port", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test'))
    def test(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('test command')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    app.set_incorrect_input_syntax_handler(lambda command: print(f'Incorrect flag syntax: "{command}"'))
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert "\nIncorrect flag syntax: \"test 535 --port\"\n" in output


# ============================================================================
# Tests for repeated flag handling
# ============================================================================


def test_repeated_flags_trigger_repeated_flags_handler(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = iter(["test --port 22 --port 33", "q"])
    monkeypatch.setattr('builtins.input', lambda _prompt="": _mock_input(inputs))
    
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command('test', flags=PredefinedFlags.PORT))
    def test(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
        print('test command')

    app = App(override_system_messages=True, print_func=print)
    app.include_router(router)
    app.set_repeated_input_flags_handler(lambda command: print(f'Repeated input flags: "{command}"'))
    orchestrator.start_polling(app)

    output = capsys.readouterr().out

    assert 'Repeated input flags: "test --port 22 --port 33"' in output
