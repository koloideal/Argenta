import json
import threading
from io import StringIO

import pytest

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


class _TTYIO(StringIO):
    """Private. A StringIO that pretends to be a terminal"""

    def isatty(self) -> bool:
        return True


def test_stdio_announces_on_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    StdioTransport(out=StringIO(), inp=StringIO())

    assert "stdio transport" in capsys.readouterr().err


def test_stdio_warns_when_driven_by_a_terminal(capsys: pytest.CaptureFixture[str]) -> None:
    StdioTransport(out=StringIO(), inp=_TTYIO())

    assert "machine transport" in capsys.readouterr().err


def test_stdio_pretty_prints_when_stdout_is_a_tty() -> None:
    out = _TTYIO()

    StdioTransport(out=out, inp=StringIO()).send(
        {"version": "v0.9", "createSurface": {"surfaceId": "main"}}
    )

    assert '  "version": "v0.9",' in out.getvalue()


def test_stdio_verbose_reports_sent_kinds(capsys: pytest.CaptureFixture[str]) -> None:
    transport = StdioTransport(out=StringIO(), inp=StringIO(), verbose=True)

    transport.send({"version": "v0.9", "createSurface": {"surfaceId": "main"}})

    assert "sent 'createSurface'" in capsys.readouterr().err


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


def test_memory_messages_streams_outgoing() -> None:
    transport = MemoryTransport()
    transport.send({"a": 1})
    transport.send({"b": 2})
    transport.close()

    assert list(transport.messages()) == [{"a": 1}, {"b": 2}]


def test_memory_live_mode_streams_pushed_actions() -> None:
    transport = MemoryTransport(live=True)
    transport.push({"action": {"name": "a"}})
    transport.push({"action": {"name": "b"}})

    stream = transport.actions()
    assert next(stream) == {"action": {"name": "a"}}
    transport.close()
    assert next(stream) == {"action": {"name": "b"}}
    assert list(stream) == []


def test_memory_live_push_while_consuming() -> None:
    transport = MemoryTransport(live=True)
    stream = transport.actions()

    threading.Timer(0.1, lambda: transport.push({"action": {"name": "late"}})).start()

    assert next(stream) == {"action": {"name": "late"}}


def test_memory_live_actions_end_on_close() -> None:
    transport = MemoryTransport(live=True)
    transport.close()

    assert list(transport.actions()) == []
    assert list(transport.messages()) == []


def test_memory_script_mode_drops_pushed_actions() -> None:
    transport = MemoryTransport(incoming=[{"action": {"name": "preloaded"}}])
    transport.push({"action": {"name": "dropped"}})

    assert list(transport.actions()) == [{"action": {"name": "preloaded"}}]
