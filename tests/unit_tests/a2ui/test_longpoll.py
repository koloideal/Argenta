import http.client
import json
import socket
import struct
import time
from collections.abc import Iterator
from typing import TypedDict

import pytest

from argenta.a2ui.models import Message
from argenta.a2ui.transport.http.longpoll import LongPollTransport


class _Batch(TypedDict):
    messages: list[Message]
    next: int


@pytest.fixture
def transport() -> Iterator[LongPollTransport]:
    poll_transport = LongPollTransport(port=0, poll_timeout=0.5)
    yield poll_transport
    poll_transport.close()


def _request(
    transport: LongPollTransport, path: str, method: str = "GET", body: str = ""
) -> http.client.HTTPResponse:
    conn = http.client.HTTPConnection("127.0.0.1", transport.port, timeout=5)
    conn.request(method, path, body=body or None)
    response = conn.getresponse()
    response.read()
    conn.close()
    return response


def _poll(transport: LongPollTransport, path: str) -> _Batch:
    conn = http.client.HTTPConnection("127.0.0.1", transport.port, timeout=5)
    conn.request("GET", path)
    response = conn.getresponse()
    batch: _Batch = json.loads(response.read())
    conn.close()
    return batch


def test_poll_returns_full_history_on_first_request(transport: LongPollTransport) -> None:
    transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})
    transport.send({"version": "v0.9", "ping": {}})

    batch = _poll(transport, "/events")

    assert len(batch["messages"]) == 2
    assert batch["next"] == 2


def test_poll_returns_only_new_messages(transport: LongPollTransport) -> None:
    transport.send({"version": "v0.9", "old": {}})
    first = _poll(transport, "/events")
    transport.send({"version": "v0.9", "new": {}})

    second = _poll(transport, f"/events?after={first['next']}")

    assert [m["new"] for m in second["messages"] if "new" in m]
    assert second["next"] == 2


def test_poll_holds_request_until_message(transport: LongPollTransport) -> None:
    conn = http.client.HTTPConnection("127.0.0.1", transport.port, timeout=5)
    conn.request("GET", "/events")
    transport.send({"version": "v0.9", "woken": {}})

    batch = json.loads(conn.getresponse().read())
    conn.close()

    assert batch["messages"] == [{"version": "v0.9", "woken": {}}]


def test_poll_returns_empty_on_timeout(transport: LongPollTransport) -> None:
    batch = _poll(transport, "/events")

    assert batch["messages"] == []
    assert batch["next"] == 0


def test_poll_malformed_cursor_gets_400(transport: LongPollTransport) -> None:
    response = _request(transport, "/events?after=banana")

    assert response.status == 400


def test_poll_post_action_reaches_actions(transport: LongPollTransport) -> None:
    body = json.dumps({"action": {"name": "deploy", "context": {}}})
    response = _request(transport, "/actions", method="POST", body=body)

    assert response.status == 202
    assert next(transport.actions()) == {"action": {"name": "deploy", "context": {}}}


def test_poll_unknown_paths_get_404(transport: LongPollTransport) -> None:
    response = _request(transport, "/nope")

    assert response.status == 404


def test_poll_close_ends_actions_and_wakes_polls(transport: LongPollTransport) -> None:
    transport.close()

    assert list(transport.actions()) == []
    assert transport.poll(0) == ([], 0)


def test_poll_client_reset_is_quiet(
    transport: LongPollTransport, capsys: pytest.CaptureFixture[str]
) -> None:
    # SO_LINGER with a zero timeout makes close() send RST instead of FIN
    conn = socket.create_connection(("127.0.0.1", transport.port), timeout=5)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    conn.close()
    time.sleep(0.2)

    assert "Traceback" not in capsys.readouterr().err


def test_poll_verbose_reports_lifecycle(capsys: pytest.CaptureFixture[str]) -> None:
    poll_transport = LongPollTransport(port=0, verbose=True)
    poll_transport.send({"version": "v0.9", "ping": {}})
    _poll(poll_transport, "/events")
    poll_transport.close()

    err = capsys.readouterr().err
    assert "[poll]" in err
    assert "listening on http://" in err
    assert "sent 'ping'" in err
