import importlib
import io
import os
import runpy
import sys
import threading
import time
from pathlib import Path
from typing import Self
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from rich.console import Console
from typer.testing import CliRunner

from argenta._cli import __main__ as cli_main
from argenta._cli.__main__ import app
from argenta._cli.commands._reload import resolve_watch_root, supervise_cli
from argenta._cli.commands.build import _resolve_build_target
from argenta._cli.di import create_cli_container
from argenta.app.presentation.ascii_art import fetcher as fetcher_module

from .conftest import _APP_MODULE, _write_module

runner = CliRunner()


# ============================================================================
# App-level
# ============================================================================


def test_no_args_shows_help() -> None:
    result = runner.invoke(app, [])
    # typer's no_args_is_help prints usage and exits with click's usage-error code
    assert result.exit_code == 2
    assert "Usage" in result.output


def test_version_flag_prints_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "argenta" in result.output


def test_info_command_shows_environment() -> None:
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "Argenta version" in result.output
    assert "Python version" in result.output


def test_info_command_with_existing_context_object() -> None:
    with create_cli_container() as container:
        result = runner.invoke(app, ["info"], obj=container)
    assert result.exit_code == 0


def test_main_entrypoint_runs(mocker: MockerFixture) -> None:
    mocker.patch.object(sys, "argv", ["argenta", "--version"])
    with pytest.raises(SystemExit) as exc:
        cli_main.main()
    assert exc.value.code == 0


def test_module_runnable_as_script(mocker: MockerFixture) -> None:
    mocker.patch.object(sys, "argv", ["argenta", "--version"])
    with pytest.raises(SystemExit) as exc:
        runpy.run_path(str(cli_main.__file__), run_name="__main__")
    assert exc.value.code == 0


# ============================================================================
# `argenta run`
# ============================================================================


def test_run_invokes_entrypoint_callable(tmp_path: Path) -> None:
    path = _write_module(
        tmp_path, "climod_run_ok", 'def main():\n    print("ENTRYPOINT-RAN-MARKER")\n'
    )
    result = runner.invoke(app, ["run", f"{path}:main"])

    assert result.exit_code == 0
    assert "ENTRYPOINT-RAN-MARKER" in result.output
    # handler marks the process as runner-spawned; the autouse fixture cleans it up
    assert os.environ["RUN_FROM_ARGENTA_RUNNER"] == "1"


