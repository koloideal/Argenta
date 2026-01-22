__all__ = ["AutoCompleter"]

from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.history import History, ThreadedHistory, FileHistory, InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings


class HistoryCompleter(Completer):
    def __init__(self, history_container: History, static_commands: set[str]) -> None:
        self.history_container: History = history_container
        self.static_commands: set[str] = static_commands

    def get_completions(self, document: Document, complete_event):
        text: str = document.text_before_cursor
        history_items: set[str] = set(self.history_container.load_history_strings())
        all_candidates: set[str] = history_items.union(self.static_commands)
        matches: list[str] = sorted(cmd for cmd in all_candidates if cmd.startswith(text))

        if not matches:
            return

        for match in matches:
            yield Completion(
                match,
                start_position=-len(text),
                display=match
            )

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


class AutoCompleter:
    def __init__(
            self,
            history_filename: str | None = None,
            autocomplete_button: str = "tab"
    ) -> None:
        self.history_filename: str | None = history_filename
        self.autocomplete_button: str = autocomplete_button
        self._session: PromptSession | None = None

    def initial_setup(self, all_commands: set[str]) -> None:
        kb = KeyBindings()

        def _(event):
            buff = event.app.current_buffer

            if buff.complete_state:
                buff.complete_next()
            else:
                completions = list(buff.completer.get_completions(buff.document, None))
                if len(completions) == 1:
                    buff.apply_completion(completions[0])
                else:
                    buff.start_completion(select_first=False)

        kb.add(self.autocomplete_button)(_)

        if self.history_filename:
            history = FileHistory(self.history_filename)
            history = ThreadedHistory(history)
        else:
            history = InMemoryHistory()

        self._session = PromptSession(
            history=history,
            completer=HistoryCompleter(history, all_commands),
            complete_while_typing=False,
            key_bindings=kb,
        )

    def prompt(self, prompt_text: str | HTML = ">>> ") -> str:
        if self._session is None:
            raise RuntimeError("Call initial_setup() before using prompt()")
        return self._session.prompt(
            HTML(f"<b><gray>{prompt_text}</gray></b>") if isinstance(prompt_text, str) else prompt_text
        )


if __name__ == "__main__":
    test_commands: set[str] = {"start", "qwertyu", "stop", "exit"}
    hist_file: str = "history.txt"

    ac: AutoCompleter = AutoCompleter(autocomplete_button='tab')
    ac.initial_setup(test_commands)

    while True:
        inp: str = ac.prompt(">>> ").strip()
        if inp == "exit":
            break
