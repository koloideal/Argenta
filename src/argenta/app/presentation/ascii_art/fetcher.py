import json
import re
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import cast
from urllib.request import urlopen

from argenta.app.presentation.ascii_art.exceptions import (
    FigletFontException,
    FigletFontFetchException,
    InvalidFigletFontException,
    UnreachableFigletFontException,
)
from argenta.app.presentation.ascii_art.loader import FigletFontLoader


def _try_open(url: str, timeout: float) -> bytes | None:
    try:
        with urlopen(url, timeout=timeout) as response:
            return cast("bytes", response.read())
    except OSError:
        return None


def _fetch_index(url: str, timeout: float) -> list[dict[str, object]] | None:
    raw_index = _try_open(url, timeout)
    if raw_index is None:
        return None
    try:
        return cast("list[dict[str, object]]", json.loads(raw_index)["tree"])
    except (ValueError, KeyError, TypeError):
        return None


def _font_names(tree: Iterable[dict[str, object]]) -> Iterator[str]:
    for entry in tree:
        path = str(entry["path"])
        if path.endswith(".flf"):
            yield Path(path).stem


class FigletFontFetcher:
    sources = (
        "https://raw.githubusercontent.com/cmatsuoka/figlet/master/fonts/{name}.flf",
        "https://raw.githubusercontent.com/xero/figlet-fonts/main/{name}.flf",
    )
    index_sources = (
        "https://api.github.com/repos/cmatsuoka/figlet/git/trees/master?recursive=1",
        "https://api.github.com/repos/xero/figlet-fonts/git/trees/main?recursive=1",
    )
    timeout = 10.0
    font_name_pattern = re.compile(r"[A-Za-z0-9 ._()-]{1,64}")

    def __init__(self, loader: FigletFontLoader | None = None) -> None:
        self._loader: FigletFontLoader = loader or FigletFontLoader()

    def fetch(self, font: str, target_dir: Path | str = ".") -> Path:
        raw_font = self._download(font)
        target = Path(target_dir) / self._filename_for(font)
        try:
            target.write_bytes(raw_font)
        except OSError as error:
            raise UnreachableFigletFontException(target) from error
        try:
            self._loader.load(target)
        except FigletFontException:
            target.unlink(missing_ok=True)
            raise
        return target

    def list_available(self) -> list[str]:
        names: dict[str, str] = {}
        for url in self.index_sources:
            tree = _fetch_index(url, self.timeout)
            if tree is not None:
                names.update({name.lower(): name for name in _font_names(tree)})
        if not names:
            raise FigletFontFetchException("remote font index")
        return sorted(names.values(), key=str.lower)

    def _download(self, font: str) -> bytes:
        for url in self._candidate_urls(font):
            raw_font = _try_open(url, self.timeout)
            if raw_font is not None:
                return raw_font
        raise FigletFontFetchException(font)

    def _candidate_urls(self, font: str) -> list[str]:
        if font.startswith(("https://", "http://")):
            return [font]
        if ".." in font or not self.font_name_pattern.fullmatch(font):
            raise InvalidFigletFontException(f"invalid font name {font!r}")
        names = dict.fromkeys((font, font.capitalize()))
        return [source.format(name=name) for source in self.sources for name in names]

    def _filename_for(self, font: str) -> str:
        if font.startswith(("https://", "http://")):
            return font.rpartition("/")[-1]
        return f"{font}.flf"
