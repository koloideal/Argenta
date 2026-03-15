__all__ = ["EntrypointResolver", "EntryPointAsApp", "CallableEntryPoint"]

import importlib
import inspect
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol, cast, get_args

from argenta.app.models import App

from .exceptions import (
    CallableEntrypointNotMatchRequiredSignatureError,
    EntrypointNotAppInstanceError,
    EntrypointNotCallableError,
    ResolveFromStringError,
)


class EntryPoint[T](Protocol):
    @property
    def raw_path(self) -> str: ...
    @property
    def instance_object(self) -> T: ...


@dataclass(frozen=True, slots=True)
class CallableEntryPoint:
    raw_path: str
    instance_object: Callable[[], None]


@dataclass(frozen=True, slots=True)
class EntryPointAsApp:
    raw_path: str
    instance_object: App


@dataclass(frozen=True, slots=True)
class ResolvedEntrypoint:
    resolved_source_path: str
    instance: Callable[[], None] | App


class EntrypointResolver[T: (CallableEntryPoint, EntryPointAsApp)]:
    def __init__(self, path_to_entrypoint: str):
        self._path_to_entrypoint = path_to_entrypoint

    def parse_entrypoint_with_type(
        self,
        entrypoint_object_name: str,
    ) -> T:
        entrypoint_type: type[T] = get_args(self.__orig_class__)[0]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        if entrypoint_type is CallableEntryPoint:
            return cast(T, self._parse_callable_entrypoint(entrypoint_object_name))
        elif entrypoint_type is EntryPointAsApp:
            return cast(T, self._parse_entrypoint_as_app(entrypoint_object_name))
        raise NotImplementedError

    def _parse_callable_entrypoint(self, entrypoint_object_name: str) -> CallableEntryPoint:
        resolved_entrypoint = self._resolve_from_string(entrypoint_object_name)
        instance_object = resolved_entrypoint.instance
        if not callable(instance_object):
            raise EntrypointNotCallableError(repr(instance_object))
        instance_object_signature = inspect.signature(instance_object)
        required_params = instance_object_signature.parameters

        if required_params:
            raise CallableEntrypointNotMatchRequiredSignatureError(repr(instance_object))

        return CallableEntryPoint(raw_path=resolved_entrypoint.resolved_source_path, instance_object=instance_object)

    def _parse_entrypoint_as_app(self, entrypoint_object_name: str) -> EntryPointAsApp:
        resolved_entrypoint = self._resolve_from_string(entrypoint_object_name)
        instance_object = resolved_entrypoint[1]
        if not isinstance(instance_object, App):
            raise EntrypointNotAppInstanceError(repr(instance_object))

        return EntryPointAsApp(raw_path=resolved_entrypoint[0], instance_object=instance_object)

    def _resolve_from_string(self, entrypoint_object_name: str) -> ResolvedEntrypoint:
        raw_path = self._path_to_entrypoint

        raw_path_as_dir = Path(raw_path).resolve()
        if raw_path_as_dir.is_dir() and (raw_path_as_dir / "__main__.py").exists():
            raw_path = str(raw_path_as_dir / "__main__.py")

        is_file_path = bool(re.search(r"[\/\\]|\.py$", raw_path))

        if is_file_path:
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
            resolved_source_path = str(abs_path)

        else:
            module_name = raw_path
            cwd_str = str(Path.cwd())
            if cwd_str not in sys.path:
                sys.path.insert(0, cwd_str)

            resolved_source_path = module_name

        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            if not is_file_path and not module_name.endswith(".__main__"):
                try:
                    main_module_name = f"{module_name}.__main__"
                    module = importlib.import_module(main_module_name)
                    module_name = main_module_name
                except ImportError:
                    raise ResolveFromStringError(f'Cannot import module "{module_name}": {e}')
            else:
                raise ResolveFromStringError(f'Cannot import module "{module_name}": {e}')

        if not is_file_path:
            resolved_source_path = getattr(module, "__file__", resolved_source_path)

        try:
            instance = getattr(module, entrypoint_object_name)
        except AttributeError:
            raise ResolveFromStringError(f'"{entrypoint_object_name}" not found in "{raw_path}"')

        return ResolvedEntrypoint(resolved_source_path, instance)
