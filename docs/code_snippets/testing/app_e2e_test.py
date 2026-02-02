import sys
from unittest.mock import patch
import pytest
from pytest import CaptureFixture

from argenta import App, Orchestrator, Router, Command, Response


@pytest.fixture(autouse=True)
def patched_argv():
    with patch.object(sys, "argv", ["program.py"]):
        yield


def test_input_incorrect_command(capsys: CaptureFixture[str]):
    router = Router()
    orchestrator = Orchestrator()

    @router.command(Command("test"))
    def test(response: Response) -> None:
        print("test command")

    app = App(override_system_messages=True, printer=print)
    app.include_router(router)
    app.set_unknown_command_handler(lambda command: print(f"Unknown command: {command.trigger}"))

    with patch("builtins.input", side_effect=["help", "q"]):
        orchestrator.start_polling(app)

    output = capsys.readouterr().out
    assert "\nUnknown command: help\n" in output
