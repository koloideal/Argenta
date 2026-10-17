import http.client
import json
from collections.abc import Iterator

import pytest

from argenta.a2ui.transport.sse import SSETransport


@pytest.fixture
def transport() -> Iterator[SSETransport]:
    sse_transport = SSETransport(port=0)
    yield sse_transport
    sse_transport.close()


def _open_events(
    transport: SSETransport,
) -> tuple[http.client.HTTPConnection, http.client.HTTPResponse]:
    conn = http.client.HTTPConnection("127.0.0.1", transport.port, timeout=5)
    conn.request("GET", "/events")
    return conn, conn.getresponse()


def _sse_frames(response: http.client.HTTPResponse) -> Iterator[str]:
    while line := response.fp.readline():
        if line.startswith(b"data: "):
            yield line[6:].strip().decode()


def _post(transport: SSETransport, path: str, body: str) -> http.client.HTTPResponse:
    conn = http.client.HTTPConnection("127.0.0.1", transport.port, timeout=5)
    conn.request("POST", path, body=body, headers={"Content-Length": str(len(body))})
    response = conn.getresponse()
    response.read()
    conn.close()
    return response


def test_sse_replays_history_to_late_client(transport: SSETransport) -> None:
    transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})

    conn, response = _open_events(transport)

    assert "createSurface" in next(_sse_frames(response))
    conn.close()


def test_sse_streams_live_messages(transport: SSETransport) -> None:
    conn, response = _open_events(transport)
    transport.send({"version": "v0.9", "updateDataModel": {"path": "/log", "value": "hi"}})

    assert "updateDataModel" in next(_sse_frames(response))
    conn.close()


def test_sse_post_action_reaches_actions(transport: SSETransport) -> None:
    body = json.dumps({"action": {"name": "deploy", "context": {}}})
    response = _post(transport, "/actions", body)

    assert response.status == 202
    assert next(transport.actions()) == {"action": {"name": "deploy", "context": {}}}


def test_sse_malformed_post_gets_400(transport: SSETransport) -> None:
    response = _post(transport, "/actions", "not json")

    assert response.status == 400


def test_sse_root_serves_endpoint_index(transport: SSETransport) -> None:
    conn = http.client.HTTPConnection("127.0.0.1", transport.port, timeout=5)
    conn.request("GET", "/")
    response = conn.getresponse()
    body = response.read()
    conn.close()

    assert response.status == 200
    assert b"GET /events" in body
    assert b"POST /actions" in body


def test_sse_unknown_paths_get_404(transport: SSETransport) -> None:
    get_response = _post(transport, "/nope", "{}")

    conn = http.client.HTTPConnection("127.0.0.1", transport.port, timeout=5)
    conn.request("GET", "/nope")
    unknown_get = conn.getresponse()
    unknown_get.read()
    conn.close()

    assert get_response.status == 404
    assert unknown_get.status == 404


def test_sse_options_preflight(transport: SSETransport) -> None:
    conn = http.client.HTTPConnection("127.0.0.1", transport.port, timeout=5)
    conn.request("OPTIONS", "/actions")
    response = conn.getresponse()
    response.read()
    conn.close()

    assert response.status == 204
    assert response.getheader("Access-Control-Allow-Origin") == "*"


def test_sse_drops_disconnected_client(transport: SSETransport) -> None:
    conn, _response = _open_events(transport)
    conn.close()
    transport.send({"version": "v0.9", "ping": {}})
    transport.send({"version": "v0.9", "ping2": {}})


def test_sse_close_ends_stream_and_actions(transport: SSETransport) -> None:
    conn, response = _open_events(transport)

    transport.close()

    assert list(_sse_frames(response)) == []
    assert list(transport.actions()) == []
    conn.close()


def test_sse_verbose_reports_lifecycle(capsys: pytest.CaptureFixture[str]) -> None:
    sse_transport = SSETransport(port=0, verbose=True)
    conn, response = _open_events(sse_transport)
    sse_transport.send({"version": "v0.9", "updateDataModel": {}})
    next(_sse_frames(response))
    sse_transport.close()
    conn.close()

    err = capsys.readouterr().err
    assert "[sse]" in err
    assert "listening on http://" in err
    assert "client connected" in err
    assert "sent 'updateDataModel'" in err
