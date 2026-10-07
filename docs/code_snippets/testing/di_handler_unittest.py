import io
from contextlib import redirect_stdout
from typing import ClassVar

from dishka import Provider, Scope, make_container

from argenta import Response, Router
from argenta.command import InputCommand
from argenta.di.integration import FromDishka, setup_dishka


class Service:
    def hello(self) -> str:
        return "world"


def get_service() -> Service:
    return Service()


router = Router(title="DI")


@router.command("HELLO")
def hello(response: Response, service: FromDishka[Service]) -> None:
    print(f"hello {service.hello()}")


class _FakeApp:
    # Minimal stub for setup_dishka; app object is not used in unit tests
    registered_routers: ClassVar[list[Router]] = [router]


def test_hello_uses_service():
    provider = Provider(scope=Scope.APP)
    provider.provide(get_service)

    container = make_container(provider)
    setup_dishka(app=_FakeApp(), container=container, auto_inject=True)

    # Call handler
    with redirect_stdout(io.StringIO()) as stdout:
        router.finds_appropriate_handler(InputCommand.parse("HELLO"))

    assert "hello world" in stdout.getvalue()
