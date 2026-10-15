from collections.abc import Sequence
from dataclasses import dataclass
from itertools import batched

from argenta.app.presentation.ascii_art.entity import FigletFont, Glyph
from argenta.app.presentation.ascii_art.exceptions import InvalidFigletFontException


@dataclass(frozen=True, slots=True)
class FigletHeader:
    hardblank: str
    height: int
    comment_lines: int


class FigletFontParser:
    signature = "flf2a"
    header_fields_count = 6
    first_codepoint = 32
    last_codepoint = 126
    printable_codepoints = range(first_codepoint, last_codepoint + 1)

    def parse(self, source: str) -> FigletFont:
        header_line, *body = source.splitlines() or [""]
        header = self._parse_header(header_line)
        glyphs = self._parse_glyphs(body, header)
        return FigletFont(height=header.height, glyphs=self._drop_undefined_glyphs(glyphs))

    def _parse_header(self, header_line: str) -> FigletHeader:
        header_fields = header_line.split()
        if not header_line.startswith(self.signature):
            raise InvalidFigletFontException("missing 'flf2a' signature")
        if len(header_fields) < self.header_fields_count:
            raise InvalidFigletFontException("malformed header")
        hardblank = header_fields[0].removeprefix(self.signature)
        if len(hardblank) != 1:
            raise InvalidFigletFontException("hardblank must be a single character")
        return FigletHeader(
            hardblank=hardblank,
            height=self._parse_header_number(header_fields[1], minimum=1),
            comment_lines=self._parse_header_number(header_fields[5], minimum=0),
        )

    def _parse_header_number(self, header_field: str, minimum: int) -> int:
        if not header_field.isdecimal() or int(header_field) < minimum:
            raise InvalidFigletFontException(f"invalid header value {header_field!r}")
        return int(header_field)

    def _parse_glyphs(self, body: Sequence[str], header: FigletHeader) -> dict[str, Glyph]:
        first_row = header.comment_lines
        last_row = first_row + header.height * len(self.printable_codepoints)
        if len(body) < last_row:
            raise InvalidFigletFontException("not enough glyph rows for printable ASCII")
        blocks = batched(body[first_row:last_row], header.height)
        return {
            chr(codepoint): self._parse_glyph(chr(codepoint), block, header.hardblank)
            for codepoint, block in zip(self.printable_codepoints, blocks, strict=True)
        }

    def _parse_glyph(self, char: str, rows: Glyph, hardblank: str) -> Glyph:
        *body_rows, last_row = (row.rstrip() for row in rows)
        endmark = last_row[-1:]
        if (
            not endmark
            or not all(row.endswith(endmark) for row in body_rows)
            or not last_row.endswith(endmark * 2)
        ):
            raise InvalidFigletFontException(f"glyph {char!r} has rows without endmarks")
        stripped_rows = [row.removesuffix(endmark) for row in body_rows]
        stripped_rows.append(last_row.removesuffix(endmark * 2))
        without_hardblanks = [row.replace(hardblank, " ") for row in stripped_rows]
        return tuple(without_hardblanks)

    def _drop_undefined_glyphs(self, glyphs: dict[str, Glyph]) -> dict[str, Glyph]:
        return dict(entry for entry in glyphs.items() if self._is_defined(entry))

    def _is_defined(self, entry: tuple[str, Glyph]) -> bool:
        char, glyph = entry
        return char == " " or any(glyph)
