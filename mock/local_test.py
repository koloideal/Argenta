import _io
from io import StringIO
from unittest.mock import patch, MagicMock
import io
from argenta.app import App
from argenta.command import Command
from argenta.router import Router


def run_shell():
    router = Router()

    @router.command(Command('test'))
    def test():
        print('loh ibanu')

    app = App()
    app.include_router(router)

    app.start_polling()


@patch("builtins.input", side_effect=["test", "q"])
@patch("sys.stdout", new_callable=io.StringIO)
def test_run_shell_output(mock_stdout: _io.StringIO, magick_mock: MagicMock):
    run_shell()
    output = mock_stdout.getvalue()

    assert "loh ibanu" in output
    return magick_mock


res = test_run_shell_output()
print(res)
print(type(res))

print("✅ Тест вывода пройден!")

