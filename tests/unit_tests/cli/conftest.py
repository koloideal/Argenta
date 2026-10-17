import importlib
import os
from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _clean_state() -> Iterator[None]:
    yield
    os.environ.pop("RUN_FROM_ARGENTA_RUNNER", None)
    os.environ.pop("ARGENTA_RUN_MODE", None)
    os.environ.pop("ARGENTA_A2UI_TRANSPORT", None)
    os.environ.pop("ARGENTA_A2UI_WS_PORT", None)


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
