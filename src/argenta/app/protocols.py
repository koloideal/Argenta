from typing import Protocol, TypeVar

T = TypeVar('T', contravariant=True)


class Handler(Protocol[T]):
    def __call__(self, __param: T) -> None:
        raise NotImplementedError
    
class EmptyCommandHandler(Protocol):
    def __call__(self) -> None:
        raise NotImplementedError
        

class Printer(Protocol):
    def __call__(self, __text: str) -> None:
        raise NotImplementedError


class DescriptionMessageGenerator(Protocol):
    def __call__(self, __first_param: str, __second_param: str) -> str:
        raise NotImplementedError
