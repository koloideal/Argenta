import http.client
import json
import re
import time
from collections.abc import Iterator

import pytest
from pytest_mock import MockerFixture
from websockets.exceptions import ConnectionClosed
from websockets.sync.client import connect
from websockets.sync.server import ServerConnection

from argenta.a2ui.transport.websocket import WebSocketTransport


@pytest.fixture
def transport() -> Iterator[WebSocketTransport]:
    ws_transport = WebSocketTransport(port=0)
    yield ws_transport
    ws_transport.close()


def _client(transport: WebSocketTransport):
    return connect(f"ws://127.0.0.1:{transport.port}")


def test_send_broadcasts_to_connected_client(transport: WebSocketTransport) -> None:
    with _client(transport) as client:
        transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})
        assert json.loads(client.recv())["createSurface"]["surfaceId"] == "main"


def test_send_to_closed_connection_does_not_raise(transport: WebSocketTransport) -> None:
    with _client(transport):
        transport.send({"a": 1})
    transport.send({"b": 2})


def test_actions_yields_client_messages(transport: WebSocketTransport) -> None:
    with _client(transport) as client:
        client.send('{"action": {"name": "deploy", "context": {}}}')
        message = next(transport.actions())
    action = message["action"]
    assert isinstance(action, dict)
    assert action["name"] == "deploy"


def test_actions_skips_non_object_frames(transport: WebSocketTransport) -> None:
    with _client(transport) as client:
        client.send("not json at all")
        client.send('"just a string"')
        client.send('{"action": {"name": "q"}}')
        message = next(transport.actions())
    action = message["action"]
    assert isinstance(action, dict)
    assert action["name"] == "q"


def test_replay_aborts_on_closed_connection(
    transport: WebSocketTransport, mocker: MockerFixture
) -> None:
    transport.send({"a": 1})
    fake = mocker.MagicMock(spec=ServerConnection)
    fake.send.side_effect = ConnectionClosed(None, None)

    transport._handle_client(fake)

    assert fake not in transport._connections


def test_send_drops_failed_connection(transport: WebSocketTransport, mocker: MockerFixture) -> None:
    fake = mocker.MagicMock(spec=ServerConnection)
    fake.send.side_effect = ConnectionClosed(None, None)
    transport._connections.add(fake)

    transport.send({"a": 1})

    assert fake not in transport._connections


def test_verbose_reports_lifecycle_to_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    ws_transport = WebSocketTransport(port=0, verbose=True)
    try:
        with _client(ws_transport):
            for _ in range(100):
                if ws_transport._connections:
                    break
                time.sleep(0.01)
            ws_transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})
    finally:
        ws_transport.close()

    err = capsys.readouterr().err
    assert "[ws]" in err
    assert "listening on ws://" in err
    assert "client connected" in err
    assert "sent 'createSurface' to 1 client(s)" in err
    assert re.search(r"\[\d{2}:\d{2}:\d{2}\]", err) is not None


def test_listening_reported_without_verbose(capsys: pytest.CaptureFixture[str]) -> None:
    ws_transport = WebSocketTransport(port=0)
    ws_transport.close()

    err = capsys.readouterr().err
    assert "listening on ws://" in err
    assert "client connected" not in err


def test_late_joiner_replays_history(transport: WebSocketTransport) -> None:
    transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})
    transport.send({"version": "v0.9", "updateDataModel": {"surfaceId": "main", "path": "/log"}})

    with _client(transport) as client:
        first = json.loads(client.recv())
        second = json.loads(client.recv())

    assert "createSurface" in first
    assert "updateDataModel" in second


def test_plain_http_probe_gets_426_and_ws_still_works(transport: WebSocketTransport) -> None:
    connection = http.client.HTTPConnection("127.0.0.1", transport.port)
    connection.request("GET", "/events")
    response = connection.getresponse()
    connection.close()

    assert response.status == 426
    with _client(transport):  # the websocket handshake still succeeds after the probe
        pass
