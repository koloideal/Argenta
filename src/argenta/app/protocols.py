__all__ = [
    "DescriptionMessageGenerator",
    "EmptyCommandHandler",
    "HandlerFunc",
    "MostSimilarCommandGetter",
    "NonStandardBehaviorHandler",
    "Printer",
]

from collections.abc import Callable
from typing import Any, Protocol


class NonStandardBehaviorHandler[T](Protocol):
    def __call__(self, _param: T, /) -> None:
        raise NotImplementedError


class EmptyCommandHandler(Protocol):
    def __call__(self) -> None:
        raise NotImplementedError


class Printer(Protocol):
    def __call__(self, _text: str, /) -> None:
        raise NotImplementedError


class MostSimilarCommandGetter(Protocol):
    def __call__(self, _unknown_trigger: str, /) -> str | None:
        raise NotImplementedError


class DescriptionMessageGenerator(Protocol):
    def __call__(self, _command: str, _description: str, /) -> str:
        raise NotImplementedError


type HandlerFunc = Callable[..., Any]
