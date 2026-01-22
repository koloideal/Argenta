import pytest
from prompt_toolkit.document import Document
from prompt_toolkit.history import InMemoryHistory

from argenta.app.autocompleter.entity import (
    AutoCompleter,
    CommandLexer,
    HistoryCompleter
)


COMMANDS: set[str] = {"start", "stop", "status"}


def test_autocompleter_initializes_with_default_params() -> None:
    completer = AutoCompleter()
    assert completer.history_filename is None
    assert completer.autocomplete_button == "tab"
    assert completer.command_highlighting is True
    assert completer.auto_suggestions is True


def test_autocompleter_initializes_with_custom_params() -> None:
    completer = AutoCompleter(
        history_filename="test.txt",
        autocomplete_button="c-space",
        command_highlighting=False,
        auto_suggestions=False
    )
    assert completer.history_filename == "test.txt"
    assert completer.autocomplete_button == "c-space"
    assert completer.command_highlighting is False
    assert completer.auto_suggestions is False


def test_prompt_raises_error_without_initial_setup() -> None:
    completer = AutoCompleter()
    with pytest.raises(RuntimeError, match="Call initial_setup"):
        completer.prompt(">>> ")


def test_command_lexer_highlights_valid_command() -> None:
    lexer = CommandLexer({"start", "stop"})
    doc = Document("start server")
    tokens = lexer.lex_document(doc)(0)
    assert tokens == [("class:valid", "start server")]


def test_command_lexer_highlights_invalid_command() -> None:
    lexer = CommandLexer({"start", "stop"})
    doc = Document("invalid command")
    tokens = lexer.lex_document(doc)(0)
    assert tokens == [("class:invalid", "invalid command")]


def test_command_lexer_handles_empty_line() -> None:
    lexer = CommandLexer({"start", "stop"})
    doc = Document("")
    tokens = lexer.lex_document(doc)(0)
    assert tokens == [("", "")]


def test_command_lexer_handles_whitespace_only() -> None:
    lexer = CommandLexer({"start", "stop"})
    doc = Document("   ")
    tokens = lexer.lex_document(doc)(0)
    assert tokens == [("", "   ")]


def test_history_completer_returns_matching_commands() -> None:
    history = InMemoryHistory()
    history.append_string("start server")
    history.append_string("stop server")
    
    completer = HistoryCompleter(history, {"status"})
    doc = Document("sta")
    
    completions = list(completer.get_completions(doc, None))
    completion_texts = [c.text for c in completions]
    
    assert "start server" in completion_texts
    assert "status" in completion_texts
    assert "stop server" not in completion_texts


def test_history_completer_returns_all_when_empty_input() -> None:
    history = InMemoryHistory()
    history.append_string("start")
    history.append_string("stop")
    
    completer = HistoryCompleter(history, {"status"})
    doc = Document("")
    
    completions = list(completer.get_completions(doc, None))
    completion_texts = [c.text for c in completions]
    
    assert len(completion_texts) == 3
    assert "start" in completion_texts
    assert "stop" in completion_texts
    assert "status" in completion_texts


def test_history_completer_returns_empty_when_no_matches() -> None:
    history = InMemoryHistory()
    history.append_string("start")
    
    completer = HistoryCompleter(history, {"stop"})
    doc = Document("xyz")
    
    completions = list(completer.get_completions(doc, None))
    assert len(completions) == 0


def test_history_completer_deduplicates_commands() -> None:
    history = InMemoryHistory()
    history.append_string("start")
    history.append_string("start")
    
    completer = HistoryCompleter(history, {"start"})
    doc = Document("sta")
    
    completions = list(completer.get_completions(doc, None))
    assert len(completions) == 1


def test_history_completer_sorts_results() -> None:
    history = InMemoryHistory()
    history.append_string("stop")
    history.append_string("start")
    history.append_string("status")
    
    completer = HistoryCompleter(history, set())
    doc = Document("st")
    
    completions = list(completer.get_completions(doc, None))
    completion_texts = [c.text for c in completions]
    
    assert completion_texts == ["start", "status", "stop"]


def test_find_common_prefix_with_multiple_matches() -> None:
    matches = ["start server", "start client", "start process"]
    prefix = HistoryCompleter._find_common_prefix(matches)
    assert prefix == "start "


def test_find_common_prefix_with_no_common() -> None:
    matches = ["start", "stop", "status"]
    prefix = HistoryCompleter._find_common_prefix(matches)
    assert prefix == "st"


def test_find_common_prefix_with_single_match() -> None:
    matches = ["start"]
    prefix = HistoryCompleter._find_common_prefix(matches)
    assert prefix == "start"


def test_find_common_prefix_with_empty_list() -> None:
    matches: list[str] = []
    prefix = HistoryCompleter._find_common_prefix(matches)
    assert prefix == ""
