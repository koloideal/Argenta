__all__ = ["NonStandardBehaviorHandler", "EmptyCommandHandler", "Printer", "DescriptionMessageGenerator", "HandlerFunc"]

from typing import ParamSpec, Protocol, TypeVar
from argenta.response import Response

T = TypeVar("T", contravariant=True) 
P = ParamSpec("P")


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


class HandlerFunc(Protocol):
    def __call__(self, response: Response) -> None:
        raise NotImplementedError
