import importlib
import os
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _clean_state() -> Iterator[None]:
    modules_before = set(sys.modules)
    path_before = list(sys.path)
    yield
    for name in set(sys.modules) - modules_before:
        sys.modules.pop(name, None)
    sys.path[:] = path_before
    os.environ.pop("RUN_FROM_ARGENTA_RUNNER", None)


def _write_module(tmp_path: Path, name: str, body: str) -> Path:
    path = tmp_path / f"{name}.py"
    path.write_text(body)
    importlib.invalidate_caches()
    return path


_APP_MODULE = """
from argenta import App, Router
from argenta.command import Command, Flag

router = Router("Test router")

@router.command(Command("mycmd", aliases=["mc"], flags=Flag("verbose")))
def mycmd_handler(response):
    pass

@router.command(Command("bare", description=""))
def bare_handler(response):
    pass

application = App()
application.include_router(router)

def create_app():
    app = App()
    app.include_router(router)
    return app
"""
