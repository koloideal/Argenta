import runpy
from pathlib import Path

import pytest

from argenta.command import InputCommand
from argenta.router import Router


@pytest.fixture
def calculator_router() -> Router:
    snippet_path = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "code_snippets"
        / "quickstart"
        / "calculator_app.py"
    )
    namespace = runpy.run_path(str(snippet_path))
    router = namespace["router"]
    assert isinstance(router, Router)
    return router


@pytest.mark.parametrize(
    ("command", "result"),
    [
        ("calc --a 10 --b 5 --operation add", "15.0"),
        ("calc --a 10 --b 5 --operation mul", "50.0"),
    ],
)
def test_documented_calculator_commands(
    calculator_router: Router, capsys: pytest.CaptureFixture[str], command: str, result: str
) -> None:
    calculator_router.finds_appropriate_handler(InputCommand.parse(command))

    assert capsys.readouterr().out == f"Result: {result}\n"


def test_calculator_reports_missing_operation(
    calculator_router: Router, capsys: pytest.CaptureFixture[str]
) -> None:
    calculator_router.finds_appropriate_handler(InputCommand.parse("calc --a 10 --b 5"))

    assert capsys.readouterr().out == "Error: must specify --a, --b and --operation\n"
