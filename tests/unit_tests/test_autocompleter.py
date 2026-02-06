import os
import sys
import tempfile
from typing import Any, Callable
from unittest.mock import MagicMock, patch

import pytest
from prompt_toolkit import HTML
from prompt_toolkit.completion import CompleteEvent
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
    
    completions = list(completer.get_completions(doc, CompleteEvent()))
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
    
    completions = list(completer.get_completions(doc, CompleteEvent()))
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
    
    completions = list(completer.get_completions(doc, CompleteEvent()))
    assert len(completions) == 0


def test_history_completer_deduplicates_commands() -> None:
    history = InMemoryHistory()
    history.append_string("start")
    history.append_string("start")
    
    completer = HistoryCompleter(history, {"start"})
    doc = Document("sta")
    
    completions = list(completer.get_completions(doc, CompleteEvent()))
    assert len(completions) == 1


def test_history_completer_sorts_results() -> None:
    history = InMemoryHistory()
    history.append_string("stop")
    history.append_string("start")
    history.append_string("status")
    
    completer = HistoryCompleter(history, set())
    doc = Document("st")
    
    completions = list(completer.get_completions(doc, CompleteEvent()))
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


def test_command_lexer_handles_out_of_range_lineno() -> None:
    lexer = CommandLexer({"start", "stop"})
    doc = Document("start")
    get_line_tokens = lexer.lex_document(doc)
    tokens = get_line_tokens(1)
    assert tokens == []


def test_history_completer_returns_early_when_no_matches() -> None:
    history = InMemoryHistory()
    completer = HistoryCompleter(history, {"start", "stop"})
    doc = Document("xyz")
    
    result = completer.get_completions(doc, CompleteEvent())
    completions = list(result)
    assert completions == []


def test_autocompleter_initial_setup_with_commands() -> None:
    completer = AutoCompleter()
    
    with patch.object(sys.stdin, 'isatty', return_value=True), \
         patch('argenta.app.autocompleter.entity.PromptSession') as mock_session:
        completer.initial_setup({"start", "stop", "status"})
    
    assert completer._session is not None
    assert completer._fallback_mode is False
    mock_session.assert_called_once()


def test_autocompleter_initial_setup_with_history_file() -> None:
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        history_file = f.name
    
    try:
        completer = AutoCompleter(history_filename=history_file)
        
        with patch.object(sys.stdin, 'isatty', return_value=True), \
             patch('argenta.app.autocompleter.entity.PromptSession'), \
             patch('argenta.app.autocompleter.entity.ThreadedHistory') as mock_threaded_history:
            completer.initial_setup({"start", "stop"})
        
        assert completer._session is not None
        assert completer._fallback_mode is False
        mock_threaded_history.assert_called_once()
    finally:
        if os.path.exists(history_file):
            os.unlink(history_file)


def test_autocompleter_initial_setup_without_history_file() -> None:
    completer = AutoCompleter(history_filename=None)
    
    with patch.object(sys.stdin, 'isatty', return_value=True), \
         patch('argenta.app.autocompleter.entity.PromptSession'), \
         patch('argenta.app.autocompleter.entity.InMemoryHistory') as mock_in_memory:
        completer.initial_setup({"start", "stop"})
    
    assert completer._session is not None
    assert completer._fallback_mode is False
    mock_in_memory.assert_called_once()


def test_autocompleter_initial_setup_with_custom_autocomplete_button() -> None:
    completer = AutoCompleter(autocomplete_button="c-space")
    
    with patch.object(sys.stdin, 'isatty', return_value=True), \
         patch('argenta.app.autocompleter.entity.PromptSession'):
        completer.initial_setup({"start", "stop"})
    
    assert completer._session is not None
    assert completer.autocomplete_button == "c-space"


