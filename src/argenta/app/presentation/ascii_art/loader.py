from enum import StrEnum
from importlib.resources import files
from pathlib import Path

from argenta.app.presentation.ascii_art.entity import FigletFont
from argenta.app.presentation.ascii_art.exceptions import UnreachableFigletFontException
from argenta.app.presentation.ascii_art.parser import FigletFontParser


class BundledFont(StrEnum):
    TARTY1 = "tarty1"
    CHUNKY = "chunky"


class FigletFontLoader:
    def __init__(self, parser: FigletFontParser | None = None) -> None:
        self._parser: FigletFontParser = parser or FigletFontParser()

    def load(self, path: Path | str) -> FigletFont:
        font_path = Path(path)
        try:
            raw_font = font_path.read_bytes()
        except OSError as error:
            raise UnreachableFigletFontException(font_path) from error
        return self._parser.parse(self._decode(raw_font))

    def load_bundled(self, font: BundledFont) -> FigletFont:
        resource = files(__name__).joinpath("_fonts", f"{font}.flf")
        return self._parser.parse(self._decode(resource.read_bytes()))

    def _decode(self, raw_font: bytes) -> str:
        try:
            return raw_font.decode("utf-8")
        except UnicodeDecodeError:
            return raw_font.decode("latin-1")
