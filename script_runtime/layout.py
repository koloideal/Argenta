"""A Layout that renders application blocks as a markdown transcript."""

from collections.abc import Callable
from contextlib import redirect_stdout
from io import StringIO
from typing import Final, TextIO

from argenta.app.presentation.layout import BlockKind

_CODE_FENCE: Final = "```"
_QUOTED_KINDS: Final = (BlockKind.SYSTEM, BlockKind.ERROR)
_FENCED_KINDS: Final = (BlockKind.OUTPUT, BlockKind.COMMAND_GROUPS, BlockKind.BANNER)


def _capture(produce: Callable[[], None]) -> str:
    buffer = StringIO()
    with redirect_stdout(buffer):
        produce()
    return buffer.getvalue().rstrip()


class MarkdownLayout:
    """
    Public. Renders each block as markdown: output and command lists go
    into fenced code blocks, system messages become blockquotes, the
    farewell becomes a horizontal rule
    """

    def __init__(self, sink: TextIO) -> None:
        """
        :param sink: text stream for markdown output (file, stdout, ...)
        """
        self._write = sink.write

    def present(
        self, kind: BlockKind, produce: Callable[[], None], *, capturable: bool = True
    ) -> None:
        """
        Public. Captures the block output and writes it as markdown
        :param kind: semantic kind of the block
        :param produce: prints the block content
        :param capturable: unused here — scripts never read interactive input
        :return: None
        """
        text = _capture(produce)
        if not text:
            return
        if kind in _QUOTED_KINDS:
            for line in text.splitlines():
                self._write(f"> {line}\n")
        elif kind in _FENCED_KINDS:
            self._write(f"{_CODE_FENCE}\n{text}\n{_CODE_FENCE}\n")
        elif kind is BlockKind.FAREWELL:
            self._write(f"\n---\n*{text}*\n")
        else:
            self._write(f"{text}\n")

    def command_heading(self, raw_command: str) -> None:
        """
        Public. Writes the command being replayed as an inline-code heading
        :param raw_command: the script line about to be dispatched
        :return: None
        """
        self._write(f"\n`$ {raw_command}`\n\n")
