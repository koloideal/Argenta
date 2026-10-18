"""A runtime that replays commands from a script file without user input."""

from pathlib import Path
from typing import Final

from argenta import App
from argenta.command import InputCommand
from argenta.command.exceptions import InputCommandException
from script_runtime.layout import MarkdownLayout

_COMMENT_PREFIX: Final = "#"


class ScriptRuntime:
    """
    Public. Reads a script of commands (one per line, `#` comments and
    blank lines allowed), dispatches each through the regular app path
    and stops at the exit command
    """

    def __init__(self, app: App, layout: MarkdownLayout) -> None:
        """
        :param app: a configured application
        :param layout: the markdown layout receiving every block
        """
        self._app = app
        self._layout = layout

    def run(self, script_path: Path) -> None:
        """
        Public. Prepares the app, then replays the script line by line
        :param script_path: file with one command per line
        :return: None
        """
        self._app.prepare_for_run(self._layout)
        for raw_line in script_path.read_text().splitlines():
            if self._dispatch(raw_line.strip()):
                break

    def _dispatch(self, raw_command: str) -> bool:
        """Private. Returns True when the exit command was dispatched"""
        if not raw_command or raw_command.startswith(_COMMENT_PREFIX):
            return False
        self._layout.command_heading(raw_command)
        try:
            command = InputCommand.parse(raw_command)
        except InputCommandException as error:
            self._app.handle_input_error(error, raw_command, self._layout)
            return False
        return self._app.dispatch_input_command(command, self._layout)
