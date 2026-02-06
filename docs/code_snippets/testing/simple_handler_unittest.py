import io
from contextlib import redirect_stdout

from argenta import Router, Command, Response
from argenta.command import InputCommand


router = Router(title="Demo")


@router.command(Command("PING", description="Ping command"))
def ping(response: Response):
    print("PONG")


def test_ping_prints_pong():
    # Call handler
    with redirect_stdout(io.StringIO()) as stdout:
        router.finds_appropriate_handler(InputCommand.parse("PING"))
    assert "PONG" in stdout.getvalue()
