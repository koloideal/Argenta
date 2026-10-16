import importlib
import io
import sys
from pathlib import Path
from typing import Any

import pytest
from pytest_mock import MockerFixture
from rich.console import Console

from argenta import App
from argenta._cli.commands._entrypoint import (
    report_entrypoint_error,
    resolve_callable_entrypoint,
    split_entrypoint_spec,
)
from argenta._cli.infrastructure.entrypoint_resolver._location import (
    resolve_module_location,
)
from argenta._cli.infrastructure.entrypoint_resolver.entity import (
    CallableEntryPoint,
    EntryPointAsApp,
    EntrypointResolver,
)
from argenta._cli.infrastructure.entrypoint_resolver.exceptions import (
    CallableEntrypointNotMatchRequiredSignatureError,
    EntrypointNotAppInstanceError,
    EntrypointNotCallableError,
    ResolveFromStringError,
)


def _write_module(tmp_path: Path, name: str, body: str) -> Path:
    path = tmp_path / f"{name}.py"
    path.write_text(body)
    importlib.invalidate_caches()
    return path


def _quiet_console() -> Console:
    return Console(file=io.StringIO())


def _console_and_buffer() -> tuple[Console, io.StringIO]:
    buffer = io.StringIO()
    return Console(file=buffer), buffer


# ============================================================================
# resolve_module_location
# ============================================================================


def test_resolve_location_for_file_path(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "clipkg_filemod", "X = 1")
    location = resolve_module_location(str(path))

    assert location.is_file_path is True
    assert location.module_name == "clipkg_filemod"
    assert location.resolved_source_path == str(path)


def test_resolve_location_for_module_name() -> None:
    location = resolve_module_location("clipkg_plainmod")

    assert location.is_file_path is False
    assert location.module_name == "clipkg_plainmod"


def test_resolve_location_for_directory_with_main(tmp_path: Path) -> None:
    pkg_dir = tmp_path / "clipkg_dir"
    pkg_dir.mkdir()
    (pkg_dir / "__main__.py").write_text("def main(): pass\n")
    location = resolve_module_location(str(pkg_dir))

    assert location.is_file_path is True
    assert location.resolved_source_path == str(pkg_dir / "__main__.py")


def test_resolve_location_raises_for_missing_file() -> None:
    with pytest.raises(ResolveFromStringError, match="not found"):
        resolve_module_location("nonexistent_dir_xyz/missing.py")


def test_resolve_location_walks_up_package_dirs(tmp_path: Path) -> None:
    pkg_dir = tmp_path / "clipkg_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    mod = _write_module(pkg_dir, "clipkg_pkgmod", "def main():\n    pass\n")

    location = resolve_module_location(str(mod))

    assert location.module_name == "clipkg_pkg.clipkg_pkgmod"
    assert location.resolved_source_path == str(mod)


def test_module_location_inserts_cwd_into_syspath(tmp_path: Path, mocker: MockerFixture) -> None:
    cwd = str(Path.cwd())
    mocker.patch.object(sys, "path", [p for p in sys.path if p != cwd])

    resolve_module_location("clipkg_anymod")

    assert cwd in sys.path


# ============================================================================
# EntrypointResolver[CallableEntryPoint]
# ============================================================================


def test_resolver_finds_zero_arg_callable(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "clipkg_okcall", "def main():\n    return 42\n")
    resolved = EntrypointResolver[CallableEntryPoint](str(path)).parse_entrypoint_with_type("main")

    assert resolved.instance_object() == 42
    assert resolved.raw_path == str(path)


def test_resolver_rejects_callable_with_required_params(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "clipkg_reqargs", "def main(arg):\n    pass\n")
    with pytest.raises(CallableEntrypointNotMatchRequiredSignatureError, match="not match"):
        EntrypointResolver[CallableEntryPoint](str(path)).parse_entrypoint_with_type("main")


def test_resolver_rejects_callable_without_signature(tmp_path: Path) -> None:
    path = _write_module(
        tmp_path,
        "clipkg_nosig",
        "class Weird:\n"
        "    @property\n"
        "    def __signature__(self):\n"
        "        raise ValueError('no sig')\n"
        "    def __call__(self):\n"
        "        pass\n"
        "weird = Weird()\n",
    )
    with pytest.raises(CallableEntrypointNotMatchRequiredSignatureError):
        EntrypointResolver[CallableEntryPoint](str(path)).parse_entrypoint_with_type("weird")


def test_resolver_rejects_non_callable_attribute(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "clipkg_notcall", "THING = 5\n")
    with pytest.raises(ResolveFromStringError, match="not a valid entrypoint"):
        EntrypointResolver[CallableEntryPoint](str(path)).parse_entrypoint_with_type("THING")


