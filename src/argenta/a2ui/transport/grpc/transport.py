import json
import queue
import threading
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress

import grpc

from argenta.a2ui._verbose import VerboseLog
from argenta.a2ui.messages import decode_message
from argenta.a2ui.models import Message
from argenta.a2ui.transport.grpc import agent_pb2

_Frames = queue.Queue[agent_pb2.Frame | None]


def _drain_requests(
    transport: "GrpcTransport",
    request_iterator: Iterator[agent_pb2.Frame],
    outgoing: _Frames,
) -> None:
    """Private. Forwards client frames into the transport's action queue,
    then ends the response stream — the client went away"""
    with suppress(grpc.RpcError):
        for frame in request_iterator:
            decoded = decode_message(frame.json)
            if decoded is not None:
                transport.incoming.put(decoded)
    outgoing.put(None)


class GrpcTransport:
    """
    Public. A2UI transport over a gRPC bidirectional stream
    (``argenta.a2ui.AgentChannel/Channel``): one JSON message per
    ``Frame`` in both directions. Replays message history to late
    joiners. For native clients that already speak gRPC — browsers
    cannot call gRPC directly.

    Requires the optional ``grpcio`` and ``protobuf`` dependencies
    (``uv add 'argenta[a2ui]'``).
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8765,
        *,
        verbose: bool = False,
        stop_timeout: float = 10,
    ) -> None:
        self.verbose = VerboseLog(verbose, "grpc")  # Private. Handler access
        self.incoming: queue.Queue[Message | None] = queue.Queue()  # Private. Actions
        self._stop_timeout = stop_timeout
        self._history: list[str] = []
        self._channels: set[_Frames] = set()
        self._lock = threading.Lock()
        self._server = grpc.server(ThreadPoolExecutor())
        handlers = {
            "Channel": grpc.stream_stream_rpc_method_handler(
                self._channel,
                request_deserializer=agent_pb2.Frame.FromString,
                response_serializer=agent_pb2.Frame.SerializeToString,
            ),
        }
        self._server.add_generic_rpc_handlers(
            (grpc.method_handlers_generic_handler("argenta.a2ui.AgentChannel", handlers),)
        )
        self.port = self._server.add_insecure_port(f"{host}:{port}")  # Private. Bound port
        self._server.start()
        self.verbose.report(f"listening on grpc://{host}:{self.port}", always=True)

    def send(self, message: Message) -> None:
        """Broadcasts an A2UI message as a Frame to every connected stream"""
        payload = json.dumps(message, ensure_ascii=False)
        kind = next(key for key in message if key != "version")
        with self._lock:
            self._history.append(payload)
            channels = tuple(self._channels)
        for outgoing in channels:
            outgoing.put(agent_pb2.Frame(json=payload))
        self.verbose.report(f"sent '{kind}' to {len(channels)} client(s)")

    def actions(self) -> Iterator[Message]:
        """Yields decoded action frames sent by clients; ends after close()
        unblocks the queue with a None sentinel"""
        yield from iter(self.incoming.get, None)

    def close(self) -> None:
        """Unblocks actions() consumers, ends client streams and shuts
        the gRPC server down"""
        self.incoming.put(None)
        with self._lock:
            channels = tuple(self._channels)
        for outgoing in channels:
            outgoing.put(None)
        self._server.stop(grace=None).wait(timeout=self._stop_timeout)

    def register_channel(self) -> _Frames:
        """Private. Replays the message history into a fresh stream's queue
        so late joiners rebuild the current surface, then registers the
        queue for live frames"""
        outgoing: _Frames = queue.Queue()
        with self._lock:
            for payload in self._history:
                outgoing.put(agent_pb2.Frame(json=payload))
            self._channels.add(outgoing)
        self.verbose.report("client connected")
        return outgoing

    def unregister_channel(self, outgoing: _Frames) -> None:
        """Private. Removes a stream queue from the broadcast set"""
        with self._lock:
            self._channels.discard(outgoing)
        self.verbose.report("client disconnected")

    def _channel(
        self, request_iterator: Iterator[agent_pb2.Frame], _context: grpc.ServicerContext
    ) -> Iterator[agent_pb2.Frame]:
        """Private. gRPC stream-stream handler: drains client frames on a
        worker thread while this generator streams server frames back"""
        outgoing = self.register_channel()
        drain = threading.Thread(
            target=_drain_requests,
            args=(self, request_iterator, outgoing),
            daemon=True,
        )
        drain.start()
        with suppress(grpc.RpcError):
            yield from iter(outgoing.get, None)
        self.unregister_channel(outgoing)
