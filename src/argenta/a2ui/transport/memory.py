import queue
from collections.abc import Iterable, Iterator

from argenta.a2ui.models import Message


class MemoryTransport:
    """
    Public. In-memory transport for tests and embedding.

    In script mode (default) actions() replays the `incoming` preload and
    ends; in live mode (live=True) actions() stays open and the host
    injects client actions via push() until close(). Outgoing messages are
    recorded in .sent for assertions and streamed live through messages()
    """

    def __init__(self, incoming: Iterable[Message] | None = None, *, live: bool = False) -> None:
        self.sent: list[Message] = []
        self._events: queue.Queue[Message | None] = queue.Queue()
        self._incoming: queue.Queue[Message | None] = queue.Queue()
        for message in incoming or ():
            self._incoming.put(message)
        if not live:
            self._incoming.put(None)

    def send(self, message: Message) -> None:
        self.sent.append(message)
        self._events.put(message)

    def messages(self) -> Iterator[Message]:
        """
        Public. Streams outgoing messages as they are sent; ends when
        close() pushes the None sentinel — the host-side subscribe API
        """
        yield from iter(self._events.get, None)

    def push(self, message: Message) -> None:
        """
        Public. Injects a client-to-agent message; consumed by actions()
        in live mode (in script mode pushed items land after the sentinel
        and are dropped)
        """
        self._incoming.put(message)

    def actions(self) -> Iterator[Message]:
        yield from iter(self._incoming.get, None)

    def close(self) -> None:
        """Public. Ends the live streams: actions() in live mode and
        messages() subscribers; idempotent"""
        self._incoming.put(None)
        self._events.put(None)
