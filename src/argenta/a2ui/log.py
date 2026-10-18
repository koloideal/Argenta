from collections import deque
from collections.abc import Callable
from contextlib import redirect_stdout
from io import StringIO

from argenta.a2ui.models import A2UIConfig, Message
from argenta.app.presentation.layout import BlockKind


class EntryLog:
    """
    Private. Layout of the A2UI agent: every block becomes one structured
    log entry ({id, kind, text, markdown}); separators, gaps and frames are
    left to the renderer, so no terminal decoration reaches the surface
    """

    def __init__(self, config: A2UIConfig) -> None:
        """
        :param config: log fence and entry cap configuration
        """
        self._fence = config.log_fence
        self._entries: deque[Message] = deque(maxlen=config.max_log_entries)
        self._next_id = 0
        self._dirty = False

    def present(
        self, kind: BlockKind, produce: Callable[[], None], *, capturable: bool = True
    ) -> None:
        """
        Private. Captures the block output into a log entry; there is no
        terminal to stream to, so the capturable hint does not apply
        :param kind: semantic kind of the block
        :param produce: prints the block content
        :param capturable: ignored — agent output is always captured
        :return: None
        """
        buffer = StringIO()
        with redirect_stdout(buffer):
            produce()
        self._append(kind, buffer.getvalue())

    def append_error(self, text: str) -> None:
        """
        Private. Records a runtime failure (an uncaught handler exception)
        :param text: the formatted traceback
        :return: None
        """
        self._append(BlockKind.ERROR, text)

    def take_update(self) -> list[Message] | None:
        """
        Private. Returns the entries changed since the previous call
        :return: the full capped entry list, or None when nothing changed
        """
        if not self._dirty:
            return None
        self._dirty = False
        return list(self._entries)

    def _append(self, kind: BlockKind, text: str) -> None:
        """Private. Appends a non-empty entry; the deque drops the oldest past the cap"""
        stripped = text.strip("\n")
        if not stripped:
            return
        self._entries.append(
            {
                "id": self._next_id,
                "kind": kind.value,
                "text": stripped,
                "markdown": f"{self._fence}\n{stripped}\n{self._fence}",
            }
        )
        self._next_id += 1
        self._dirty = True
