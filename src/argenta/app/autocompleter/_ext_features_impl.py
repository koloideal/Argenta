__all__ = ['build_session', 'do_prompt']

from typing import Callable, Iterable

from prompt_toolkit import HTML, PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import CompleteEvent, Completer, Completion, ThreadedCompleter
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.history import FileHistory, History, InMemoryHistory, ThreadedHistory
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles import Style


class CommandLexer(Lexer):
    def __init__(self, valid_commands: set[str]) -> None:
        self.valid_commands: set[str] = valid_commands

    def lex_document(self, document: Document) -> Callable[[int], StyleAndTextTuples]:
        def get_line_tokens(lineno: int) -> StyleAndTextTuples:
            if lineno >= len(document.lines):
                return []

            line_text: str = document.lines[lineno]

            if not line_text.strip():
                return [("", line_text)]

            first_word: str = line_text.split()[0] if line_text.split() else ""

            if first_word in self.valid_commands:
                return [("class:valid", line_text)]
            else:
                return [("class:invalid", line_text)]

        return get_line_tokens


class HistoryCompleter(Completer):
    def __init__(self, history_container: History, static_commands: set[str]) -> None:
        self.history_container: History = history_container
        self.static_commands: set[str] = static_commands

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        text: str = document.text_before_cursor
        history_items: set[str] = set(self.history_container.load_history_strings())
        all_candidates: set[str] = history_items.union(self.static_commands)
        matches: list[str] = sorted(cmd for cmd in all_candidates if cmd.startswith(text))

        if not matches:
            return

        for match in matches:
            yield Completion(match, start_position=-len(text), display=match)

    @staticmethod
    def _find_common_prefix(matches: list[str]) -> str:
        if not matches:
            return ""
        common: str = matches[0]
        for match in matches[1:]:
            i: int = 0
            while i < len(common) and i < len(match) and common[i] == match[i]:
                i += 1
            common = common[:i]
        return common


def build_session(
    history_filename: str | None,
    autocomplete_button: str,
    command_highlighting: bool,
    auto_suggestions: bool,
    all_commands: set[str],
) -> PromptSession[str]:
    kb = KeyBindings()

    def _(event: KeyPressEvent) -> None:
        buff = event.app.current_buffer
        if buff.complete_state:
            buff.complete_next()
            return
        comps_gen = iter(buff.completer.get_completions(buff.document, CompleteEvent()))
        try:
            first = next(comps_gen)
        except StopIteration:
            return
        try:
            _ = next(comps_gen)
            buff.start_completion(select_first=False)
        except StopIteration:
            buff.apply_completion(first)

    kb.add(autocomplete_button)(_)

    history: InMemoryHistory | ThreadedHistory
    if history_filename:
        history = ThreadedHistory(FileHistory(history_filename))
    else:
        history = InMemoryHistory()

    style = Style.from_dict({"valid": "#00ff00", "invalid": "#ff0000"})
    return PromptSession(
        history=history,
        completer=ThreadedCompleter(HistoryCompleter(history, all_commands)),
        complete_while_typing=False,
        key_bindings=kb,
        auto_suggest=AutoSuggestFromHistory() if auto_suggestions else None,
        style=style if command_highlighting else None,
        lexer=CommandLexer(all_commands) if command_highlighting else None,
    )


def do_prompt(session: PromptSession[str], prompt_text: str | HTML) -> str:
    return session.prompt(
        HTML(prompt_text) if isinstance(prompt_text, str) else prompt_text,
        cursor=CursorShape.BLINKING_BEAM,
    )
