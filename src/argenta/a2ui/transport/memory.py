from collections.abc import Iterator

from argenta.a2ui.models import Message


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

    def close(self) -> None:
        """Public. Releases no resources; exists to satisfy the Transport contract"""
