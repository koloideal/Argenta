import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock

from dishka import Provider, provide, make_container, Scope  # pyright: ignore[reportUnknownVariableType]

from argenta import Router, Command
from argenta.di.integration import inject, setup_dishka, FromDishka
from argenta.response import Response
from argenta.response.status import ResponseStatus


class Service:
    def hello(self) -> str:
        return "world"


router = Router(title="DI")


@router.command(Command("HELLO"))
@inject  # Auto-inject dependencies from the Response container
def hello(response: Response, service: FromDishka[Service]) -> None:
    print(f"hello {service.hello()}")


class TestDIHandler(unittest.TestCase):
    def test_hello_uses_service(self):
        # Prepare DI container with a stub
        fake = Mock(spec=Service)
        fake.hello.return_value = "mocked"

        class TestProvider(Provider):
            scope = Scope.APP

            @provide(scope=Scope.APP)
            def service(self) -> Service:
                return fake

        container = make_container(TestProvider())

        # Bind container to Response via integration
        setup_dishka(app=_FakeApp(), container=container, auto_inject=False)  # type: ignore[arg-type]

        # Create Response bound to the container
        r = Response(ResponseStatus.ALL_FLAGS_VALID)
        r._dishka_container = container  # direct assignment is acceptable in tests  # pyright: ignore[reportPrivateUsage]

        # Call handler directly
        with redirect_stdout(io.StringIO()) as stdout:
            hello(r)

        self.assertIn("hello mocked", stdout.getvalue())


class _FakeApp:
    # Minimal stub for setup_dishka; app object is not used in unit tests
    registered_routers = []
