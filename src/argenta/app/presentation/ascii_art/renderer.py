from argenta.app.presentation.ascii_art.entity import FigletFont
from argenta.app.presentation.ascii_art.exceptions import MissingGlyphsException


class AsciiArtRenderer:
    def render(self, text: str, font: FigletFont) -> str:
        self._ensure_glyphs_exist(text, font)
        rendered_lines = [self._render_line(line, font) for line in text.split("\n")]
        *leading_lines, last_line = rendered_lines
        return "".join(map(self._terminate_line, leading_lines)) + last_line

    def _ensure_glyphs_exist(self, text: str, font: FigletFont) -> None:
        missing_chars = set(text.replace("\n", "")).difference(font.glyphs)
        if missing_chars:
            raise MissingGlyphsException(missing_chars)

    def _render_line(self, line: str, font: FigletFont) -> str:
        rows = zip(*(font.glyphs[char] for char in line), strict=True)
        return "\n".join(map("".join, rows))

    def _terminate_line(self, rendered_line: str) -> str:
        return rendered_line if rendered_line.endswith("\n") else f"{rendered_line}\n"
