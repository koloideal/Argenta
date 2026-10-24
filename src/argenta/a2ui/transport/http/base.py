import queue
import socket
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Protocol
from urllib.parse import urlparse

from argenta.a2ui._verbose import VerboseLog
from argenta.a2ui.messages import decode_message
from argenta.a2ui.models import Message


class HttpTransportOps(Protocol):
    """Transport surface the HTTP plumbing needs"""

    verbose: VerboseLog
    incoming: queue.Queue[Message | None]


class A2UIHttpServer(ThreadingHTTPServer):
    daemon_threads = True
    transport: HttpTransportOps

    def __init__(
        self,
        address: tuple[str, int],
        handler_class: type[BaseHTTPRequestHandler],
        transport: HttpTransportOps,
    ) -> None:
        super().__init__(address, handler_class)
        self.transport = transport

    def handle_error(
        self, request: socket.socket | tuple[bytes, socket.socket], client_address: object
    ) -> None:
        """Client resets and other socket errors are routine for a local
        agent — report them through the transport channel; genuine handler
        bugs keep their traceback"""
        if isinstance(sys.exc_info()[1], OSError):
            name = type(sys.exc_info()[1]).__name__
            self.transport.verbose.report(f"http: connection dropped ({name})")
            return
        super().handle_error(request, client_address)


class A2UIHttpHandler(BaseHTTPRequestHandler):
    """Shared HTTP plumbing for the browser-facing transports:
    endpoint index on /, action ingress on POST /actions, CORS preflight,
    access logs routed to the transport verbose channel. Subclasses
    implement serve_events() — SSE stream or a long-poll batch"""

    server: A2UIHttpServer
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/":
            index = (
                b"Argenta A2UI agent\n"
                b"GET /events   -- A2UI message stream\n"
                b"POST /actions -- client action messages\n"
            )
            self._respond(HTTPStatus.OK, body=index)
            return
        if path != "/events":
            self._respond(HTTPStatus.NOT_FOUND)
            return
        self.serve_events()

    def serve_events(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/actions":
            self._respond(HTTPStatus.NOT_FOUND)
            return
        length = int(self.headers.get("Content-Length") or 0)
        message = decode_message(self.rfile.read(length))
        if message is None:
            self._respond(HTTPStatus.BAD_REQUEST)
            return
        self.server.transport.incoming.put(message)
        self._respond(HTTPStatus.ACCEPTED)

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

    def _respond(self, status: HTTPStatus, body: bytes = b"") -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
