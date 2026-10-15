import marshal
from typing import cast

from argenta.app.presentation.ascii_art.entity import FigletFont, LazyGlyphs
from argenta.app.presentation.ascii_art.exceptions import InvalidFigletFontException

_MARSHAL_ERRORS: tuple[type[Exception], ...] = (
    ValueError,
    TypeError,
    EOFError,
    OverflowError,
    RecursionError,
)


def _unmarshal(payload: bytes) -> tuple[int, int, str, str]:
    try:
        return cast("tuple[int, int, str, str]", marshal.loads(payload))
    except _MARSHAL_ERRORS as error:
        raise InvalidFigletFontException("corrupted compiled font dump") from error


class FigletFontCompiler:
    magic = b"FLFD"
    version = 1
    header = magic + bytes((version,))

    def dump(self, font: FigletFont, source_mtime_ns: int) -> bytes:
        chars = "".join(font.glyphs)
        blob = "\n".join(row for glyph in font.glyphs.values() for row in glyph)
        payload = (source_mtime_ns, font.height, chars, blob)
        return self.header + marshal.dumps(payload)

    def load(self, raw_dump: bytes, expected_mtime_ns: int | None = None) -> FigletFont:
        if not raw_dump.startswith(self.header):
            raise InvalidFigletFontException("unrecognized compiled font format")
        payload = _unmarshal(raw_dump.removeprefix(self.header))
        return self._build_font(payload, expected_mtime_ns)

    def _build_font(
        self, payload: tuple[int, int, str, str], expected_mtime_ns: int | None
    ) -> FigletFont:
        mtime_ns, height, chars, blob = payload
        if expected_mtime_ns is not None and mtime_ns != expected_mtime_ns:
            raise InvalidFigletFontException("compiled font dump is outdated")
        return FigletFont(height=height, glyphs=LazyGlyphs(chars, blob, height))
