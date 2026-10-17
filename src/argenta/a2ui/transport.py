import json
import sys
from collections.abc import Iterator
from contextlib import suppress
from typing import Protocol, TextIO

from argenta.a2ui.models import Message


class Transport(Protocol):
    """
    Public. Transport contract for the A2UI stream:
    send() emits agent-to-renderer messages, actions() yields decoded
    client-to-agent messages
    """

    def send(self, message: Message) -> None:
        raise NotImplementedError  # pragma: no cover

    def actions(self) -> Iterator[Message]:
        raise NotImplementedError  # pragma: no cover


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


class MemoryTransport:
    """
    Public. In-memory transport for tests and embedding:
    keeps outgoing messages in .sent, replays incoming messages
    """

    def __init__(self, incoming: list[Message] | None = None) -> None:
        self.sent: list[Message] = []
        self._incoming = incoming or []

    def send(self, message: Message) -> None:
        self.sent.append(message)

    def actions(self) -> Iterator[Message]:
        yield from self._incoming