def test_resolver_rejects_class_attribute(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "clipkg_classattr", "class Thing:\n    pass\n")
    with pytest.raises(ResolveFromStringError, match="not a valid entrypoint"):
        EntrypointResolver[CallableEntryPoint](str(path)).parse_entrypoint_with_type("Thing")


def test_resolver_rejects_app_instance_as_callable(tmp_path: Path) -> None:
    path = _write_module(
        tmp_path, "clipkg_appval", "from argenta import App\napplication = App()\n"
    )
    with pytest.raises(EntrypointNotCallableError, match="not callable"):
        EntrypointResolver[CallableEntryPoint](str(path)).parse_entrypoint_with_type("application")


def test_resolver_raises_for_missing_attribute(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "clipkg_noattr", "X = 1\n")
    with pytest.raises(ResolveFromStringError, match="not found"):
        EntrypointResolver[CallableEntryPoint](str(path)).parse_entrypoint_with_type("missing")


def test_resolver_raises_for_missing_module() -> None:
    with pytest.raises(ResolveFromStringError, match="Cannot import module"):
        EntrypointResolver[CallableEntryPoint]("clipkg_no_such_module").parse_entrypoint_with_type(
            "main"
        )


def test_resolver_raises_when_module_import_fails(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "clipkg_broken", "import clipkg_definitely_missing_dep\n")
    with pytest.raises(ResolveFromStringError, match="Cannot import module"):
        EntrypointResolver[CallableEntryPoint](str(path)).parse_entrypoint_with_type("main")


def test_resolver_resolves_module_by_name(tmp_path: Path, mocker: MockerFixture) -> None:
    _write_module(tmp_path, "clipkg_bymodname", "def main():\n    return 'by-name'\n")
    mocker.patch.object(sys, "path", [str(tmp_path), *sys.path])

    resolved = EntrypointResolver[CallableEntryPoint](
        "clipkg_bymodname"
    ).parse_entrypoint_with_type("main")

    assert resolved.instance_object() == "by-name"


def test_resolver_rejects_unknown_parametrization(tmp_path: Path) -> None:
    with pytest.raises(NotImplementedError):
        EntrypointResolver[Any](str(tmp_path)).parse_entrypoint_with_type("x")


def test_unparametrized_resolver_raises() -> None:
    with pytest.raises(ResolveFromStringError, match="must be parametrized"):
        EntrypointResolver("whatever").parse_entrypoint_with_type("main")


# ============================================================================
# EntrypointResolver[EntryPointAsApp]
# ============================================================================


def test_resolver_finds_app_instance(tmp_path: Path) -> None:
    path = _write_module(
        tmp_path, "clipkg_appinst", "from argenta import App\napplication = App()\n"
    )
    resolved = EntrypointResolver[EntryPointAsApp](str(path)).parse_entrypoint_with_type(
        "application"
    )
    assert isinstance(resolved.instance_object, App)


def test_resolver_rejects_non_app_for_app_type(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "clipkg_notapp", "def main():\n    pass\n")
    with pytest.raises(EntrypointNotAppInstanceError, match="not instance of App"):
        EntrypointResolver[EntryPointAsApp](str(path)).parse_entrypoint_with_type("main")


# ============================================================================
# _entrypoint helpers
# ============================================================================


def test_split_entrypoint_spec_parses_valid_spec() -> None:
    spec = split_entrypoint_spec("a/b.py:main", _quiet_console(), format_hint="HINT")
    assert spec.file_path == "a/b.py"
    assert spec.callable_name == "main"


@pytest.mark.parametrize("bad", ["nocolon", "file.py:", ":main", ""])
def test_split_entrypoint_spec_exits_on_invalid(bad: str) -> None:
    console, buffer = _console_and_buffer()
    with pytest.raises(SystemExit) as exc:
        split_entrypoint_spec(bad, console, format_hint="HINT")
    assert exc.value.code == 1
    assert "HINT" in buffer.getvalue()


def test_resolve_callable_entrypoint_reports_errors(tmp_path: Path) -> None:
    path = _write_module(tmp_path, "clipkg_errcall", "THING = 1\n")
    console, buffer = _console_and_buffer()
    with pytest.raises(SystemExit) as exc:
        resolve_callable_entrypoint(
            split_entrypoint_spec(f"{path}:THING", console, format_hint="H"), console
        )
    assert exc.value.code == 1
    assert "Error:" in buffer.getvalue()


def test_report_entrypoint_error_exits() -> None:
    console, buffer = _console_and_buffer()
    with pytest.raises(SystemExit):
        report_entrypoint_error(console, ResolveFromStringError("boom"))
    assert "boom" in buffer.getvalue()
