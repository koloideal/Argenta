import json
from io import StringIO

from argenta.a2ui.transport import MemoryTransport, StdioTransport


def test_stdio_send_writes_json_lines() -> None:
    out = StringIO()
    transport = StdioTransport(out=out, inp=StringIO())

    transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})
    transport.send({"version": "v0.9", "deleteSurface": {"surfaceId": "main"}})

    lines = out.getvalue().split("\n")
    assert json.loads(lines[0])["createSurface"]["surfaceId"] == "main"
    assert json.loads(lines[1])["deleteSurface"]["surfaceId"] == "main"
    assert lines[2] == ""


def test_stdio_send_non_ascii() -> None:
    out = StringIO()
    transport = StdioTransport(out=out, inp=StringIO())

    transport.send({"text": "привет"})

    assert "привет" in out.getvalue()


def test_stdio_actions_reads_json_lines() -> None:
    incoming = StringIO('{"action": {"name": "a"}}\n{"action": {"name": "b"}}\n')
    transport = StdioTransport(out=StringIO(), inp=incoming)

    messages = list(transport.actions())

    assert messages == [{"action": {"name": "a"}}, {"action": {"name": "b"}}]


def test_stdio_actions_skips_blank_and_malformed() -> None:
    incoming = StringIO('\n   \nnot json\n{"action": {"name": "a"}}\n')
    transport = StdioTransport(out=StringIO(), inp=incoming)

    messages = list(transport.actions())

    assert messages == [{"action": {"name": "a"}}]


def test_stdio_close_flushes_output() -> None:
    out = StringIO()
    transport = StdioTransport(out=out, inp=StringIO())

    transport.send({"a": 1})
    transport.close()

    assert out.getvalue().endswith("\n")


def test_memory_transport_stores_sent() -> None:
    transport = MemoryTransport()

    transport.send({"a": 1})
    transport.send({"b": 2})

    assert transport.sent == [{"a": 1}, {"b": 2}]


def test_memory_transport_replays_incoming() -> None:
    transport = MemoryTransport(incoming=[{"action": {"name": "x"}}])

    assert list(transport.actions()) == [{"action": {"name": "x"}}]


def test_memory_transport_empty_by_default() -> None:
    transport = MemoryTransport()

    assert list(transport.actions()) == []
    assert transport.sent == []
