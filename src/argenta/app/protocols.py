from typing import Protocol, TypeVar, overload, Any, Never

T = TypeVar('T', contravariant=True)
_default: Any = object()


class Handler(Protocol[T]):
    @overload
    def __call__(self: "Handler[Never]") -> None: ...
    
    @overload
    def __call__(self, __param: T) -> None: ...
        
    def __call__(self, __param: T = _default) -> None:
        raise NotImplementedError
        

class Printer(Protocol):
    def __call__(self, __text: str) -> None:
        raise NotImplementedError


class DescriptionMessageGenerator(Protocol):
    def __call__(self, __first_param: str, __second_param: str) -> str:
        raise NotImplementedError
