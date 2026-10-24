import json
import sys
from collections.abc import Iterator
from contextlib import suppress
from typing import TextIO

from argenta.a2ui._verbose import VerboseLog
from argenta.a2ui.models import Message


class StdioTransport:
    """
    Public. JSON Lines transport over stdin/stdout:
    one JSON message per line in both directions. stdout carries the
    protocol, so this transport is meant for machine clients; diagnostics
    go to stderr
    """

    def __init__(
        self, out: TextIO = sys.stdout, inp: TextIO = sys.stdin, *, verbose: bool = False
    ) -> None:
        self._out = out
        self._inp = inp
        self._indent: int | None = 2 if out.isatty() else None
        self._verbose = VerboseLog(verbose, "stdio")
        if inp.isatty():
            self._verbose.report(
                "stdio is a machine transport — usually driven by a parent process "
                "piping stdin/stdout; for the browser UI run 'argenta a2ui -t ws'",
                always=True,
                style="bold red",
            )
        else:
            self._verbose.report(
                "stdio transport: emitting JSONL protocol on stdout, reading actions from stdin",
                always=True,
            )

    def send(self, message: Message) -> None:
        payload = json.dumps(message, ensure_ascii=False, indent=self._indent)
        self._out.write(f"{payload}\n")
        self._out.flush()
        kind = next(key for key in message if key != "version")
        self._verbose.report(f"sent '{kind}'")

    def actions(self) -> Iterator[Message]:
        for line in self._inp:
            stripped = line.strip()
            if not stripped:
                continue
            with suppress(json.JSONDecodeError):
                yield json.loads(stripped)

    def close(self) -> None:
        self._out.flush()
