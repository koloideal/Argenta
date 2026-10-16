import json
import os
import re
from hashlib import sha256
from pathlib import Path
from typing import cast
from urllib.parse import quote
from urllib.request import urlopen

from argenta.app.presentation.ascii_art.exceptions import (
    FigletFontException,
    FigletFontFetchException,
    InvalidFigletFontException,
    UnreachableFigletFontException,
)
from argenta.app.presentation.ascii_art.loader import FigletFontLoader

FONT_SOURCES = (
    "https://raw.githubusercontent.com/cmatsuoka/figlet/master/fonts/{name}.flf",
    "https://raw.githubusercontent.com/xero/figlet-fonts/main/{name}.flf",
)
INDEX_SOURCES = (
    "https://api.github.com/repos/cmatsuoka/figlet/git/trees/master?recursive=1",
    "https://api.github.com/repos/xero/figlet-fonts/git/trees/main?recursive=1",
)
FONT_NAME_PATTERN = re.compile(r"[A-Za-z0-9 ._()-]{1,64}")
_CACHE_HASH_LENGTH = 16


def _try_open(url: str, timeout: float) -> bytes | None:
    try:
        with urlopen(url, timeout=timeout) as response:
            return cast("bytes", response.read())
    except OSError:
        return None


def _fetch_font_names(url: str, timeout: float) -> list[str] | None:
    raw_index = _try_open(url, timeout)
    if raw_index is None:
        return None
    try:
        tree = cast("list[dict[str, object]]", json.loads(raw_index)["tree"])
    except (ValueError, KeyError, TypeError):
        return None
    names: list[str] = []
    for entry in tree:
        path = str(entry["path"])
        if path.endswith(".flf"):
            names.append(Path(path).stem)
    return names


def _default_cache_dir() -> Path:
    base = os.environ.get("XDG_CACHE_HOME")
    root = Path(base) if base else Path.home() / ".cache"
    return root / "argenta" / "fonts"


def _candidate_urls(font: str) -> list[str]:
    if font.startswith(("https://", "http://")):
        return [font]
    if ".." in font or FONT_NAME_PATTERN.fullmatch(font) is None:
        raise InvalidFigletFontException(f"invalid font name {font!r}")
    names = dict.fromkeys((font, font.capitalize()))
    return [source.format(name=quote(name)) for source in FONT_SOURCES for name in names]


def _filename_for(font: str) -> str:
    if font.startswith(("https://", "http://")):
        return font.rpartition("/")[-1]
    return f"{font}.flf"


def _store_font(path: Path, font_bytes: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(font_bytes)


class FigletFontFetcher:
    sources = FONT_SOURCES
    index_sources = INDEX_SOURCES
    timeout = 10.0
    font_name_pattern = FONT_NAME_PATTERN

    def __init__(
        self,
        loader: FigletFontLoader | None = None,
        cache_dir: Path | str | None = None,
        use_cache: bool = True,
    ) -> None:
        self._loader: FigletFontLoader = loader or FigletFontLoader()
        self._cache_dir = _default_cache_dir() if cache_dir is None else Path(cache_dir)
        self._use_cache = use_cache

    def fetch(self, font: str, target_dir: Path | str = ".") -> Path:
        raw_font = self._obtain(font)
        target = Path(target_dir) / _filename_for(font)
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

    def fetch_cached(self, font: str) -> Path:
        cached = self._cache_path(font)
        if cached.is_file():
            return cached
        raw_font = self._download(font)
        try:
            _store_font(cached, raw_font)
        except OSError as error:
            raise UnreachableFigletFontException(cached) from error
        try:
            self._loader.load(cached)
        except FigletFontException:
            cached.unlink(missing_ok=True)
            raise
        return cached

    def list_available(self) -> list[str]:
        names: dict[str, str] = {}
        for url in self.index_sources:
            fetched = _fetch_font_names(url, self.timeout)
            if fetched is not None:
                names.update({name.lower(): name for name in fetched})
        if not names:
            raise FigletFontFetchException("remote font index")
        return sorted(names.values(), key=str.lower)

    def _obtain(self, font: str) -> bytes:
        if self._use_cache:
            cached = self.fetch_cached(font)
            try:
                return cached.read_bytes()
            except OSError as error:
                raise UnreachableFigletFontException(cached) from error
        return self._download(font)

    def _download(self, font: str) -> bytes:
        for url in _candidate_urls(font):
            raw_font = _try_open(url, self.timeout)
            if raw_font is not None:
                return raw_font
        raise FigletFontFetchException(font)

    def _cache_path(self, font: str) -> Path:
        digest = sha256(font.encode("utf-8")).hexdigest()[:_CACHE_HASH_LENGTH]
        return self._cache_dir / f"{digest}-{_filename_for(font)}"
