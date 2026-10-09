import sys

from prompt_toolkit import HTML, PromptSession

from argenta.app.autocompleter._ext_features_impl import build_session, do_prompt


class AutoCompleter:
    def __init__(
        self,
        history_filename: str | None = None,
        autocomplete_button: str = "tab",
        command_highlighting: bool = True,
        auto_suggestions: bool = True,
    ) -> None:
        self.history_filename: str | None = history_filename
        self.autocomplete_button: str = autocomplete_button
        self.command_highlighting: bool = command_highlighting
        self.auto_suggestions: bool = auto_suggestions
        self._session: PromptSession[str] | None = None
        self._fallback_mode: bool = False

    def initial_setup(self, all_commands: set[str]) -> None:
        if not sys.stdin.isatty():
            self._session = None
            self._fallback_mode = True
            return

        self._session = build_session(
            self.history_filename,
            self.autocomplete_button,
            self.command_highlighting,
            self.auto_suggestions,
            all_commands,
        )

    def prompt(self, prompt_text: str | HTML = ">>> ") -> str:
        if self._fallback_mode:
            return input(prompt_text if isinstance(prompt_text, str) else ">>> ")
        if self._session is None:
            raise RuntimeError("Call initial_setup() before using prompt()")

        return do_prompt(self._session, prompt_text)
