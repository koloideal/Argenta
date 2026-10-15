from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from typing import override

from argenta.app.presentation.ascii_art.exceptions import InvalidFigletFontException

type Glyph = tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FigletFont:
    height: int
    glyphs: Mapping[str, Glyph]


class LazyGlyphs(Mapping[str, Glyph]):
    __slots__ = ("_blob", "_cache", "_chars", "_height", "_lines")

    def __init__(self, chars: str, blob: str, height: int) -> None:
        if blob.count("\n") + 1 != len(chars) * height:
            raise InvalidFigletFontException("compiled font dump has mismatched glyph table")
        self._chars = chars
        self._blob = blob
        self._height = height
        self._cache: dict[str, Glyph] = {}
        self._lines: list[str] | None = None

    @override
    def __getitem__(self, char: str) -> Glyph:
        if char not in self._cache:
            index = self._chars.find(char)
            if index == -1:
                raise KeyError(char)
            start = index * self._height
            stop = start + self._height
            self._cache[char] = tuple(self._materialized_lines()[start:stop])
        return self._cache[char]

    @override
    def __len__(self) -> int:
        return len(self._chars)

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._chars)

    @override
    def __contains__(self, char: object) -> bool:
        return isinstance(char, str) and char in self._chars

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Mapping) and dict(self) == dict(other)

    def _materialized_lines(self) -> list[str]:
        if self._lines is None:
            self._lines = self._blob.split("\n")
        return self._lines
