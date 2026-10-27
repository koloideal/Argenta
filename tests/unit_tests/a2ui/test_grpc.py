import json
import queue
import re
import time
from collections.abc import Iterator

import grpc
import pytest

from argenta.a2ui.transport.grpc import GrpcTransport, agent_pb2, agent_pb2_grpc


@pytest.fixture
def transport() -> Iterator[GrpcTransport]:
    grpc_transport = GrpcTransport(port=0)
    yield grpc_transport
    grpc_transport.close()


def _client(transport: GrpcTransport):
    channel = grpc.insecure_channel(f"127.0.0.1:{transport.port}")
    stub = agent_pb2_grpc.AgentChannelStub(channel)
    requests: queue.Queue[agent_pb2.Frame | None] = queue.Queue()
    responses = stub.Channel(iter(requests.get, None))
    return channel, requests, responses


def _wait_for_clients(transport: GrpcTransport, count: int) -> None:
    for _ in range(100):
        if len(transport._channels) == count:
            return
        time.sleep(0.01)
    raise AssertionError(f"expected {count} connected channel(s)")


def test_send_broadcasts_to_connected_client(transport: GrpcTransport) -> None:
    channel, _requests, responses = _client(transport)
    try:
        _wait_for_clients(transport, 1)
        transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})
        frame = next(responses)
        assert json.loads(frame.json)["createSurface"]["surfaceId"] == "main"
    finally:
        channel.close()


def test_actions_yields_client_messages(transport: GrpcTransport) -> None:
    channel, requests, _responses = _client(transport)
    try:
        requests.put(agent_pb2.Frame(json='{"action": {"name": "deploy", "context": {}}}'))
        message = next(transport.actions())
    finally:
        channel.close()
    action = message["action"]
    assert isinstance(action, dict)
    assert action["name"] == "deploy"


def test_actions_skips_non_object_frames(transport: GrpcTransport) -> None:
    channel, requests, _responses = _client(transport)
    try:
        requests.put(agent_pb2.Frame(json="not json at all"))
        requests.put(agent_pb2.Frame(json='"just a string"'))
        requests.put(agent_pb2.Frame(json='{"action": {"name": "q"}}'))
        message = next(transport.actions())
    finally:
        channel.close()
    action = message["action"]
    assert isinstance(action, dict)
    assert action["name"] == "q"


def test_late_joiner_replays_history(transport: GrpcTransport) -> None:
    transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})
    transport.send({"version": "v0.9", "updateDataModel": {"surfaceId": "main", "path": "/log"}})

    channel, _requests, responses = _client(transport)
    try:
        first = json.loads(next(responses).json)
        second = json.loads(next(responses).json)
    finally:
        channel.close()

    assert "createSurface" in first
    assert "updateDataModel" in second


def test_client_disconnect_unregisters_channel(transport: GrpcTransport) -> None:
    channel, _requests, _responses = _client(transport)
    _wait_for_clients(transport, 1)

    channel.close()
    _wait_for_clients(transport, 0)
    transport.send({"a": 1})


def test_clean_request_stream_end(transport: GrpcTransport) -> None:
    channel, requests, responses = _client(transport)
    try:
        _wait_for_clients(transport, 1)
        requests.put(None)
        for _frame in responses:
            pass
        _wait_for_clients(transport, 0)
    finally:
        channel.close()


def test_register_channel_replays_history(transport: GrpcTransport) -> None:
    transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})

    outgoing = transport.register_channel()
    transport.unregister_channel(outgoing)

    frame = outgoing.get()
    assert frame is not None
    assert json.loads(frame.json)["createSurface"]["surfaceId"] == "main"


def test_verbose_reports_lifecycle_to_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    grpc_transport = GrpcTransport(port=0, verbose=True)
    try:
        channel, _requests, _responses = _client(grpc_transport)
        try:
            _wait_for_clients(grpc_transport, 1)
            grpc_transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})
        finally:
            channel.close()
    finally:
        grpc_transport.close()

    err = capsys.readouterr().err
    assert "[grpc]" in err
    assert "listening on grpc://" in err
    assert "client connected" in err
    assert "sent 'createSurface' to 1 client(s)" in err
    assert re.search(r"\[\d{2}:\d{2}:\d{2}\]", err) is not None


def test_listening_reported_without_verbose(capsys: pytest.CaptureFixture[str]) -> None:
    grpc_transport = GrpcTransport(port=0)
    grpc_transport.close()

    err = capsys.readouterr().err
    assert "listening on grpc://" in err
    assert "client connected" not in err
