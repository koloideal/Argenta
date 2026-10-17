import json
import queue
import threading
from collections.abc import Iterator
from contextlib import suppress
from http import HTTPStatus
from io import BufferedIOBase

from argenta.a2ui._verbose import VerboseLog
from argenta.a2ui.models import Message
from argenta.a2ui.transport.http.base import A2UIHttpHandler, A2UIHttpServer


def _write_frame(writer: BufferedIOBase, payload: str) -> bool:
    """Private. Writes one SSE frame; False when the client went away"""
    with suppress(BrokenPipeError, ConnectionResetError):
        writer.write(f"data: {payload}\n\n".encode())
        writer.flush()
        return True
    return False


class _SSEServer(A2UIHttpServer):
    transport: "SSETransport"


class _SSEHandler(A2UIHttpHandler):
    """Private. Serves the SSE stream on GET /events"""

    server: _SSEServer

    def serve_events(self) -> None:
        transport = self.server.transport
        client = transport.register_client()
        self._send_stream_headers()
        while True:
            payload = client.get()
            if payload is None or not _write_frame(self.wfile, payload):
                break
        transport.unregister_client(client)

    def _send_stream_headers(self) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        # the stream is close-delimited: closing the socket ends it
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True


class SSETransport:
    """
    Public. Serves A2UI messages to renderer clients over SSE
    (GET /events) and accepts action messages via POST /actions.
    Pure-stdlib alternative to the WebSocket transport that survives
    proxies which block WebSocket upgrades
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8765, *, verbose: bool = False) -> None:
        self.verbose = VerboseLog(verbose, "sse")  # Private. Used by the handler
        self.incoming: queue.Queue[Message | None] = queue.Queue()  # Private. Actions
        self._clients: list[queue.Queue[str | None]] = []
        self._history: list[str] = []
        self._lock = threading.Lock()
        self._server = _SSEServer((host, port), _SSEHandler, self)
        self.port = int(self._server.socket.getsockname()[1])  # Private. Actual bound port
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self.verbose.report(f"listening on http://{host}:{self.port}/events", always=True)

    def send(self, message: Message) -> None:
        """Broadcasts an A2UI message to all connected clients"""
        payload = json.dumps(message, ensure_ascii=False)
        kind = next(key for key in message if key != "version")
        with self._lock:
            self._history.append(payload)
            clients = tuple(self._clients)
        for client in clients:
            client.put(payload)
        self.verbose.report(f"sent '{kind}' to {len(clients)} client(s)")

    def actions(self) -> Iterator[Message]:
        """Yields action messages posted by clients; ends after close()
        unblocks the queue with a None sentinel"""
        yield from iter(self.incoming.get, None)

    def close(self) -> None:
        """Unblocks actions() consumers, ends client streams and
        shuts the HTTP server down"""
        self.incoming.put(None)
        with self._lock:
            clients = tuple(self._clients)
        for client in clients:
            client.put(None)
        self._server.shutdown()
        self._server.server_close()

    def register_client(self) -> queue.Queue[str | None]:
        """Private. Registers an SSE client and replays the message
        history so late joiners rebuild the current surface"""
        client: queue.Queue[str | None] = queue.Queue()
        with self._lock:
            for payload in self._history:
                client.put(payload)
            self._clients.append(client)
        self.verbose.report("client connected")
        return client

    def unregister_client(self, client: queue.Queue[str | None]) -> None:
        """Private. Removes a client from the broadcast list"""
        with self._lock:
            self._clients.remove(client)
        self.verbose.report("client disconnected")