def test_run_leaves_a2ui_env_unset(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_run_plain", "def main():\n    pass\n")
    result = runner.invoke(app, ["run", f"{path}:main"])

    assert result.exit_code == 0
    assert "ARGENTA_RUN_MODE" not in os.environ
    assert "ARGENTA_A2UI_TRANSPORT" not in os.environ


# ============================================================================
# `argenta a2ui`
# ============================================================================


def test_a2ui_sets_agent_mode_env(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_run_a2ui", "def main():\n    pass\n")
    result = runner.invoke(app, ["a2ui", f"{path}:main"])

    assert result.exit_code == 0
    assert os.environ["RUN_FROM_ARGENTA_RUNNER"] == "1"
    assert os.environ["ARGENTA_RUN_MODE"] == "a2ui"


def test_a2ui_ws_transport_sets_env(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_run_ws", "def main():\n    pass\n")
    result = runner.invoke(app, ["a2ui", "--transport", "ws", "--port", "9999", f"{path}:main"])

    assert result.exit_code == 0
    assert os.environ["ARGENTA_A2UI_TRANSPORT"] == "ws"
    assert os.environ["ARGENTA_A2UI_WS_PORT"] == "9999"


def test_a2ui_transport_defaults_to_ws(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_run_std", "def main():\n    pass\n")
    result = runner.invoke(app, ["a2ui", f"{path}:main"])

    assert result.exit_code == 0
    assert os.environ["ARGENTA_A2UI_TRANSPORT"] == "ws"
    assert "ARGENTA_A2UI_WS_PORT" not in os.environ
    assert "ARGENTA_A2UI_VERBOSE" not in os.environ


def test_a2ui_stdio_transport_sets_env(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_run_stdio", "def main():\n    pass\n")
    result = runner.invoke(app, ["a2ui", "--transport", "stdio", f"{path}:main"])

    assert result.exit_code == 0
    assert os.environ["ARGENTA_A2UI_TRANSPORT"] == "stdio"


def test_a2ui_verbose_sets_env(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_run_verbose", "def main():\n    pass\n")
    result = runner.invoke(app, ["a2ui", "-v", f"{path}:main"])

    assert result.exit_code == 0
    assert os.environ["ARGENTA_A2UI_VERBOSE"] == "1"


def test_a2ui_fails_on_malformed_spec() -> None:
    result = runner.invoke(app, ["a2ui", "no_colon_here"])
    assert result.exit_code == 1
    assert "must be in format" in result.output


def test_a2ui_reload_supervises_and_exits(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_reload_ok", "def main():\n    pass\n")
    result = runner.invoke(app, ["a2ui", "--reload", f"{path}:main"])

    assert result.exit_code == 0
    assert "watching" in result.output
    assert "ARGENTA_RUN_MODE" not in os.environ  # env bridge lives in the child


def test_a2ui_reload_fails_on_unresolvable_module(tmp_path: Path) -> None:
    result = runner.invoke(app, ["a2ui", "--reload", "no_such_module_xyz:main"])

    assert result.exit_code == 1
    assert "cannot resolve a directory" in result.output


# ============================================================================
# `argenta a2ui --reload` supervisor
# ============================================================================


def test_resolve_watch_root_for_file(tmp_path: Path) -> None:
    module_path = tmp_path / "watched.py"
    module_path.write_text("x = 1")
    assert resolve_watch_root(str(module_path)) == tmp_path.resolve()


def test_resolve_watch_root_for_module() -> None:
    import argenta.app

    expected = Path(argenta.app.__file__).resolve().parent
    assert resolve_watch_root("argenta.app") == expected


def test_resolve_watch_root_unresolvable() -> None:
    assert resolve_watch_root("no_such_module_xyz.deep") is None


def test_supervise_restarts_on_file_change(tmp_path: Path) -> None:
    watched = tmp_path / "mod.py"
    watched.write_text("x = 1")
    counter = tmp_path / "count.txt"
    script = (
        "import pathlib, time\n"
        f"p = pathlib.Path({str(counter)!r})\n"
        "n = int(p.read_text()) + 1 if p.exists() else 1\n"
        "p.write_text(str(n))\n"
        "time.sleep(0 if n >= 2 else 30)\n"
    )
    args = [sys.executable, "-c", script]
    supervisor = threading.Thread(
        target=supervise_cli,
        args=(args, tmp_path, Console()),
    )
    supervisor.start()
    time.sleep(0.6)
    watched.write_text("x = 2")
    supervisor.join(timeout=20)

    assert not supervisor.is_alive()
    assert counter.read_text() == "2"


def test_supervise_stops_on_keyboard_interrupt(tmp_path: Path, mocker: MockerFixture) -> None:
    mocker.patch("watchfiles.watch", side_effect=KeyboardInterrupt)
    args = [sys.executable, "-c", "import time; time.sleep(30)"]

    supervise_cli(args, tmp_path, Console())  # terminates the sleeping child


def test_a2ui_fails_without_extra(mocker: MockerFixture, tmp_path: Path) -> None:
    mocker.patch("argenta._cli.commands.a2ui.find_spec", return_value=None)
    path = _write_module(tmp_path, "climod_no_extra", "def main():\n    pass\n")

    result = runner.invoke(app, ["a2ui", f"{path}:main"])

    assert result.exit_code == 1
    assert "argenta[a2ui]" in result.output


def test_run_fails_on_malformed_spec() -> None:
    result = runner.invoke(app, ["run", "no_colon_here"])
    assert result.exit_code == 1
    assert "must be in format" in result.output


def test_run_fails_on_missing_file() -> None:
    result = runner.invoke(app, ["run", "ghost_dir_xyz/missing.py:main"])
    assert result.exit_code == 1


# ============================================================================
# `argenta routes`
# ============================================================================


def test_routes_lists_app_commands(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_routes_app", _APP_MODULE)
    result = runner.invoke(app, ["routes", f"{path}:application"])

    assert result.exit_code == 0
    assert "mycmd" in result.output
    assert "Total Routers" in result.output


def test_routes_accepts_callable_returning_app(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_routes_callable", _APP_MODULE)
    result = runner.invoke(app, ["routes", f"{path}:create_app"])

    assert result.exit_code == 0
    assert "mycmd" in result.output


def test_routes_fails_when_callable_returns_non_app(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_routes_bad", "def make():\n    return 5\n")
    result = runner.invoke(app, ["routes", f"{path}:make"])

    assert result.exit_code == 1
    assert "must return an App instance" in result.output


def test_routes_fails_on_invalid_entrypoint_object(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "climod_routes_obj", "THING = 42\n")
    result = runner.invoke(app, ["routes", f"{path}:THING"])

    assert result.exit_code == 1


# ============================================================================
# `argenta build`
# ============================================================================


def _mock_nuitka_present(mocker: MockerFixture) -> MagicMock:
    mocker.patch("argenta._cli.commands.build.find_spec", return_value=MagicMock())
    return mocker.patch(
        "argenta._cli.commands.build.subprocess.run",
        return_value=MagicMock(returncode=0),
    )


def test_build_fails_without_nuitka(mocker: MockerFixture, tmp_path: Path) -> None:
    mocker.patch("argenta._cli.commands.build.find_spec", return_value=None)
    path = _write_module(tmp_path, "climod_build_nonuitka", "def main():\n    pass\n")

    result = runner.invoke(app, ["build", f"{path}:main"])

    assert result.exit_code == 1
    assert "nuitka is required" in result.output


def test_build_invokes_nuitka_with_defaults(mocker: MockerFixture, tmp_path: Path) -> None:
    run_mock = _mock_nuitka_present(mocker)
    path = _write_module(tmp_path, "climod_build_ok", "def main():\n    pass\n")

    result = runner.invoke(app, ["build", f"{path}:main", "--output", "mybin"])

    assert result.exit_code == 0
    nuitka_cmd = run_mock.call_args[0][0]
    assert "--onefile" in nuitka_cmd
    assert "--output-filename=mybin" in nuitka_cmd
    assert nuitka_cmd[-1] == str(path)


def test_build_targets_parent_dir_for_main_module(mocker: MockerFixture, tmp_path: Path) -> None:
    run_mock = _mock_nuitka_present(mocker)
    pkg_dir = tmp_path / "clipkg_mainpkg"
    pkg_dir.mkdir()
    main_path = pkg_dir / "__main__.py"
    main_path.write_text("def main():\n    pass\n")
    importlib.invalidate_caches()

    result = runner.invoke(app, ["build", f"{main_path}:main"])

    assert result.exit_code == 0
    nuitka_cmd = run_mock.call_args[0][0]
    assert "--python-flag=-m" in nuitka_cmd
    assert nuitka_cmd[-1] == str(pkg_dir)


def test_build_appends_extra_nuitka_args(mocker: MockerFixture, tmp_path: Path) -> None:
    run_mock = _mock_nuitka_present(mocker)
    path = _write_module(tmp_path, "climod_build_extra", "def main():\n    pass\n")

    result = runner.invoke(app, ["build", f"{path}:main", "--", "--lto=yes", "--include-package=x"])

    assert result.exit_code == 0
    nuitka_cmd = run_mock.call_args[0][0]
    assert "--lto=yes" in nuitka_cmd
    assert "--include-package=x" in nuitka_cmd


def test_build_propagates_nuitka_failure(mocker: MockerFixture, tmp_path: Path) -> None:
    mocker.patch("argenta._cli.commands.build.find_spec", return_value=MagicMock())
    mocker.patch(
        "argenta._cli.commands.build.subprocess.run",
        return_value=MagicMock(returncode=3),
    )
    path = _write_module(tmp_path, "climod_build_fail", "def main():\n    pass\n")

    result = runner.invoke(app, ["build", f"{path}:main"])

    assert result.exit_code == 3
    assert "Build failed" in result.output


def test_build_target_rejects_non_python_file(tmp_path: Path) -> None:
    not_py = tmp_path / "thing.txt"
    not_py.write_text("x")
    console = Console(file=io.StringIO())

    with pytest.raises(SystemExit) as exc:
        _resolve_build_target(str(not_py), None, console)
    assert exc.value.code == 1


# ============================================================================
# `argenta fonts compile`
# ============================================================================


def _write_font(tmp_path: Path, height: int = 2) -> Path:
    header = f"flf2a$ {height} {height} 10 0 0"
    rows: list[str] = []
    for codepoint in range(32, 127):
        glyph = [f"{chr(codepoint)}{index}" for index in range(height)]
        rows.extend(f"{row}@" for row in glyph[:-1])
        rows.append(f"{glyph[-1]}@@")
    font_path = tmp_path / "font.flf"
    font_path.write_text("\n".join([header, *rows]) + "\n", encoding="utf-8")
    return font_path


def test_compile_font_writes_dump(tmp_path: Path) -> None:
    font_path = _write_font(tmp_path)
    result = runner.invoke(app, ["fonts", "compile", str(font_path)])

    assert result.exit_code == 0
    assert "Compiled" in result.output
    assert font_path.with_suffix(".flfd").read_bytes().startswith(b"FLFD")


def test_compile_font_writes_to_explicit_output(tmp_path: Path) -> None:
    font_path = _write_font(tmp_path)
    target = tmp_path / "dump.flfd"
    result = runner.invoke(app, ["fonts", "compile", str(font_path), "-o", str(target)])

    assert result.exit_code == 0
    assert target.is_file()


def test_compile_font_fails_on_missing_source(tmp_path: Path) -> None:
    result = runner.invoke(app, ["fonts", "compile", str(tmp_path / "missing.flf")])

    assert result.exit_code == 1
    assert "unreachable" in result.output


def test_compile_font_fails_on_invalid_font(tmp_path: Path) -> None:
    bad_font = tmp_path / "bad.flf"
    bad_font.write_text("not a font")
    result = runner.invoke(app, ["fonts", "compile", str(bad_font)])

    assert result.exit_code == 1
    assert "Invalid" in result.output


# ============================================================================
# `argenta fonts fetch` and `argenta fonts list`
# ============================================================================


def test_fetch_font_downloads(tmp_path: Path, mocker: MockerFixture) -> None:
    class FakeResponse:
        def read(self) -> bytes:
            return _write_font(tmp_path).read_bytes()

        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_args: object) -> None:
            pass

    mocker.patch.object(fetcher_module, "urlopen", return_value=FakeResponse())
    result = runner.invoke(
        app,
        ["fonts", "fetch", "slant", "-o", str(tmp_path), "--cache-dir", str(tmp_path / "cache")],
    )

    assert result.exit_code == 0
    assert "Downloaded" in result.output
    assert (tmp_path / "slant.flf").is_file()


def test_fetch_font_fails_when_download_fails(tmp_path: Path, mocker: MockerFixture) -> None:
    mocker.patch.object(fetcher_module, "urlopen", side_effect=OSError("404"))
    result = runner.invoke(
        app,
        [
            "fonts",
            "fetch",
            "nosuchfont",
            "-o",
            str(tmp_path),
            "--cache-dir",
            str(tmp_path / "cache"),
        ],
    )

    assert result.exit_code == 1
    assert "Could not fetch" in result.output


def test_fonts_list_shows_names(mocker: MockerFixture) -> None:
    class FakeResponse:
        def read(self) -> bytes:
            return b'{"tree": [{"path": "fonts/slant.flf"}, {"path": "Slant2.flf"}]}'

        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_args: object) -> None:
            pass

    mocker.patch.object(fetcher_module, "urlopen", return_value=FakeResponse())
    result = runner.invoke(app, ["fonts", "list"])

    assert result.exit_code == 0
    assert "fonts available" in result.output
    assert "slant" in result.output


def test_fonts_list_fails_on_network_error(mocker: MockerFixture) -> None:
    mocker.patch.object(fetcher_module, "urlopen", side_effect=OSError("down"))
    result = runner.invoke(app, ["fonts", "list"])

    assert result.exit_code == 1
    assert "Could not fetch" in result.output


# ============================================================================
# `argenta fonts preview`
# ============================================================================


class _FontResponse:
    def __init__(self, body: bytes) -> None:
        self._body = body

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_args: object) -> None:
        pass


def test_preview_font_renders_banner(tmp_path: Path, mocker: MockerFixture) -> None:
    mocker.patch.object(
        fetcher_module,
        "urlopen",
        return_value=_FontResponse(_write_font(tmp_path).read_bytes()),
    )
    result = runner.invoke(
        app, ["fonts", "preview", "slant", "--cache-dir", str(tmp_path / "cache")]
    )

    assert result.exit_code == 0
    assert "A0" in result.output  # first glyph row of 'A' in "Argenta"


def test_preview_font_serves_second_run_from_cache(tmp_path: Path, mocker: MockerFixture) -> None:
    urlopen_mock = mocker.patch.object(
        fetcher_module,
        "urlopen",
        return_value=_FontResponse(_write_font(tmp_path).read_bytes()),
    )
    cache_dir = str(tmp_path / "cache")
    first = runner.invoke(app, ["fonts", "preview", "slant", "--cache-dir", cache_dir])
    second = runner.invoke(app, ["fonts", "preview", "slant", "--cache-dir", cache_dir])

    assert first.exit_code == 0
    assert second.exit_code == 0
    assert urlopen_mock.call_count == 1


def test_preview_font_no_cache_downloads_every_time(tmp_path: Path, mocker: MockerFixture) -> None:
    urlopen_mock = mocker.patch.object(
        fetcher_module,
        "urlopen",
        return_value=_FontResponse(_write_font(tmp_path).read_bytes()),
    )
    first = runner.invoke(app, ["fonts", "preview", "slant", "--no-cache"])
    second = runner.invoke(app, ["fonts", "preview", "slant", "--no-cache"])

    assert first.exit_code == 0
    assert second.exit_code == 0
    assert urlopen_mock.call_count == 2


def test_preview_font_fails_when_download_fails(tmp_path: Path, mocker: MockerFixture) -> None:
    mocker.patch.object(fetcher_module, "urlopen", side_effect=OSError("down"))
    result = runner.invoke(
        app, ["fonts", "preview", "nosuchfont", "--cache-dir", str(tmp_path / "cache")]
    )

    assert result.exit_code == 1
    assert "Could not fetch" in result.output
