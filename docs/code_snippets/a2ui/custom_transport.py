import json
import sys
from collections.abc import Iterator

from argenta.a2ui.models import Message


class StdoutTransport:
    """Minimal transport: prints outgoing frames, reads JSONL actions from stdin."""

    def send(self, message: Message) -> None:
        print(json.dumps(message))

    def actions(self) -> Iterator[Message]:
        for line in sys.stdin:
            decoded = json.loads(line)
            if isinstance(decoded, dict):
                yield decoded

    def close(self) -> None:
        pass
