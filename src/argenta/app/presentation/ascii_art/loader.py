from contextlib import suppress
from enum import StrEnum
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import ClassVar

from argenta.app.presentation.ascii_art.compiler import FigletFontCompiler
from argenta.app.presentation.ascii_art.entity import FigletFont
from argenta.app.presentation.ascii_art.exceptions import (
    InvalidFigletFontException,
    UnreachableFigletFontException,
)
from argenta.app.presentation.ascii_art.parser import FigletFontParser


class BundledFont(StrEnum):
    TARTY1 = "tarty1"
    CHUNKY = "chunky"


def _decode(raw_font: bytes) -> str:
    try:
        return raw_font.decode("utf-8")
    except UnicodeDecodeError:
        return raw_font.decode("latin-1")


def _bundled_resource(font: BundledFont, suffix: str) -> Traversable:
    return files(__name__).joinpath("_fonts", f"{font}{suffix}")


def _read_source(font_path: Path) -> tuple[bytes, int]:
    try:
        return font_path.read_bytes(), font_path.stat().st_mtime_ns
    except OSError as error:
        raise UnreachableFigletFontException(font_path) from error


def _parse_source(parser: FigletFontParser, font_path: Path) -> tuple[FigletFont, int]:
    raw_font, mtime_ns = _read_source(font_path)
    return parser.parse(_decode(raw_font)), mtime_ns


class FigletFontLoader:
    compiled_suffix = ".flfd"
    _bundled_fonts: ClassVar[dict[BundledFont, FigletFont]] = {}

    def __init__(
        self,
        parser: FigletFontParser | None = None,
        compiler: FigletFontCompiler | None = None,
    ) -> None:
        self._parser: FigletFontParser = parser or FigletFontParser()
        self._compiler: FigletFontCompiler = compiler or FigletFontCompiler()

    def load(self, path: Path | str) -> FigletFont:
        font_path = Path(path)
        if font_path.suffix == self.compiled_suffix:
            return self._load_compiled(font_path)
        dump_path = font_path.with_suffix(self.compiled_suffix)
        if font_path.is_file():
            return self._load_source(font_path, dump_path)
        if dump_path.is_file():
            return self._load_compiled(dump_path)
        raise UnreachableFigletFontException(font_path)

    def compile(self, source_path: Path | str, target_path: Path | str | None = None) -> Path:
        source = Path(source_path)
        target = Path(target_path) if target_path else source.with_suffix(self.compiled_suffix)
        font, mtime_ns = _parse_source(self._parser, source)
        try:
            target.write_bytes(self._compiler.dump(font, mtime_ns))
        except OSError as error:
            raise UnreachableFigletFontException(target) from error
        return target

    def load_bundled(self, font: BundledFont) -> FigletFont:
        if font not in self._bundled_fonts:
            try:
                loaded = self._compiler.load(
                    _bundled_resource(font, self.compiled_suffix).read_bytes()
                )
            except (InvalidFigletFontException, OSError):
                loaded = self._parser.parse(_decode(_bundled_resource(font, ".flf").read_bytes()))
            self._bundled_fonts[font] = loaded
        return self._bundled_fonts[font]

    def _load_source(self, font_path: Path, dump_path: Path) -> FigletFont:
        raw_font, mtime_ns = _read_source(font_path)
        if dump_path.is_file():
            cached = self._try_load_compiled(dump_path, mtime_ns)
            if cached is not None:
                return cached
        font = self._parser.parse(_decode(raw_font))
        with suppress(OSError):
            dump_path.write_bytes(self._compiler.dump(font, mtime_ns))
        return font

    def _load_compiled(self, dump_path: Path) -> FigletFont:
        try:
            raw_dump = dump_path.read_bytes()
        except OSError as error:
            raise UnreachableFigletFontException(dump_path) from error
        return self._compiler.load(raw_dump)

    def _try_load_compiled(self, dump_path: Path, mtime_ns: int) -> FigletFont | None:
        try:
            return self._compiler.load(dump_path.read_bytes(), expected_mtime_ns=mtime_ns)
        except (InvalidFigletFontException, OSError):
            return None
