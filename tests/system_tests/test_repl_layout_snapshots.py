import sys
from collections.abc import Iterator

import pytest
from syrupy.assertion import SnapshotAssertion

from argenta import App, Orchestrator, Router
from argenta.app import PredefinedMessages
from argenta.command import Command
from argenta.repl import DynamicDividingLine, REPLConfig, StaticDividingLine
from argenta.response import Response

type _DividingLine = StaticDividingLine | DynamicDividingLine | None

_SESSION = ("hello", "bogus", "hello -f -f", "", "q")


@pytest.fixture(autouse=True)
def patch_argv(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["program.py"])


def _feed(monkeypatch: pytest.MonkeyPatch, inputs: Iterator[str]) -> None:
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))


def _router(*, disable_redirect_stdout: bool = False) -> Router:
    router = Router(title="Main:", disable_redirect_stdout=disable_redirect_stdout)

    @router.command(Command("hello", description="Says hello"))
    def hello(_response: Response) -> None:
        print("hello from handler")
        print("second, longer line of handler output")

    return router


def _run_session(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    dividing_line: _DividingLine,
    *,
    plain: bool = True,
    repeat_groups: bool = False,
    disable_redirect_stdout: bool = False,
) -> str:
    _feed(monkeypatch, iter(_SESSION))
    app = App(
        initial_message="Banner",
        override_system_messages=plain,
        repeat_command_groups_printing=repeat_groups,
        printer=print if plain else None,
    )
    app.add_message_on_startup(PredefinedMessages.USAGE)
    app.include_router(_router(disable_redirect_stdout=disable_redirect_stdout))
    Orchestrator().run_repl(app, REPLConfig(dividing_line=dividing_line))
    return capsys.readouterr().out


def test_plain_without_dividing_line(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], snapshot: SnapshotAssertion
) -> None:
    assert _run_session(monkeypatch, capsys, None) == snapshot


def test_plain_static_dividing_line(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], snapshot: SnapshotAssertion
) -> None:
    assert _run_session(monkeypatch, capsys, StaticDividingLine("~")) == snapshot


def test_plain_dynamic_dividing_line(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], snapshot: SnapshotAssertion
) -> None:
    assert _run_session(monkeypatch, capsys, DynamicDividingLine("-")) == snapshot


def test_plain_dynamic_line_with_redirect_disabled(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], snapshot: SnapshotAssertion
) -> None:
    output = _run_session(
        monkeypatch, capsys, DynamicDividingLine("-"), disable_redirect_stdout=True
    )
    assert output == snapshot


def test_plain_repeated_command_groups(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], snapshot: SnapshotAssertion
) -> None:
    output = _run_session(monkeypatch, capsys, StaticDividingLine("~"), repeat_groups=True)
    assert output == snapshot


def test_rich_static_dividing_line(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], snapshot: SnapshotAssertion
) -> None:
    output = _run_session(monkeypatch, capsys, StaticDividingLine("="), plain=False)
    assert output == snapshot
