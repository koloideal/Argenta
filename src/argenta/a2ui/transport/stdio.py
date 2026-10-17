import json
import sys
from collections.abc import Iterator
from contextlib import suppress
from typing import TextIO

from argenta.a2ui.models import Message


class StdioTransport:
    """
    Public. JSON Lines transport over stdin/stdout:
    one JSON message per line in both directions
    """

    def __init__(self, out: TextIO = sys.stdout, inp: TextIO = sys.stdin) -> None:
        self._out = out
        self._inp = inp

    def send(self, message: Message) -> None:
        self._out.write(f"{json.dumps(message, ensure_ascii=False)}\n")
        self._out.flush()

    def actions(self) -> Iterator[Message]:
        for line in self._inp:
            stripped = line.strip()
            if not stripped:
                continue
            with suppress(json.JSONDecodeError):
                yield json.loads(stripped)

    def close(self) -> None:
        self._out.flush()
