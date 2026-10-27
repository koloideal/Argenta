from collections.abc import Iterator
from typing import Protocol

from argenta.a2ui.models import Message


class Transport(Protocol):
    """
    Public. Transport contract for the A2UI stream:
    send() emits agent-to-renderer messages, actions() yields decoded
    client-to-agent messages, close() releases the transport
    """

    def send(self, message: Message) -> None:
        raise NotImplementedError  # pragma: no cover

    def actions(self) -> Iterator[Message]:
        raise NotImplementedError  # pragma: no cover

    def close(self) -> None:
        raise NotImplementedError  # pragma: no cover
