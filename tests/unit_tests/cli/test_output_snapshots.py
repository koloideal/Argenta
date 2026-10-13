import platform
import re
import sys
from pathlib import Path

import pytest
from syrupy import SnapshotAssertion
from typer.testing import CliRunner

from argenta._cli.__main__ import app

from .conftest import _APP_MODULE, _write_module

runner = CliRunner()


@pytest.fixture(autouse=True)
def _pin_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    # Rich falls back to COLUMNS/LINES when stdout is not a tty —
    # pin them so snapshots are identical locally and in CI.
    monkeypatch.setenv("COLUMNS", "100")
    monkeypatch.setenv("LINES", "40")

    # The info table right-justifies its value column, so its width —
    # and the whole rendered layout — depends on the platform string
    # length. Pin the underlying values instead of masking the output.
    monkeypatch.setattr(platform, "system", lambda: "TestOS")
    monkeypatch.setattr(platform, "release", lambda: "0.0.0-test")
    monkeypatch.setattr(platform, "machine", lambda: "test64")
    monkeypatch.setattr(sys, "version", "0.0.0 (test)")
    monkeypatch.setattr("argenta._cli.commands.info.version", lambda _name: "0.0.0")


def _normalize(output: str) -> str:
    return re.sub(r"0x[0-9a-f]+", "0xADDR", output)


def test_info_output(snapshot: SnapshotAssertion) -> None:
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert _normalize(result.output) == snapshot


def test_routes_output(tmp_path: Path, snapshot: SnapshotAssertion) -> None:
    module = _write_module(tmp_path, "snap_app", _APP_MODULE)
    result = runner.invoke(app, ["routes", f"{module}:application"])
    assert result.exit_code == 0
    assert _normalize(result.output) == snapshot
