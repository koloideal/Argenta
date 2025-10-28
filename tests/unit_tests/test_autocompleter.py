import os
from unittest.mock import MagicMock, call, patch

import pytest

# Since readline is not available on all platforms (e.g., Windows) for testing,
# it is mocked for all tests.
readline_mock = MagicMock()

# We patch the module where it's imported, not where it's defined.
@pytest.fixture
def mock_readline():
    """Fixture to provide a mock of the `readline` module."""
    with patch('argenta.app.autocompleter.entity.readline', readline_mock) as mock:
        # This nested state simulates readline's internal history list.
        _history = []

        def add_history(item: str) -> None:
            _history.append(item)

        def get_history_item(index: int) -> str | None:
            # readline history is 1-based.
            if 1 <= index <= len(_history):
                return _history[index - 1]
            return None

        def get_current_history_length() -> int:
            return len(_history)

        def clear_history() -> None:
            _history.clear()

        # Reset all mocks and the internal history before each test.
        mock.reset_mock()
        clear_history()

        # Apply side effects to mock functions to simulate real behavior.
        mock.add_history.side_effect = add_history
        mock.get_history_item.side_effect = get_history_item
        mock.get_current_history_length.side_effect = get_current_history_length

        # Provide a default return value for functions that are read from.
        mock.get_completer_delims.return_value = " "

        yield mock

# We import the class under test after setting up the patch context if needed,
# or ensure patches target the correct import location.
from argenta.app.autocompleter.entity import (AutoCompleter,
                                              _get_history_items,
                                              _is_command_exist)


