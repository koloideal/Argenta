import re
import sys
from dataclasses import dataclass
from pathlib import Path

from argenta._cli.infrastructure.entrypoint_resolver.exceptions import (
    ResolveFromStringError,
)


@dataclass(frozen=True, slots=True)
class ModuleLocation:
    module_name: str
    resolved_source_path: str
    is_file_path: bool
    display_path: str


def resolve_module_location(path_to_entrypoint: str) -> ModuleLocation:
    raw_path = path_to_entrypoint

    raw_path_as_dir = Path(raw_path).resolve()
    if raw_path_as_dir.is_dir() and (raw_path_as_dir / "__main__.py").exists():
        raw_path = str(raw_path_as_dir / "__main__.py")

    if re.search(r"[\/\\]|\.py$", raw_path):
        return file_path_location(raw_path)
    return module_path_location(raw_path)


def module_path_location(module_name: str) -> ModuleLocation:
    cwd_str = str(Path.cwd())
    if cwd_str not in sys.path:
        sys.path.insert(0, cwd_str)
    return ModuleLocation(module_name, module_name, False, module_name)


def file_path_location(raw_path: str) -> ModuleLocation:
    abs_path = Path(raw_path).resolve()
    if not abs_path.exists():
        raise ResolveFromStringError(f'File "{raw_path}" not found')

    package_root = abs_path.parent
    while (package_root / "__init__.py").exists():
        package_root = package_root.parent

    pkg_root_str = str(package_root)
    if pkg_root_str not in sys.path:
        sys.path.insert(0, pkg_root_str)

    module_name = ".".join(abs_path.relative_to(package_root).with_suffix("").parts)
    return ModuleLocation(module_name, str(abs_path), True, raw_path)
