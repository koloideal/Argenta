import os
from typing import Any

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture

from argenta.app.autocompleter.entity import (
    AutoCompleter,
    _get_history_items,
    _is_command_exist,
)


HISTORY_FILE: str = "test_history.txt"
COMMANDS: list[str] = ["start", "stop", "status"]


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mock_readline(mocker: MockerFixture) -> Any:
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

    mock: Any = mocker.MagicMock()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    mocker.patch('argenta.app.autocompleter.entity.readline', mock)  # pyright: ignore[reportUnknownArgumentType]

    mock.reset_mock()  # pyright: ignore[reportUnknownMemberType]
    clear_history()

    mock.add_history.side_effect = add_history  # pyright: ignore[reportUnknownMemberType]
    mock.get_history_item.side_effect = get_history_item  # pyright: ignore[reportUnknownMemberType]
    mock.get_current_history_length.side_effect = get_current_history_length  # pyright: ignore[reportUnknownMemberType]
    mock.get_completer_delims.return_value = " "  # pyright: ignore[reportUnknownMemberType]

    return mock  # pyright: ignore[reportReturnType, reportUnknownVariableType]


# ============================================================================
# Tests for AutoCompleter initialization
# ============================================================================


def test_autocompleter_initializes_with_history_file_and_button() -> None:
    completer: AutoCompleter = AutoCompleter(history_filename=HISTORY_FILE, autocomplete_button="tab")
    assert completer.history_filename == HISTORY_FILE
    assert completer.autocomplete_button == "tab"


# ============================================================================
# Tests for initial setup
# ============================================================================


def test_initial_setup_creates_history_when_file_does_not_exist(fs: FakeFilesystem, mock_readline: Any) -> None:
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

    completer: AutoCompleter = AutoCompleter(history_filename=HISTORY_FILE)
    completer.initial_setup(COMMANDS)

    mock_readline.read_history_file.assert_not_called()
    assert mock_readline.add_history.call_count == len(COMMANDS)

    mock_readline.set_completer.assert_called_with(completer._complete)
    mock_readline.parse_and_bind.assert_called_with("tab: complete")


def test_initial_setup_reads_existing_history_file(fs: FakeFilesystem, mock_readline: Any) -> None:
    fs.create_file(HISTORY_FILE, contents="previous_command\n")  # pyright: ignore[reportUnknownMemberType]

    completer: AutoCompleter = AutoCompleter(history_filename=HISTORY_FILE)
    completer.initial_setup(COMMANDS)

    mock_readline.read_history_file.assert_called_once_with(HISTORY_FILE)
    mock_readline.add_history.assert_not_called()
    mock_readline.set_completer.assert_called_once()
    mock_readline.parse_and_bind.assert_called_once()


def test_initial_setup_works_without_history_filename(mock_readline: Any) -> None:
    completer: AutoCompleter = AutoCompleter(history_filename=None)
    completer.initial_setup(COMMANDS)

    mock_readline.read_history_file.assert_not_called()
    assert mock_readline.add_history.call_count == len(COMMANDS)


# ============================================================================
# Tests for exit setup and history filtering
# ============================================================================


def test_exit_setup_writes_and_filters_duplicate_commands(fs: FakeFilesystem, mock_readline: Any) -> None:
    mock_readline.add_history.side_effect = None
    mock_readline.add_history("start server")
    mock_readline.add_history("stop client")
    mock_readline.add_history("invalid command")
    mock_readline.add_history("start server")

    raw_history_content: str = "\n".join(["start server", "stop client", "invalid command", "start server"])
    fs.create_file(HISTORY_FILE, contents=raw_history_content)  # pyright: ignore[reportUnknownMemberType]

    completer: AutoCompleter = AutoCompleter(history_filename=HISTORY_FILE)
    completer.exit_setup(all_commands=["start", "stop"], ignore_command_register=False)

    mock_readline.write_history_file.assert_called_once_with(HISTORY_FILE)

    with open(HISTORY_FILE) as f:
        content: str = f.read()
        lines: list[str] = sorted(content.strip().split("\n"))
        assert lines == ["start server", "stop client"]


def test_exit_setup_skips_writing_when_no_history_filename(mock_readline: Any) -> None:
    completer: AutoCompleter = AutoCompleter(history_filename=None)
    completer.exit_setup(all_commands=COMMANDS, ignore_command_register=False)
    mock_readline.write_history_file.assert_not_called()


# ============================================================================
# Tests for autocomplete functionality
# ============================================================================


def test_complete_returns_none_when_no_matches_found(mock_readline: Any) -> None:
    cmd: str
    for cmd in ["start", "stop"]:
        mock_readline.add_history(cmd)

    completer: AutoCompleter = AutoCompleter()
    assert completer._complete("run", 0) is None
    assert completer._complete("run", 1) is None


def test_complete_returns_single_match(mock_readline: Any) -> None:
    mock_readline.add_history("start server")
    mock_readline.add_history("stop server")

    completer: AutoCompleter = AutoCompleter()
    assert completer._complete("start", 0) == "start server"
    assert completer._complete("start", 1) is None


def test_complete_inserts_common_prefix_for_multiple_matches(mock_readline: Any) -> None:
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


# ============================================================================
# Tests for helper functions
# ============================================================================


def test_is_command_exist_checks_case_sensitive_when_enabled() -> None:
    existing: list[str] = ["start", "stop", "status"]

    assert _is_command_exist("start", existing, ignore_command_register=False) is True
    assert _is_command_exist("START", existing, ignore_command_register=False) is False
    assert _is_command_exist("unknown", existing, ignore_command_register=False) is False


def test_is_command_exist_checks_case_insensitive_when_enabled() -> None:
    existing: list[str] = ["start", "stop", "status"]

    assert _is_command_exist("start", existing, ignore_command_register=True) is True
    assert _is_command_exist("START", existing, ignore_command_register=True) is True
    assert _is_command_exist("unknown", existing, ignore_command_register=True) is False


def test_get_history_items_returns_empty_list_initially(mock_readline: Any) -> None:
    assert _get_history_items() == []


def test_get_history_items_returns_all_added_items(mock_readline: Any) -> None:
    mock_readline.add_history("first item")
    mock_readline.add_history("second item")

    assert _get_history_items() == ["first item", "second item"]
