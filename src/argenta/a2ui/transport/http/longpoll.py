import json
import queue
import threading
import time
from collections.abc import Iterator
from http import HTTPStatus
from urllib.parse import parse_qs, urlparse

from argenta.a2ui._verbose import VerboseLog
from argenta.a2ui.models import Message
from argenta.a2ui.transport.http.base import A2UIHttpHandler, A2UIHttpServer


def _parse_cursor(query: str) -> int | None:
    """Private. Extracts the `after` cursor from a query string;
    None when present but malformed"""
    raw = parse_qs(query).get("after", ["0"])[0]
    try:
        return int(raw)
    except ValueError:
        return None


class _PollServer(A2UIHttpServer):
    transport: "LongPollTransport"


class _PollHandler(A2UIHttpHandler):
    """Private. Serves batched A2UI messages on GET /events?after=<cursor>:
    holds the request open until new messages arrive or the poll timeout
    expires, so clients re-request immediately after each response"""

    server: _PollServer

    def serve_events(self) -> None:
        cursor = _parse_cursor(urlparse(self.path).query)
        if cursor is None:
            self._respond(HTTPStatus.BAD_REQUEST)
            return
        batch, next_cursor = self.server.transport.poll(cursor)
        body = json.dumps({"messages": batch, "next": next_cursor}, ensure_ascii=False).encode()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class LongPollTransport:
    """
    Public. Serves A2UI messages to renderer clients as long-polling JSON
    batches (GET /events?after=<cursor>) and accepts action messages via
    POST /actions. Fallback for environments where even SSE streaming is
    blocked — proxies that buffer or cut long-lived chunked responses;
    every poll is a short request/response cycle
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8765,
        *,
        poll_timeout: float = 25.0,
        verbose: bool = False,
    ) -> None:
        self.verbose = VerboseLog(verbose, "poll")  # Private. Handler access
        self.incoming: queue.Queue[Message | None] = queue.Queue()  # Private. Actions
        self.poll_timeout = poll_timeout
        self._history: list[Message] = []
        self._condition = threading.Condition()
        self._closed = False
        self._server = _PollServer((host, port), _PollHandler, self)
        self.port = int(self._server.socket.getsockname()[1])  # Private. Bound port
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self.verbose.report(
            f"listening on http://{host}:{self.port}/events (long poll)", always=True
        )

    def send(self, message: Message) -> None:
        """Appends the message to the history and wakes pending polls"""
        kind = next(key for key in message if key != "version")
        with self._condition:
            self._history.append(message)
            self._condition.notify_all()
        self.verbose.report(f"sent '{kind}'")

    def poll(self, after: int) -> tuple[list[Message], int]:
        """Private. Returns the history slice past `after`, waiting up to
        poll_timeout for new messages"""
        deadline = time.monotonic() + self.poll_timeout
        with self._condition:
            while not self._closed:
                batch = self._history[after:]
                if batch:
                    return batch, len(self._history)
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                self._condition.wait(remaining)
            return [], len(self._history)

    def actions(self) -> Iterator[Message]:
        """Yields action messages posted by clients; ends after close()
        unblocks the queue with a None sentinel"""
        yield from iter(self.incoming.get, None)

    def close(self) -> None:
        """Unblocks actions() consumers, wakes pending polls and shuts
        the HTTP server down"""
        self.incoming.put(None)
        with self._condition:
            self._closed = True
            self._condition.notify_all()
        self._server.shutdown()
        self._server.server_close()
