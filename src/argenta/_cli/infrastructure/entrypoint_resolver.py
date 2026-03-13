from dataclasses import dataclass
import inspect
import importlib.util
from pathlib import Path
from typing import Callable, Protocol, cast, overload

from argenta import App


class ResolverError(Exception):
    def __init__(self, entrypoint_as_repr: str) -> None:
        self.entrypoint_as_repr = entrypoint_as_repr

class ResolveFromStringError(ResolverError):
    pass
    
class EntrypointNotCallableError(ResolverError):
    def __str__(self):
        return f'Entrypoint {self.entrypoint_as_repr} is not callable'
        
class CallableEntrypointNotMatchRequiredSignatureError(ResolverError):
    def __str__(self) -> str:
        return f'Callable entrypoint {self.entrypoint_as_repr} not match with required signature Callable[[], ...]'
    
class EntrypointNotAppInstanceError(ResolverError):
    def __str__(self):
        return f'Entrypoint {self.entrypoint_as_repr} is not instance of App'


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
        self, entrypoint_type: type[CallableEntryPoint]
    ) -> EntryPoint[Callable[[], None]]: ...
    @overload
    def parse_entrypoint_with_type(
        self, entrypoint_type: type[EntryPointAsApp]
    ) -> EntryPoint[App]: ...

    def parse_entrypoint_with_type(
        self, entrypoint_type: type[CallableEntryPoint] | type[EntryPointAsApp]
    ) -> EntryPoint[Callable[[], None]] | EntryPoint[App]:
        if entrypoint_type is CallableEntryPoint:
            return self._parse_callable_entrypoint()
        elif entrypoint_type is EntryPointAsApp:
            return self._parse_entrypoint_as_app()
        raise NotImplementedError

    def _parse_callable_entrypoint(self) -> CallableEntryPoint:
        resolved_entrypoint = self._resolve_from_string()
        instance_object = resolved_entrypoint[1]
        if not callable(instance_object):
            raise EntrypointNotCallableError(repr(instance_object))
        instance_object_signature = inspect.signature(instance_object)
        required_params = instance_object_signature.parameters
        
        if required_params:
            raise CallableEntrypointNotMatchRequiredSignatureError(repr(instance_object))
        
        instance_object = cast(Callable[[], None], instance_object)
        return CallableEntryPoint(raw_path=resolved_entrypoint[0], instance_object=instance_object)

    def _parse_entrypoint_as_app(self) -> EntryPointAsApp:
        resolved_entrypoint = self._resolve_from_string()
        instance_object = resolved_entrypoint[1]
        if not isinstance(instance_object, App):
            raise EntrypointNotAppInstanceError(repr(instance_object))
        
        return EntryPointAsApp(raw_path=resolved_entrypoint[0], instance_object=instance_object)
        
    def _resolve_from_string(self) -> tuple[str, object]:
        file_path, _, attr_name = self._path_to_entrypoint.partition(":")
    
        if not file_path or not attr_name:
            raise ResolveFromStringError(
                f'"{self._path_to_entrypoint}" must be in format "<path/to/file.py>:<attribute>"'
            )
    
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
