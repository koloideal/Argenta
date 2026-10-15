from collections.abc import Iterable
from pathlib import Path
from typing import override


class FigletFontException(Exception):
    __slots__ = ()


class UnreachableFigletFontException(FigletFontException):
    @override
    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__()

    @override
    def __str__(self) -> str:
        return f"FIGlet font file is unreachable: {self.path}"


class InvalidFigletFontException(FigletFontException):
    @override
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__()

    @override
    def __str__(self) -> str:
        return f"Invalid FIGlet font: {self.reason}"


class MissingGlyphsException(FigletFontException):
    @override
    def __init__(self, missing_chars: Iterable[str]) -> None:
        self.missing_chars = frozenset(missing_chars)
        super().__init__()

    @override
    def __str__(self) -> str:
        listed_chars = ", ".join(repr(char) for char in sorted(self.missing_chars))
        return f"FIGlet font has no glyphs for: {listed_chars}"
