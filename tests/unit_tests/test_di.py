from typing import Generator
from argenta import App, DataBridge, Router
from argenta.di.providers import SystemProvider
from argenta.orchestrator.argparser import ArgParser, ArgSpace
from argenta.response import ResponseStatus
from dishka import Container, make_container
import pytest
from argenta.response.entity import Response
from argenta.di.integration import FromDishka, _get_container_from_response, setup_dishka, _auto_inject_handlers


@pytest.fixture
def argparser() -> ArgParser:
    return ArgParser(processed_args=[])

@pytest.fixture
def container(argparser: ArgParser) -> Generator[Container]:
    container = make_container(SystemProvider(), context={ArgParser: argparser})
    yield container
    container.close()


def test_get_container_from_response(container: Container):
    Response.patch_by_container(container)
    response = Response(ResponseStatus.ALL_FLAGS_VALID)
    assert _get_container_from_response((response,), {}) == container
    
def test_get_container_from_response4(container: Container):
    Response.patch_by_container(container)
    response = Response(ResponseStatus.ALL_FLAGS_VALID)
    assert _get_container_from_response((object(), response,), {}) == container
    
def test_get_container_from_response2(container: Container):
    delattr(Response, '__dishka_container__')
    response = Response(ResponseStatus.ALL_FLAGS_VALID)
    with pytest.raises(RuntimeError):
        _get_container_from_response((response,), {})
        
def test_get_container_from_response3(container: Container):
    Response.patch_by_container(container)
    with pytest.raises(RuntimeError):
        assert _get_container_from_response((), {}) == container
        
def test_setup_dishka(container: Container):
    app = App()
    router = Router()
    
    @router.command('command')
    def handler(res: Response, data_bridge: FromDishka[DataBridge]):
        print(data_bridge)
        
    app.include_router(router)
    
    assert setup_dishka(app, container, auto_inject=True) is None
    
def test_setup_dishka2(container: Container):
    app = App()
    assert setup_dishka(app, container, auto_inject=False) is None
    
def test_auto_inject_handlers(container: Container):
    Response.patch_by_container(container)
    
    app = App()
    router = Router()
    
    @router.command('command')
    def handler(res: Response, data_bridge: FromDishka[DataBridge]):
        print(data_bridge)
        
    app.include_router(router)
        
    _auto_inject_handlers(app)
    _auto_inject_handlers(app) # check idempotency
    
def test_get_from_container(container: Container):
    assert isinstance(container.get(ArgSpace), ArgSpace)
    
def test_get_from_container2(container: Container):
    assert isinstance(container.get(DataBridge), DataBridge)
    
    