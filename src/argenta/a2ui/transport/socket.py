import json
import os
import queue
import socket
import socketserver
import threading
from collections.abc import Iterator
from contextlib import suppress
from io import BufferedIOBase

from argenta.a2ui._verbose import VerboseLog
from argenta.a2ui.messages import decode_message
from argenta.a2ui.models import Message


class _Client:
    """Private. One connected client: its socket plus the buffered writer"""

    def __init__(self, connection: socket.socket, writer: BufferedIOBase) -> None:
        self.connection = connection
        self.writer = writer


def _write_frame(writer: BufferedIOBase, payload: bytes) -> bool:
    """Private. Writes one JSONL frame; False when the client went away"""
    with suppress(OSError, ValueError):
        writer.write(payload)
        writer.flush()
        return True
    return False


class _TCPServer(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True
    transport: "SocketTransport"


class _UnixServer(socketserver.ThreadingUnixStreamServer):
    daemon_threads = True
    transport: "SocketTransport"


class _SocketHandler(socketserver.StreamRequestHandler):
    """Private. Replays history to a fresh client, then reads action lines"""

    server: _TCPServer | _UnixServer
    _client: _Client

    def setup(self) -> None:
        super().setup()
        self._client = self.server.transport.register_client(self.connection, self.wfile)

    def handle(self) -> None:  # noqa: WPS110 — socketserver handler API
        # a client resetting the connection mid-read is routine, not an error
        with suppress(OSError):
            for raw in self.rfile:
                decoded = decode_message(raw)
                if decoded is not None:
                    self.server.transport.incoming.put(decoded)

    def finish(self) -> None:
        self.server.transport.unregister_client(self._client)
        with suppress(OSError):
            super().finish()


class SocketTransport:
    """
    Public. JSON Lines transport over raw TCP or Unix domain sockets:
    one JSON message per line in both directions. Replays message history
    to late joiners. The native-clients counterpart of the stdio
    transport — for renderers without a browser, across processes
    or containers
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8765,
        *,
        path: str | None = None,
        verbose: bool = False,
    ) -> None:
        self.verbose = VerboseLog(verbose, "sock")  # Private. Handler access
        self.incoming: queue.Queue[Message | None] = queue.Queue()  # Private. Actions
        self._clients: set[_Client] = set()
        self._history: list[str] = []
        self._lock = threading.Lock()
        self._path = path
        self.port = 0  # Private. Actual bound port for TCP servers
        if path is None:
            tcp_server = _TCPServer((host, port), _SocketHandler)
            self._server: _TCPServer | _UnixServer = tcp_server
            self.port = int(tcp_server.server_address[1])
            endpoint = f"tcp://{host}:{self.port}"
        else:
            with suppress(FileNotFoundError):
                os.unlink(path)
            unix_server = _UnixServer(path, _SocketHandler)
            self._server = unix_server
            endpoint = f"unix://{path}"
        self._server.transport = self
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self.verbose.report(f"listening on {endpoint}", always=True)

    def send(self, message: Message) -> None:
        """Broadcasts an A2UI message as a JSONL frame to every client"""
        payload = json.dumps(message, ensure_ascii=False)
        kind = next(key for key in message if key != "version")
        with self._lock:
            self._history.append(payload)
            clients = tuple(self._clients)
        frame = f"{payload}\n".encode()
        for client in clients:
            if not _write_frame(client.writer, frame):
                self.unregister_client(client)
        self.verbose.report(f"sent '{kind}' to {len(clients)} client(s)")

    def actions(self) -> Iterator[Message]:
        """Yields decoded action lines sent by clients; ends after close()
        unblocks the queue with a None sentinel"""
        yield from iter(self.incoming.get, None)

    def close(self) -> None:
        """Unblocks actions() consumers, drops clients and shuts
        the listening server down"""
        self.incoming.put(None)
        with self._lock:
            clients = tuple(self._clients)
        for client in clients:
            with suppress(OSError):
                client.connection.shutdown(socket.SHUT_RDWR)
                client.connection.close()
        self._server.shutdown()
        self._server.server_close()
        if self._path is not None:
            with suppress(FileNotFoundError):
                os.unlink(self._path)

    def register_client(self, connection: socket.socket, writer: BufferedIOBase) -> _Client:
        """Private. Replays the message history so late joiners rebuild
        the current surface, then registers the client for live frames"""
        client = _Client(connection, writer)
        with self._lock:
            for payload in self._history:
                if not _write_frame(writer, f"{payload}\n".encode()):
                    return client
            self._clients.add(client)
        self.verbose.report("client connected")
        return client

    def unregister_client(self, client: _Client) -> None:
        """Private. Removes a client from the broadcast set"""
        with self._lock:
            self._clients.discard(client)
        self.verbose.report("client disconnected")