def test_autocompleter_initial_setup_without_auto_suggestions() -> None:
    completer = AutoCompleter(auto_suggestions=False)
    
    with patch.object(sys.stdin, 'isatty', return_value=True), \
         patch('argenta.app.autocompleter.entity.PromptSession') as mock_session:
        completer.initial_setup({"start", "stop"})
    
    assert completer._session is not None
    call_kwargs = mock_session.call_args[1]
    assert call_kwargs['auto_suggest'] is None


def test_autocompleter_initial_setup_without_command_highlighting() -> None:
    completer = AutoCompleter(command_highlighting=False)
    
    with patch.object(sys.stdin, 'isatty', return_value=True), \
         patch('argenta.app.autocompleter.entity.PromptSession') as mock_session:
        completer.initial_setup({"start", "stop"})
    
    assert completer._session is not None
    call_kwargs = mock_session.call_args[1]
    assert call_kwargs['style'] is None
    assert call_kwargs['lexer'] is None


def test_autocompleter_key_binding_handler_with_complete_state() -> None:
    completer = AutoCompleter()
    
    captured_handler: Callable[[Any], None] | None = None
    
    def capture_kb_add(key: str) -> Callable[[Callable[[Any], None]], Callable[[Any], None]]:
        def decorator(func: Callable[[Any], None]) -> Callable[[Any], None]:
            nonlocal captured_handler
            captured_handler = func
            return func
        return decorator
    
    with patch.object(sys.stdin, 'isatty', return_value=True), \
         patch('argenta.app.autocompleter.entity.PromptSession'), \
         patch('argenta.app.autocompleter.entity.KeyBindings') as mock_kb_class:
        
        mock_kb = MagicMock()
        mock_kb.add = capture_kb_add
        mock_kb_class.return_value = mock_kb
        
        completer.initial_setup({"start", "stop"})
    
    assert captured_handler is not None
    
    mock_event = MagicMock()
    mock_buff = MagicMock()
    mock_buff.complete_state = True
    mock_event.app.current_buffer = mock_buff
    
    captured_handler(mock_event)
    
    mock_buff.complete_next.assert_called_once()


def test_autocompleter_key_binding_handler_no_completions() -> None:
    completer = AutoCompleter()
    
    captured_handler: Callable[[Any], None] | None = None
    
    def capture_kb_add(key: str) -> Callable[[Callable[[Any], None]], Callable[[Any], None]]:
        def decorator(func: Callable[[Any], None]) -> Callable[[Any], None]:
            nonlocal captured_handler
            captured_handler = func
            return func
        return decorator
    
    with patch.object(sys.stdin, 'isatty', return_value=True), \
         patch('argenta.app.autocompleter.entity.PromptSession'), \
         patch('argenta.app.autocompleter.entity.KeyBindings') as mock_kb_class:
        
        mock_kb = MagicMock()
        mock_kb.add = capture_kb_add
        mock_kb_class.return_value = mock_kb
        
        completer.initial_setup({"start", "stop"})
    
    mock_event = MagicMock()
    mock_buff = MagicMock()
    mock_buff.complete_state = False
    mock_completer = MagicMock()
    mock_completer.get_completions.return_value = iter([])
    mock_buff.completer = mock_completer
    mock_event.app.current_buffer = mock_buff
    
    assert captured_handler is not None
    captured_handler(mock_event)
    
    mock_buff.start_completion.assert_not_called()
    mock_buff.apply_completion.assert_not_called()


def test_autocompleter_key_binding_handler_single_completion() -> None:
    completer = AutoCompleter()
    
    captured_handler: Callable[[Any], None] | None = None
    
    def capture_kb_add(key: str) -> Callable[[Callable[[Any], None]], Callable[[Any], None]]:
        def decorator(func: Callable[[Any], None]) -> Callable[[Any], None]:
            nonlocal captured_handler
            captured_handler = func
            return func
        return decorator
    
    with patch.object(sys.stdin, 'isatty', return_value=True), \
         patch('argenta.app.autocompleter.entity.PromptSession'), \
         patch('argenta.app.autocompleter.entity.KeyBindings') as mock_kb_class:
        
        mock_kb = MagicMock()
        mock_kb.add = capture_kb_add
        mock_kb_class.return_value = mock_kb
        
        completer.initial_setup({"start", "stop"})
    
    mock_event = MagicMock()
    mock_buff = MagicMock()
    mock_buff.complete_state = False
    mock_completion = MagicMock()
    mock_completer = MagicMock()
    mock_completer.get_completions.return_value = iter([mock_completion])
    mock_buff.completer = mock_completer
    mock_event.app.current_buffer = mock_buff
    
    assert captured_handler is not None
    captured_handler(mock_event)
    
    mock_buff.apply_completion.assert_called_once_with(mock_completion)
    mock_buff.start_completion.assert_not_called()


