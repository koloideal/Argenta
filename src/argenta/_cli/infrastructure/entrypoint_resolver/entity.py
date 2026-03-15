__all__ = ['EntrypointResolver', 'EntryPointAsApp', 'CallableEntryPoint']

import inspect
from dataclasses import dataclass
from pathlib import Path
import sys
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


class EntrypointResolver[T: (CallableEntryPoint, EntryPointAsApp)]:
    def __init__(self, path_to_entrypoint: str):
        self._path_to_entrypoint = path_to_entrypoint

    def parse_entrypoint_with_type(
        self, entrypoint_object_name: str,
    ) -> T:
        entrypoint_type: type[T] = get_args(self.__orig_class__)[0]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        if entrypoint_type is CallableEntryPoint:
            return cast(T, self._parse_callable_entrypoint(entrypoint_object_name))
        elif entrypoint_type is EntryPointAsApp:
            return cast(T, self._parse_entrypoint_as_app(entrypoint_object_name))
        raise NotImplementedError

    def _parse_callable_entrypoint(self, entrypoint_object_name: str) -> CallableEntryPoint:
        resolved_entrypoint = self._resolve_from_string(entrypoint_object_name)
        instance_object = resolved_entrypoint[1]
        if not callable(instance_object):
            raise EntrypointNotCallableError(repr(instance_object))
        instance_object_signature = inspect.signature(instance_object)
        required_params = instance_object_signature.parameters

        if required_params:
            raise CallableEntrypointNotMatchRequiredSignatureError(repr(instance_object))

        instance_object = cast(Callable[[], None], instance_object)
        return CallableEntryPoint(raw_path=resolved_entrypoint[0], instance_object=instance_object)

    def _parse_entrypoint_as_app(self, entrypoint_object_name: str) -> EntryPointAsApp:
        resolved_entrypoint = self._resolve_from_string(entrypoint_object_name)
        instance_object = resolved_entrypoint[1]
        if not isinstance(instance_object, App):
            raise EntrypointNotAppInstanceError(repr(instance_object))

        return EntryPointAsApp(raw_path=resolved_entrypoint[0], instance_object=instance_object)

    def _resolve_from_string(self, entrypoint_object_name: str) -> tuple[str, object]:
        abs_path = Path(self._path_to_entrypoint).resolve()
        if not abs_path.exists():
            raise ResolveFromStringError(f'File "{self._path_to_entrypoint}" not found')
    
        package_root = abs_path.parent
        while (package_root / "__init__.py").exists():
            package_root = package_root.parent
    
        pkg_root_str = str(package_root)
        if pkg_root_str not in sys.path:
            sys.path.insert(0, pkg_root_str)
    
        module_name = ".".join(abs_path.relative_to(package_root).with_suffix("").parts)
    
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            raise ResolveFromStringError(f'Cannot import module "{module_name}": {e}')
    
        try:
            instance = getattr(module, entrypoint_object_name)
        except AttributeError:
            raise ResolveFromStringError(
                f'"{entrypoint_object_name}" not found in "{self._path_to_entrypoint}"'
            )
            
        return str(abs_path), instance

