from typing import Protocol, Any, Callable


class Printer(Protocol):
    def __call__(self, text: str, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()


class WhoNeedsPrinter:
    def __init__(self, print_func: Printer) -> None:
        self.print_func = print_func

def my_printer(text: str, **kwargs) -> None:
    pass

WhoNeedsPrinter(my_printer)
