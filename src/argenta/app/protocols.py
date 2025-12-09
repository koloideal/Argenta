__all__ = ["NonStandardBehaviorHandler", "EmptyCommandHandler", "Printer", "DescriptionMessageGenerator"]

from typing import Protocol, TypeVar

T = TypeVar("T", contravariant=True)  # noqa: WPS111


class NonStandardBehaviorHandler(Protocol[T]):
    def __call__(self, _param: T, /) -> None:
        raise NotImplementedError


class EmptyCommandHandler(Protocol):
    def __call__(self) -> None:
        raise NotImplementedError


class Printer(Protocol):
    def __call__(self, _text: str, /) -> None:
        raise NotImplementedError


class DescriptionMessageGenerator(Protocol):
    def __call__(self, _command: str, _description: str, /) -> str:
        raise NotImplementedError
