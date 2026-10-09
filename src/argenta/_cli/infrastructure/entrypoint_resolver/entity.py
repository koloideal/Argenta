import importlib
import inspect
from collections.abc import Callable
from dataclasses import dataclass
from types import ModuleType
from typing import cast, get_args

from argenta._cli.infrastructure.entrypoint_resolver._location import (
    resolve_module_location,
)
from argenta._cli.infrastructure.entrypoint_resolver.exceptions import (
    CallableEntrypointNotMatchRequiredSignatureError,
    EntrypointNotAppInstanceError,
    EntrypointNotCallableError,
    ResolveFromStringError,
)
from argenta.app.models import App

EntrypointCallable = Callable[[], object]


@dataclass(frozen=True, slots=True)
class CallableEntryPoint:
    raw_path: str
    instance_object: EntrypointCallable


@dataclass(frozen=True, slots=True)
class EntryPointAsApp:
    raw_path: str
    instance_object: App


@dataclass(frozen=True, slots=True)
class ResolvedEntrypoint[InstanceT]:
    resolved_source_path: str
    instance: InstanceT


def _import_entrypoint_module(module_name: str, *, is_file_path: bool) -> ModuleType:
    try:
        return importlib.import_module(module_name)
    except ImportError as error:
        if is_file_path or module_name.endswith(".__main__"):
            raise ResolveFromStringError(f'Cannot import module "{module_name}": {error}')
        return _import_main_fallback(module_name, error)


def _import_main_fallback(module_name: str, error: ImportError) -> ModuleType:
    try:
        return importlib.import_module(f"{module_name}.__main__")
    except ImportError:
        raise ResolveFromStringError(f'Cannot import module "{module_name}": {error}')


class EntrypointResolver[EntrypointT: (CallableEntryPoint, EntryPointAsApp)]:
    def __init__(self, path_to_entrypoint: str):
        self._path_to_entrypoint = path_to_entrypoint

    def parse_entrypoint_with_type(
        self,
        entrypoint_object_name: str,
    ) -> EntrypointT:
        orig_class = getattr(self, "__orig_class__", None)
        if orig_class is None:
            raise ResolveFromStringError(
                "EntrypointResolver must be parametrized, e.g. "
                "EntrypointResolver[CallableEntryPoint](path)"
            )
        entrypoint_type = get_args(orig_class)[0]
        parsed: CallableEntryPoint | EntryPointAsApp
        if entrypoint_type is CallableEntryPoint:
            parsed = self._parse_callable_entrypoint(entrypoint_object_name)
        elif entrypoint_type is EntryPointAsApp:
            parsed = self._parse_entrypoint_as_app(entrypoint_object_name)
        else:
            raise NotImplementedError
        return cast(EntrypointT, parsed)

    def _parse_callable_entrypoint(self, entrypoint_object_name: str) -> CallableEntryPoint:
        resolved_entrypoint = self._resolve_from_string(entrypoint_object_name)
        instance_object = resolved_entrypoint.instance
        if isinstance(instance_object, App) or not callable(instance_object):
            raise EntrypointNotCallableError(repr(instance_object))
        try:
            instance_object_signature = inspect.signature(instance_object)
        except (TypeError, ValueError):
            raise CallableEntrypointNotMatchRequiredSignatureError(repr(instance_object))
        required_params = [
            parameter
            for parameter in instance_object_signature.parameters.values()
            if parameter.default is inspect.Parameter.empty
            and parameter.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            )
        ]

        if required_params:
            raise CallableEntrypointNotMatchRequiredSignatureError(repr(instance_object))

        return CallableEntryPoint(
            raw_path=resolved_entrypoint.resolved_source_path, instance_object=instance_object
        )

    def _parse_entrypoint_as_app(self, entrypoint_object_name: str) -> EntryPointAsApp:
        resolved_entrypoint = self._resolve_from_string(entrypoint_object_name)
        instance_object = resolved_entrypoint.instance
        if not isinstance(instance_object, App):
            raise EntrypointNotAppInstanceError(repr(instance_object))

        return EntryPointAsApp(
            raw_path=resolved_entrypoint.resolved_source_path, instance_object=instance_object
        )

    def _resolve_from_string(
        self, entrypoint_object_name: str
    ) -> ResolvedEntrypoint[EntrypointCallable | App]:
        location = resolve_module_location(self._path_to_entrypoint)

        module = _import_entrypoint_module(location.module_name, is_file_path=location.is_file_path)

        resolved_source_path = location.resolved_source_path
        if not location.is_file_path:
            resolved_source_path = getattr(module, "__file__", resolved_source_path)

        try:
            instance = getattr(module, entrypoint_object_name)
        except AttributeError:
            raise ResolveFromStringError(
                f'"{entrypoint_object_name}" not found in "{location.display_path}"'
            )

        match instance:
            case App():
                return ResolvedEntrypoint(resolved_source_path, instance)
            case candidate if callable(candidate) and not isinstance(candidate, type):
                return ResolvedEntrypoint(resolved_source_path, instance)
            case _:
                raise ResolveFromStringError(
                    f'"{entrypoint_object_name}" is not a valid entrypoint'
                )
