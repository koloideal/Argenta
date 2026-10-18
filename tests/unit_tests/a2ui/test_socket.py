import io
import json
import socket
import struct
import time
from collections.abc import Iterator
from io import BufferedReader
from pathlib import Path

import pytest

from argenta.a2ui.transport.socket import SocketTransport


@pytest.fixture
def transport() -> Iterator[SocketTransport]:
    socket_transport = SocketTransport(port=0)
    yield socket_transport
    socket_transport.close()


def _connect(transport: SocketTransport) -> tuple[socket.socket, BufferedReader]:
    connection = socket.create_connection(("127.0.0.1", transport.port), timeout=5)
    return connection, connection.makefile("rb")


def test_socket_replays_history_to_late_client(transport: SocketTransport) -> None:
    transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})

    conn, reader = _connect(transport)

    assert "createSurface" in reader.readline().decode()
    conn.close()


def test_socket_streams_live_messages(transport: SocketTransport) -> None:
    conn, reader = _connect(transport)
    transport.send({"version": "v0.9", "updateDataModel": {"path": "/log", "value": "hi"}})

    assert "updateDataModel" in reader.readline().decode()
    conn.close()


def test_socket_action_line_reaches_actions(transport: SocketTransport) -> None:
    conn, _reader = _connect(transport)
    conn.sendall(json.dumps({"action": {"name": "deploy", "context": {}}}).encode() + b"\n")

    assert next(transport.actions()) == {"action": {"name": "deploy", "context": {}}}
    conn.close()


def test_socket_malformed_lines_are_skipped(transport: SocketTransport) -> None:
    conn, _reader = _connect(transport)
    conn.sendall(b"not json\n")
    conn.sendall(json.dumps({"action": {"name": "deploy"}}).encode() + b"\n")

    assert next(transport.actions()) == {"action": {"name": "deploy"}}
    conn.close()


def test_socket_client_reset_is_quiet(
    transport: SocketTransport, capsys: pytest.CaptureFixture[str]
) -> None:
    conn, _reader = _connect(transport)
    # SO_LINGER with a zero timeout makes close() send RST instead of FIN
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    conn.close()
    time.sleep(0.2)
    transport.send({"version": "v0.9", "ping": {}})

    assert "Traceback" not in capsys.readouterr().err


def test_socket_drops_disconnected_client(transport: SocketTransport) -> None:
    conn, _reader = _connect(transport)
    conn.close()
    transport.send({"version": "v0.9", "ping": {}})
    transport.send({"version": "v0.9", "ping2": {}})


def test_socket_send_unregisters_client_with_dead_writer(
    transport: SocketTransport,
) -> None:
    dead_conn = socket.socket()
    writer = io.BytesIO()
    client = transport.register_client(dead_conn, writer)
    writer.close()

    transport.send({"version": "v0.9", "ping": {}})

    assert client not in transport._clients
    dead_conn.close()


def test_socket_unix_path(tmp_path: Path) -> None:
    path = str(tmp_path / "agent.sock")
    unix_transport = SocketTransport(path=path)
    connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    connection.connect(path)
    unix_transport.send({"version": "v0.9", "ping": {}})

    assert "ping" in connection.makefile("rb").readline().decode()
    connection.close()
    unix_transport.close()
    assert not Path(path).exists()


def test_socket_close_ends_actions(transport: SocketTransport) -> None:
    transport.close()

    assert list(transport.actions()) == []


def test_socket_verbose_reports_lifecycle(capsys: pytest.CaptureFixture[str]) -> None:
    socket_transport = SocketTransport(port=0, verbose=True)
    conn, reader = _connect(socket_transport)
    socket_transport.send({"version": "v0.9", "updateDataModel": {}})
    reader.readline()
    conn.close()
    socket_transport.close()

    err = capsys.readouterr().err
    assert "[sock]" in err
    assert "listening on tcp://" in err
    assert "client connected" in err
    assert "sent 'updateDataModel'" in err
