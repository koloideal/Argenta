from functools import lru_cache

from rich.console import Console
from rich.text import Text

_RENDERABLE_CACHE_SIZE = 256


@lru_cache(maxsize=_RENDERABLE_CACHE_SIZE)
def _renderable(text: str) -> Text:
    """
    Private. Parses a markup string into a Rich Text once per unique string
    :param text: markup string to parse
    :return: parsed Text renderable
    """
    return Text.from_markup(text)


class DefaultPrinter:
    """
    Private. Default system messages printer.
    Prints via a Rich console with auto-highlighting disabled and reuses
    parsed Text renderables so repeated identical prints (for example, the
    command groups block in repeat mode) skip markup parsing
    """

    def __init__(self) -> None:
        self._console = Console(highlight=False)

    def __call__(self, text: str, /) -> None:
        self._console.print(_renderable(text))
