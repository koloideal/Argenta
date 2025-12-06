from typing import Generator

import pytest
from dishka import Container, make_container

from argenta import App, DataBridge, Router
from argenta.di.integration import (
    FromDishka,
    _auto_inject_handlers,
    _get_container_from_response,
    setup_dishka,
)
from argenta.di.providers import SystemProvider
from argenta.orchestrator.argparser import ArgParser, ArgSpace
from argenta.response import ResponseStatus
from argenta.response.entity import Response


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def argparser() -> ArgParser:
    return ArgParser(processed_args=[])


@pytest.fixture
def container(argparser: ArgParser) -> Generator[Container, None, None]:
    container = make_container(SystemProvider(), context={ArgParser: argparser})
    yield container
    container.close()


# ============================================================================
# Tests for container retrieval from response
# ============================================================================


def test_get_container_from_response_extracts_container_from_first_response_arg(container: Container) -> None:
    Response.patch_by_container(container)
    response = Response(ResponseStatus.ALL_FLAGS_VALID)
    assert _get_container_from_response((response,), {}) == container


def test_get_container_from_response_extracts_container_from_second_response_arg(container: Container) -> None:
    Response.patch_by_container(container)
    response = Response(ResponseStatus.ALL_FLAGS_VALID)
    assert _get_container_from_response((object(), response,), {}) == container


def test_get_container_from_response_raises_error_when_container_not_patched() -> None:
    delattr(Response, '__dishka_container__')
    response = Response(ResponseStatus.ALL_FLAGS_VALID)
    with pytest.raises(RuntimeError):
        _get_container_from_response((response,), {})


def test_get_container_from_response_raises_error_when_no_response_in_args(container: Container) -> None:
    Response.patch_by_container(container)
    with pytest.raises(RuntimeError):
        _get_container_from_response((), {})


# ============================================================================
# Tests for dishka setup
# ============================================================================


def test_setup_dishka_with_auto_inject_enabled(container: Container) -> None:
    app = App()
    router = Router()
    
    @router.command('command')
    def handler(_res: Response, data_bridge: FromDishka[DataBridge]) -> None:
        print(data_bridge)
        
    app.include_router(router)
    
    assert setup_dishka(app, container, auto_inject=True) is None


def test_setup_dishka_with_auto_inject_disabled(container: Container) -> None:
    app = App()
    assert setup_dishka(app, container, auto_inject=False) is None


# ============================================================================
# Tests for auto injection
# ============================================================================


def test_auto_inject_handlers_injects_dependencies_into_handlers(container: Container) -> None:
    Response.patch_by_container(container)
    
    app = App()
    router = Router()
    
    @router.command('command')
    def handler(_res: Response, data_bridge: FromDishka[DataBridge]) -> None:
        print(data_bridge)
        
    app.include_router(router)
        
    _auto_inject_handlers(app)
    _auto_inject_handlers(app)  # check idempotency


# ============================================================================
# Tests for container dependency resolution
# ============================================================================F


def test_container_resolves_argspace_dependency(container: Container) -> None:
    assert isinstance(container.get(ArgSpace), ArgSpace)


def test_container_resolves_databridge_dependency(container: Container) -> None:
    assert isinstance(container.get(DataBridge), DataBridge)
