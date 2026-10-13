import re
from pathlib import Path

import pytest
from syrupy import SnapshotAssertion
from typer.testing import CliRunner

from argenta._cli.__main__ import app

from .conftest import _APP_MODULE, _write_module

runner = CliRunner()


@pytest.fixture(autouse=True)
def _pin_terminal_size(monkeypatch: pytest.MonkeyPatch) -> None:
    # Rich falls back to COLUMNS/LINES when stdout is not a tty —
    # pin them so snapshots are identical locally and in CI.
    monkeypatch.setenv("COLUMNS", "100")
    monkeypatch.setenv("LINES", "40")


_DYNAMIC_ROW = re.compile(r"^(\s*(?:Argenta version|Python version|Platform)\s+)\S+.*$")


def _normalize(output: str) -> str:
    """Mask machine/version-specific values inside fixed-width table rows."""
    output = re.sub(r"0x[0-9a-f]+", "0xADDR", output)
    lines = [_DYNAMIC_ROW.sub(r"\1 <masked>", line).rstrip() for line in output.splitlines()]
    return "\n".join(lines) + "\n"


def test_info_output(snapshot: SnapshotAssertion) -> None:
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert _normalize(result.output) == snapshot


def test_routes_output(tmp_path: Path, snapshot: SnapshotAssertion) -> None:
    module = _write_module(tmp_path, "snap_app", _APP_MODULE)
    result = runner.invoke(app, ["routes", f"{module}:application"])
    assert result.exit_code == 0
    assert _normalize(result.output) == snapshot
