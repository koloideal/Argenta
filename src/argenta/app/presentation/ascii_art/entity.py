from collections.abc import Mapping
from dataclasses import dataclass

type Glyph = tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FigletFont:
    height: int
    glyphs: Mapping[str, Glyph]