class TestAutoCompleter:
    """Test suite for the AutoCompleter class."""
    HISTORY_FILE = "test_history.txt"
    COMMANDS = ["start", "stop", "status"]

    def test_initialization(self):
        """Tests that the constructor correctly assigns attributes."""
        completer = AutoCompleter(history_filename=self.HISTORY_FILE, autocomplete_button="tab")
        assert completer.history_filename == self.HISTORY_FILE
        assert completer.autocomplete_button == "tab"

    def test_initial_setup_if_history_file_does_not_exist(self, fs, mock_readline):
        """Tests initial setup creates history from commands when the history file is absent."""
        # Ensure the file does not exist in the fake filesystem.
        if os.path.exists(self.HISTORY_FILE):
            os.remove(self.HISTORY_FILE)

        completer = AutoCompleter(history_filename=self.HISTORY_FILE)
        completer.initial_setup(self.COMMANDS)

        mock_readline.read_history_file.assert_not_called()
        expected_calls = [call(cmd) for cmd in self.COMMANDS]
        mock_readline.add_history.assert_has_calls(expected_calls, any_order=True)
        assert mock_readline.add_history.call_count == len(self.COMMANDS)

        mock_readline.set_completer.assert_called_with(completer._complete)
        mock_readline.parse_and_bind.assert_called_with("tab: complete")

    def test_initial_setup_if_history_file_exists(self, fs, mock_readline):
        """Tests initial setup reads from an existing history file."""
        fs.create_file(self.HISTORY_FILE, contents="previous_command\n")

        completer = AutoCompleter(history_filename=self.HISTORY_FILE)
        completer.initial_setup(self.COMMANDS)

        mock_readline.read_history_file.assert_called_once_with(self.HISTORY_FILE)
        mock_readline.add_history.assert_not_called()
        mock_readline.set_completer.assert_called_once()
        mock_readline.parse_and_bind.assert_called_once()

    def test_initial_setup_with_no_history_filename(self, mock_readline):
        """Tests initial setup when no history filename is provided."""
        completer = AutoCompleter(history_filename=None)
        completer.initial_setup(self.COMMANDS)

        mock_readline.read_history_file.assert_not_called()
        expected_calls = [call(cmd) for cmd in self.COMMANDS]
        mock_readline.add_history.assert_has_calls(expected_calls, any_order=True)

    def test_exit_setup_writes_and_filters_history(self, fs, mock_readline):
        """Tests that exit_setup writes a filtered and unique history to the file."""
        # 1. Populate the mock readline history.
        mock_readline.add_history.side_effect(None) # Temporarily disable side effect to just record calls
        mock_readline.add_history("start server")
        mock_readline.add_history("stop client")
        mock_readline.add_history("invalid command")
        mock_readline.add_history("start server")  # Add a duplicate.

        # 2. Simulate the state of the history file after readline.write_history_file would have run.
        raw_history_content = "\n".join(["start server", "stop client", "invalid command", "start server"])
        fs.create_file(self.HISTORY_FILE, contents=raw_history_content)

        # 3. Call the method under test.
        completer = AutoCompleter(history_filename=self.HISTORY_FILE)
        completer.exit_setup(all_commands=["start", "stop"], ignore_command_register=False)

        # 4. Assert that readline's write function was called.
        mock_readline.write_history_file.assert_called_once_with(self.HISTORY_FILE)

        # 5. Assert the file was correctly re-written with filtered and unique content.
        with open(self.HISTORY_FILE, "r") as f:
            content = f.read()
            lines = sorted(content.strip().split("\n"))
            assert lines == ["start server", "stop client"]

    def test_exit_setup_with_no_history_filename(self, mock_readline):
        """Tests that exit_setup does nothing if no filename is provided."""
        completer = AutoCompleter(history_filename=None)
        completer.exit_setup(all_commands=self.COMMANDS, ignore_command_register=False)
        mock_readline.write_history_file.assert_not_called()

    def test_complete_with_no_matches(self, mock_readline):
        """Tests the _complete method when there are no matching history items."""
        for cmd in ["start", "stop"]:
            mock_readline.add_history(cmd)

        completer = AutoCompleter()
        assert completer._complete("run", 0) is None
        assert completer._complete("run", 1) is None

    def test_complete_with_one_match(self, mock_readline):
        """Tests the _complete method when there is exactly one match."""
        mock_readline.add_history("start server")
        mock_readline.add_history("stop server")

        completer = AutoCompleter()
        assert completer._complete("start", 0) == "start server"
        assert completer._complete("start", 1) is None  # Subsequent states yield no matches

    def test_complete_with_multiple_matches(self, mock_readline):
        """Tests _complete with multiple matches that share a common prefix."""
        mock_readline.add_history("status client")
        mock_readline.add_history("status server")
        mock_readline.add_history("stop")

        completer = AutoCompleter()

        # On state 0, it should insert the common prefix via readline and return None.
        result = completer._complete("stat", 0)
        assert result is None
        mock_readline.insert_text.assert_called_once_with("us ")  # Completes "stat" to "status "
        mock_readline.redisplay.assert_called_once()

        # On subsequent states, it should do nothing.
        mock_readline.reset_mock()
        result_state_1 = completer._complete("stat", 1)
        assert result_state_1 is None
        mock_readline.insert_text.assert_not_called()


class TestHelperFunctions:
    """Test suite for helper functions in the autocompleter module."""

    def test_is_command_exist(self):
        """Tests the _is_command_exist helper function."""
        existing = ["start", "stop", "status"]

        # Case-sensitive check
        assert _is_command_exist("start", existing, ignore_command_register=False) is True
        assert _is_command_exist("START", existing, ignore_command_register=False) is False
        assert _is_command_exist("unknown", existing, ignore_command_register=False) is False

        # Case-insensitive check
        assert _is_command_exist("start", existing, ignore_command_register=True) is True
        assert _is_command_exist("START", existing, ignore_command_register=True) is True
        assert _is_command_exist("unknown", existing, ignore_command_register=True) is False

    def test_get_history_items(self, mock_readline):
        """Tests the _get_history_items helper function."""
        assert _get_history_items() == []

        mock_readline.add_history("first item")
        mock_readline.add_history("second item")

        assert _get_history_items() == ["first item", "second item"]
