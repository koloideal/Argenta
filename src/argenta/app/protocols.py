__all__ = [
    "NonStandardBehaviorHandler",
    "EmptyCommandHandler",
    "MostSimilarCommandGetter",
    "Printer",
    "DescriptionMessageGenerator",
    "HandlerFunc",
]

from typing import Any, Protocol, TypeVar, Callable


T = TypeVar("T", contravariant=True)


class NonStandardBehaviorHandler(Protocol[T]):
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
