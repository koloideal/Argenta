__all__ = ["run_handler"]

import importlib
from typing import Any

from argenta import App, Orchestrator


class ImportFromStringError(Exception):
    pass


def import_from_string(import_str: str) -> Any:
    module_str, _, attrs_str = import_str.partition(":")
    if not module_str or not attrs_str:
        raise ImportFromStringError(
            f'Import string "{import_str}" must be in format "<module>:<attribute>".'
        )

    try:
        module = importlib.import_module(module_str)
    except ModuleNotFoundError as exc:
        if exc.name != module_str:
            raise exc from None
        raise ImportFromStringError(f'Could not import module "{module_str}".')

    instance = module
    try:
        for attr_str in attrs_str.split("."):
            instance = getattr(instance, attr_str)
    except AttributeError:
        raise ImportFromStringError(f'Attribute "{attrs_str}" not found in module "{module_str}".')

    return instance


def run_handler(orchestrator_str: str, app_str: str | None = None) -> Any:
    orchestrator = import_from_string(orchestrator_str)

    if not isinstance(orchestrator, Orchestrator):
        raise TypeError(f"Not an Orchestrator: {type(orchestrator).__name__}")

    if app_str is not None:
        app = import_from_string(app_str)
    else:
        module_str = orchestrator_str.partition(":")[0]
        module = importlib.import_module(module_str)

        app = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, App):
                app = attr
                break

        if app is None:
            raise ValueError(f'No App instance found in module "{module_str}"')

    if not isinstance(app, App):
        raise TypeError(f"Not an App: {type(app).__name__}")

    return orchestrator.start_polling(app)
