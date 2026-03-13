__all__ = ['EntrypointResolver', 'EntryPointAsApp', 'CallableEntryPoint']

import importlib.util
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol, cast, overload

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


class EntrypointResolver:
    def __init__(self, path_to_entrypoint: str):
        self._path_to_entrypoint = path_to_entrypoint

    @overload
    def parse_entrypoint_with_type(
        self, entrypoint_object_name: str, entrypoint_type: type[CallableEntryPoint]
    ) -> EntryPoint[Callable[[], None]]: ...
    @overload
    def parse_entrypoint_with_type(
        self, entrypoint_object_name: str, entrypoint_type: type[EntryPointAsApp]
    ) -> EntryPoint[App]: ...

    def parse_entrypoint_with_type(
        self,
        entrypoint_object_name: str,
        entrypoint_type: type[CallableEntryPoint] | type[EntryPointAsApp],
    ) -> EntryPoint[Callable[[], None]] | EntryPoint[App]:
        if entrypoint_type is CallableEntryPoint:
            return self._parse_callable_entrypoint(entrypoint_object_name)
        elif entrypoint_type is EntryPointAsApp:
            return self._parse_entrypoint_as_app(entrypoint_object_name)
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
        file_path: str = self._path_to_entrypoint
        attr_name: str = entrypoint_object_name

        path = Path(file_path).resolve()
        if not path.exists():
            raise ResolveFromStringError(f'File "{file_path}" not found')

        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            raise ResolveFromStringError(f'Cannot load module from "{file_path}"')

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        try:
            instance = getattr(module, attr_name)
        except AttributeError:
            raise ResolveFromStringError(f'"{attr_name}" not found in "{file_path}"')

        return file_path, instance
