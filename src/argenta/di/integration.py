__all__ = ["inject", "setup_dishka", "FromDishka"]

from typing import Any, Callable, TypeVar

from dishka import Container, FromDishka
from dishka.integrations.base import is_dishka_injected, wrap_injection

from argenta.app import App
from argenta.response import Response

T = TypeVar("T")


def inject(func: Callable[..., T]) -> Callable[..., T]:
    return wrap_injection(
        func=func,
        is_async=False,
        container_getter=_get_container_from_response,
    )


def setup_dishka(app: App, container: Container, *, auto_inject: bool = False) -> None:
    if auto_inject:
        _auto_inject_handlers(app)
    Response.patch_by_container(container)


def _get_container_from_response(
    args: tuple[Any, ...], kwargs: dict[str, Any]
) -> Container:
    for arg in args:
        if isinstance(arg, Response):
            if hasattr(arg, "_dishka_container"):
                return arg._dishka_container  # pyright: ignore[reportPrivateUsage]
            break
    raise RuntimeError("dishka container not found in Response")


def _auto_inject_handlers(app: App) -> None:
    for router in app.registered_routers:
        for command_handler in router.command_handlers:
            if not is_dishka_injected(command_handler.handler_as_func):
                injected_handler = inject(command_handler.handler_as_func)
                command_handler.handler_as_func = injected_handler
