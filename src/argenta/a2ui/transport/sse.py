import json
import queue
import threading
from collections.abc import Iterator
from contextlib import suppress
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BufferedIOBase

from argenta.a2ui._verbose import VerboseLog
from argenta.a2ui.messages import decode_message
from argenta.a2ui.models import Message


def _write_frame(writer: BufferedIOBase, payload: str) -> bool:
    """Private. Writes one SSE frame; False when the client went away"""
    with suppress(BrokenPipeError, ConnectionResetError):
        writer.write(f"data: {payload}\n\n".encode())
        writer.flush()
        return True
    return False


class _SSEServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], transport: "SSETransport") -> None:
        super().__init__(address, _SSEHandler)
        self.transport = transport


class _SSEHandler(BaseHTTPRequestHandler):
    """Private. Serves the SSE stream (GET /events) and the action
    ingress endpoint (POST /actions)"""

    server: _SSEServer
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:
        if self.path != "/events":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        transport = self.server.transport
        client = transport.register_client()
        self._send_stream_headers()
        while True:
            payload = client.get()
            if payload is None or not _write_frame(self.wfile, payload):
                break
        transport.unregister_client(client)

    def do_POST(self) -> None:
        if self.path != "/actions":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        length = int(self.headers.get("Content-Length") or 0)
        message = decode_message(self.rfile.read(length))
        if message is None:
            self.send_error(HTTPStatus.BAD_REQUEST)
            return
        self.server.transport.incoming.put(message)
        self.send_response(HTTPStatus.ACCEPTED)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def end_headers(self) -> None:
        # the demo client is served from a different port
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, msg_format: str, *args: object) -> None:
        message = msg_format % args
        self.server.transport.verbose.report(f"http: {message}")

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
        self._server = _SSEServer((host, port), self)
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
