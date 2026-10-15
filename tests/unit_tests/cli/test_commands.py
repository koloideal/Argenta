import importlib
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from argenta._cli.__main__ import app

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
    from argenta._cli.di import create_cli_container

    with create_cli_container() as container:
        result = runner.invoke(app, ["info"], obj=container)
    assert result.exit_code == 0


def test_main_entrypoint_runs(mocker: MockerFixture) -> None:
    mocker.patch.object(sys, "argv", ["argenta", "--version"])
    from argenta._cli import __main__ as cli_main

    with pytest.raises(SystemExit) as exc:
        cli_main.main()
    assert exc.value.code == 0


def test_module_runnable_as_script(mocker: MockerFixture) -> None:
    import runpy

    sys.modules.pop("argenta._cli.__main__", None)
    mocker.patch.object(sys, "argv", ["argenta", "--version"])
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("argenta._cli.__main__", run_name="__main__")
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
    import io

    from rich.console import Console

    from argenta._cli.commands.build import _resolve_build_target

    not_py = tmp_path / "thing.txt"
    not_py.write_text("x")
    console = Console(file=io.StringIO())

    with pytest.raises(SystemExit) as exc:
        _resolve_build_target(str(not_py), None, console)
    assert exc.value.code == 1


# ============================================================================
# `argenta compile-font`
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
    result = runner.invoke(app, ["compile-font", str(font_path)])

    assert result.exit_code == 0
    assert "Compiled" in result.output
    assert font_path.with_suffix(".flfd").read_bytes().startswith(b"FLFD")


def test_compile_font_writes_to_explicit_output(tmp_path: Path) -> None:
    font_path = _write_font(tmp_path)
    target = tmp_path / "dump.flfd"
    result = runner.invoke(app, ["compile-font", str(font_path), "-o", str(target)])

    assert result.exit_code == 0
    assert target.is_file()


def test_compile_font_fails_on_missing_source(tmp_path: Path) -> None:
    result = runner.invoke(app, ["compile-font", str(tmp_path / "missing.flf")])

    assert result.exit_code == 1
    assert "unreachable" in result.output


def test_compile_font_fails_on_invalid_font(tmp_path: Path) -> None:
    bad_font = tmp_path / "bad.flf"
    bad_font.write_text("not a font")
    result = runner.invoke(app, ["compile-font", str(bad_font)])

    assert result.exit_code == 1
    assert "Invalid" in result.output
