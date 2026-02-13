__all__ = ["run_handler"]

import importlib
import os
import sys
from pathlib import Path
from typing import Any


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
        raise ImportFromStringError(f'Could not import module "{module_str}".') from exc

    instance = module
    try:
        for attr_str in attrs_str.split("."):
            instance = getattr(instance, attr_str)
    except AttributeError:
        raise ImportFromStringError(f'Attribute "{attrs_str}" not found in module "{module_str}".')

    return instance


def run_handler(entry_point: str) -> None:
    os.environ["RUN_AS_ARGENTA_APPLICATION"] = "1"

    if str(Path.cwd()) not in sys.path:
        sys.path.insert(0, str(Path.cwd()))

    runner = import_from_string(entry_point)

    if not callable(runner):
        raise TypeError(f'"{entry_point}" is not callable')

    runner()