def test_autocompleter_key_binding_handler_multiple_completions() -> None:
    completer = AutoCompleter()
    
    captured_handler: Callable[[Any], None] | None = None
    
    def capture_kb_add(key: str) -> Callable[[Callable[[Any], None]], Callable[[Any], None]]:
        def decorator(func: Callable[[Any], None]) -> Callable[[Any], None]:
            nonlocal captured_handler
            captured_handler = func
            return func
        return decorator
    
    with patch.object(sys.stdin, 'isatty', return_value=True), \
         patch('argenta.app.autocompleter.entity.PromptSession'), \
         patch('argenta.app.autocompleter.entity.KeyBindings') as mock_kb_class:
        
        mock_kb = MagicMock()
        mock_kb.add = capture_kb_add
        mock_kb_class.return_value = mock_kb
        
        completer.initial_setup({"start", "stop"})
    
    mock_event = MagicMock()
    mock_buff = MagicMock()
    mock_buff.complete_state = False
    mock_completion1 = MagicMock()
    mock_completion2 = MagicMock()
    mock_completer = MagicMock()
    mock_completer.get_completions.return_value = iter([mock_completion1, mock_completion2])
    mock_buff.completer = mock_completer
    mock_event.app.current_buffer = mock_buff
    
    assert captured_handler is not None
    captured_handler(mock_event)
    
    mock_buff.start_completion.assert_called_once_with(select_first=False)
    mock_buff.apply_completion.assert_not_called()


def test_autocompleter_prompt_in_fallback_mode_with_string() -> None:
    completer = AutoCompleter()
    
    with patch.object(sys.stdin, 'isatty', return_value=False):
        completer.initial_setup({"start", "stop"})
    
    assert completer._fallback_mode is True
    
    with patch('builtins.input', return_value='test input'):
        result = completer.prompt(">>> ")
    
    assert result == 'test input'


def test_autocompleter_prompt_in_fallback_mode_with_html() -> None:
    completer = AutoCompleter()
    
    with patch.object(sys.stdin, 'isatty', return_value=False):
        completer.initial_setup({"start", "stop"})
    
    assert completer._fallback_mode is True
    
    with patch('builtins.input', return_value='test input'):
        result = completer.prompt(HTML("<b>>>> </b>"))
    
    assert result == 'test input'


def test_autocompleter_prompt_with_html_in_normal_mode() -> None:
    completer = AutoCompleter()
    
    mock_session = MagicMock()
    mock_session.prompt.return_value = 'test result'
    completer._session = mock_session
    completer._fallback_mode = False
    
    html_prompt = HTML("<b>>>> </b>")
    result = completer.prompt(html_prompt)
    
    assert result == 'test result'
    mock_session.prompt.assert_called_once()
    call_args = mock_session.prompt.call_args
    assert call_args[0][0] == html_prompt


def test_autocompleter_prompt_with_string_in_normal_mode() -> None:
    completer = AutoCompleter()
    
    mock_session = MagicMock()
    mock_session.prompt.return_value = 'test result'
    completer._session = mock_session
    completer._fallback_mode = False
    
    result = completer.prompt(">>> ")
    
    assert result == 'test result'
    mock_session.prompt.assert_called_once()
    call_args = mock_session.prompt.call_args
    assert isinstance(call_args[0][0], HTML)
