import json
import queue
import threading
from collections.abc import Iterator
from contextlib import suppress
from typing import Final, cast

from websockets.exceptions import ConnectionClosed
from websockets.http11 import Request, Response
from websockets.sync.server import Server, ServerConnection, serve

from argenta.a2ui._verbose import VerboseLog
from argenta.a2ui.messages import decode_message
from argenta.a2ui.models import Message

_UPGRADE_REQUIRED_STATUS = 426


class _HttpProbeGuard:
    """Private. Intercepts the opening handshake: plain HTTP requests
    (stale SSE/poll probes, healthchecks) get 426 Upgrade Required
    instead of a crashing handshake; real websocket upgrades pass"""

    def __init__(self, verbose: VerboseLog) -> None:
        self._verbose = verbose

    def __call__(self, connection: ServerConnection, request: Request) -> Response | None:
        if request.headers.get("Upgrade", "").lower() == "websocket":
            return None
        self._verbose.report("rejected a plain HTTP request")
        return connection.respond(_UPGRADE_REQUIRED_STATUS, "Upgrade Required\n")


class WebSocketTransport:
    """
    Public. Broadcasts A2UI messages to every connected renderer client
    and yields decoded action messages received over WebSocket.

    Requires the optional ``websockets`` dependency (``uv add 'argenta[a2ui]'``).
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8765, *, verbose: bool = False) -> None:
        self._stop: Final = cast("Message", object())
        self._verbose = VerboseLog(verbose, "ws")
        self._incoming: queue.Queue[Message] = queue.Queue()
        self._connections: set[ServerConnection] = set()
        self._history: list[str] = []
        self._lock = threading.Lock()
        self._server: Server = serve(
            self._handle_client,
            host,
            port,
            process_request=_HttpProbeGuard(self._verbose),
        )
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self._verbose.report(f"listening on ws://{host}:{self.port}", always=True)

    @property
    def port(self) -> int:
        """The actual port the server is bound to"""
        return int(self._server.socket.getsockname()[1])

    def send(self, message: Message) -> None:
        """Broadcasts an A2UI message to all connected clients"""
        payload = json.dumps(message, ensure_ascii=False)
        kind = next(key for key in message if key != "version")
        with self._lock:
            self._history.append(payload)
            connections = tuple(self._connections)
        for connection in connections:
            try:
                connection.send(payload)
            except ConnectionClosed:
                self._drop(connection)
        self._verbose.report(f"sent '{kind}' to {len(connections)} client(s)")

    def actions(self) -> Iterator[Message]:
        """Yields decoded action messages received from connected clients;
        ends after close() unblocks the queue with the stop sentinel"""
        yield from iter(self._incoming.get, self._stop)

    def close(self) -> None:
        """Unblocks actions() consumers and shuts the WebSocket server down"""
        self._incoming.put(self._stop)
        self._server.shutdown()

    def _handle_client(self, connection: ServerConnection) -> None:
        """Private. Serves one client connection: replays missed messages
        so late joiners rebuild the current surface, then forwards actions"""
        with self._lock:
            for payload in self._history:
                try:
                    connection.send(payload)
                except ConnectionClosed:
                    return
            self._connections.add(connection)
        self._verbose.report("client connected")
        with suppress(ConnectionClosed):
            for raw in connection:
                decoded = decode_message(raw)
                if decoded is not None:
                    self._incoming.put(decoded)
        self._drop(connection)

    def _drop(self, connection: ServerConnection) -> None:
        """Private. Removes a connection from the broadcast set"""
        with self._lock:
            self._connections.discard(connection)
        self._verbose.report("client disconnected")
