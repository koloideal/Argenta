import io
from pathlib import Path

import pytest
from rich.console import Console
from typer.testing import CliRunner

from argenta._cli.__main__ import app
from argenta._cli.commands._scaffold import create_file, sanitize_package_name

runner = CliRunner()


def _quiet_console() -> Console:
    return Console(file=io.StringIO())


# ============================================================================
# Helpers
# ============================================================================


def test_sanitize_package_name_replaces_spaces_and_dashes() -> None:
    assert sanitize_package_name("My Cool-App") == "my_cool_app"


def test_sanitize_package_name_keeps_valid_names() -> None:
    assert sanitize_package_name("project") == "project"


def test_create_file_writes_content_with_trailing_newline(tmp_path: Path) -> None:
    target = tmp_path / "sub" / "file.py"
    create_file(target, "content\n", _quiet_console())
    assert target.read_text() == "content\n"


def test_create_file_skips_existing(tmp_path: Path) -> None:
    target = tmp_path / "file.py"
    target.write_text("original")
    create_file(target, "new content", _quiet_console())
    assert target.read_text() == "original"


# ============================================================================
# `argenta new`
# ============================================================================


def test_new_creates_flat_layout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["new", "myproj"])

    assert result.exit_code == 0
    base = tmp_path / "myproj"
    assert (base / ".gitignore").read_text().startswith("__pycache__/")
    assert "Orchestrator" in (base / "main.py").read_text()
    assert "Router" in (base / "handlers.py").read_text()


def test_new_creates_src_layout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["new", "my-app", "--arch", "src"])

    assert result.exit_code == 0
    pkg = tmp_path / "my-app" / "src" / "my_app"
    app_pkg = pkg / "application"
    assert (app_pkg / "__main__.py").exists()
    assert (app_pkg / "routers.py").exists()
    assert (app_pkg / "handlers" / "hello_world_handler.py").exists()
    assert (tmp_path / "my-app" / "src" / "__init__.py").exists()
    assert (pkg / "__init__.py").exists()
    assert (app_pkg / "__init__.py").exists()
    assert (app_pkg / "handlers" / "__init__.py").exists()


def test_new_fails_when_directory_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "myproj").mkdir()
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["new", "myproj"])

    assert result.exit_code == 1
    assert "already exists" in result.output


def test_new_fails_on_invalid_project_name(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["new", "bad/name"])

    assert result.exit_code == 1
    assert "not a valid project name" in result.output


def test_new_fails_when_package_name_not_identifier(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["new", "1bad", "--arch", "src"])

    assert result.exit_code == 1
    assert "cannot derive a valid package name" in result.output


# ============================================================================
# `argenta init`
# ============================================================================


def test_init_creates_flat_layout_in_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_dir = tmp_path / "existing_proj"
    project_dir.mkdir()
    monkeypatch.chdir(project_dir)

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    assert (project_dir / "main.py").exists()
    assert (project_dir / "handlers.py").exists()
    assert (project_dir / ".gitignore").exists()


def test_init_creates_src_layout_in_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_dir = tmp_path / "existing_proj"
    project_dir.mkdir()
    monkeypatch.chdir(project_dir)

    result = runner.invoke(app, ["init", "--arch", "src"])

    assert result.exit_code == 0
    assert (project_dir / "src" / "existing_proj" / "application" / "__main__.py").exists()
    assert (project_dir / "src" / "existing_proj" / "application" / "routers.py").exists()


def test_init_fails_when_dir_name_not_identifier(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project_dir = tmp_path / "1bad"
    project_dir.mkdir()
    monkeypatch.chdir(project_dir)

    result = runner.invoke(app, ["init", "--arch", "src"])

    assert result.exit_code == 1
    assert "cannot derive a valid package name" in result.output


def test_init_skips_existing_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.py").write_text("original")

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    assert (tmp_path / "main.py").read_text() == "original"
    assert "Skipped" in result.output


# ============================================================================
# Unknown arch (typer Literal guards this, handlers stay defensive)
# ============================================================================


def test_init_with_unknown_arch_writes_only_gitignore(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from unittest.mock import MagicMock

    from argenta._cli.commands.init import init_handler

    monkeypatch.chdir(tmp_path)
    container = MagicMock()
    container.get.return_value = _quiet_console()

    init_handler(container, "bogus")  # type: ignore[arg-type]

    assert (tmp_path / ".gitignore").exists()
    assert not (tmp_path / "main.py").exists()
    assert not (tmp_path / "src").exists()


def test_scaffold_with_unknown_arch_writes_only_gitignore(tmp_path: Path) -> None:
    from argenta._cli.commands.new import _scaffold_project

    _scaffold_project(tmp_path, "proj", "bogus", _quiet_console())  # type: ignore[arg-type]

    assert (tmp_path / ".gitignore").exists()
    assert not (tmp_path / "main.py").exists()
    assert not (tmp_path / "src").exists()
