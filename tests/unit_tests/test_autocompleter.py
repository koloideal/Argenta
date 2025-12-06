import os

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture
from pytest_mock.plugin import MockType

from argenta.app.autocompleter.entity import (
    AutoCompleter,
    _get_history_items,
    _is_command_exist,
)


@pytest.fixture
def mock_readline(mocker: MockerFixture) -> MockType:
    _history: list[str] = []

    def add_history(item: str) -> None:
        _history.append(item)

    def get_history_item(index: int) -> str | None:
        if 1 <= index <= len(_history):
            return _history[index - 1]
        return None

    def get_current_history_length() -> int:
        return len(_history)

    def clear_history() -> None:
        _history.clear()

    mock: MockType = mocker.MagicMock()
    mocker.patch('argenta.app.autocompleter.entity.readline', mock)

    mock.reset_mock()
    clear_history()

    mock.add_history.side_effect = add_history
    mock.get_history_item.side_effect = get_history_item
    mock.get_current_history_length.side_effect = get_current_history_length
    mock.get_completer_delims.return_value = " "

    return mock


HISTORY_FILE: str = "test_history.txt"
COMMANDS: list[str] = ["start", "stop", "status"]


def test_initialization() -> None:
    completer: AutoCompleter = AutoCompleter(history_filename=HISTORY_FILE, autocomplete_button="tab")
    assert completer.history_filename == HISTORY_FILE
    assert completer.autocomplete_button == "tab"


def test_initial_setup_if_history_file_does_not_exist(fs: FakeFilesystem, mock_readline: MockType) -> None:
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

    completer: AutoCompleter = AutoCompleter(history_filename=HISTORY_FILE)
    completer.initial_setup(COMMANDS)

    mock_readline.read_history_file.assert_not_called()
    assert mock_readline.add_history.call_count == len(COMMANDS)

    mock_readline.set_completer.assert_called_with(completer._complete)
    mock_readline.parse_and_bind.assert_called_with("tab: complete")


def test_initial_setup_if_history_file_exists(fs: FakeFilesystem, mock_readline: MockType) -> None:
    fs.create_file(HISTORY_FILE, contents="previous_command\n")

    completer: AutoCompleter = AutoCompleter(history_filename=HISTORY_FILE)
    completer.initial_setup(COMMANDS)

    mock_readline.read_history_file.assert_called_once_with(HISTORY_FILE)
    mock_readline.add_history.assert_not_called()
    mock_readline.set_completer.assert_called_once()
    mock_readline.parse_and_bind.assert_called_once()


def test_initial_setup_with_no_history_filename(mock_readline: MockType) -> None:
    completer: AutoCompleter = AutoCompleter(history_filename=None)
    completer.initial_setup(COMMANDS)

    mock_readline.read_history_file.assert_not_called()
    assert mock_readline.add_history.call_count == len(COMMANDS)


def test_exit_setup_writes_and_filters_history(fs: FakeFilesystem, mock_readline: MockType) -> None:
    mock_readline.add_history.side_effect = None
    mock_readline.add_history("start server")
    mock_readline.add_history("stop client")
    mock_readline.add_history("invalid command")
    mock_readline.add_history("start server")

    raw_history_content: str = "\n".join(["start server", "stop client", "invalid command", "start server"])
    fs.create_file(HISTORY_FILE, contents=raw_history_content)

    completer: AutoCompleter = AutoCompleter(history_filename=HISTORY_FILE)
    completer.exit_setup(all_commands=["start", "stop"], ignore_command_register=False)

    mock_readline.write_history_file.assert_called_once_with(HISTORY_FILE)

    with open(HISTORY_FILE) as f:
        content: str = f.read()
        lines: list[str] = sorted(content.strip().split("\n"))
        assert lines == ["start server", "stop client"]


def test_exit_setup_with_no_history_filename(mock_readline: MockType) -> None:
    completer: AutoCompleter = AutoCompleter(history_filename=None)
    completer.exit_setup(all_commands=COMMANDS, ignore_command_register=False)
    mock_readline.write_history_file.assert_not_called()


def test_complete_with_no_matches(mock_readline: MockType) -> None:
    cmd: str
    for cmd in ["start", "stop"]:
        mock_readline.add_history(cmd)

    completer: AutoCompleter = AutoCompleter()
    assert completer._complete("run", 0) is None
    assert completer._complete("run", 1) is None


def test_complete_with_one_match(mock_readline: MockType) -> None:
    mock_readline.add_history("start server")
    mock_readline.add_history("stop server")

    completer: AutoCompleter = AutoCompleter()
    assert completer._complete("start", 0) == "start server"
    assert completer._complete("start", 1) is None


def test_complete_with_multiple_matches(mock_readline: MockType) -> None:
    mock_readline.add_history("status client")
    mock_readline.add_history("status server")
    mock_readline.add_history("stop")

    completer: AutoCompleter = AutoCompleter()

    result: str | None = completer._complete("stat", 0)
    assert result is None
    mock_readline.insert_text.assert_called_once_with("us ")
    mock_readline.redisplay.assert_called_once()

    mock_readline.reset_mock()
    result_state_1: str | None = completer._complete("stat", 1)
    assert result_state_1 is None
    mock_readline.insert_text.assert_not_called()


def test_is_command_exist() -> None:
    existing: list[str] = ["start", "stop", "status"]

    assert _is_command_exist("start", existing, ignore_command_register=False) is True
    assert _is_command_exist("START", existing, ignore_command_register=False) is False
    assert _is_command_exist("unknown", existing, ignore_command_register=False) is False

    assert _is_command_exist("start", existing, ignore_command_register=True) is True
    assert _is_command_exist("START", existing, ignore_command_register=True) is True
    assert _is_command_exist("unknown", existing, ignore_command_register=True) is False


def test_get_history_items(mock_readline: MockType) -> None:
    assert _get_history_items() == []

    mock_readline.add_history("first item")
    mock_readline.add_history("second item")

    assert _get_history_items() == ["first item", "second item"]
