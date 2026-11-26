import marshal
import os
from collections.abc import Mapping
from importlib.resources import files
from pathlib import Path
from typing import Self

import pytest
from pytest_mock import MockerFixture

from argenta.app import App
from argenta.app.presentation.ascii_art import (
    AsciiArtRenderer,
    BundledFont,
    FigletFont,
    FigletFontException,
    FigletFontFetcher,
    FigletFontFetchException,
    FigletFontLoader,
    FigletFontParser,
    InvalidFigletFontException,
    MissingGlyphsException,
    UnreachableFigletFontException,
)
from argenta.app.presentation.ascii_art.compiler import FigletFontCompiler

PRINTABLE_ASCII = [chr(codepoint) for codepoint in range(32, 127)]


def build_flf(
    height: int = 2,
    comments: tuple[str, ...] = (),
    hardblank: str = "$",
    undefined: str = "",
) -> str:
    header = f"flf2a{hardblank} {height} {height} 10 0 {len(comments)}"
    glyph_rows: list[str] = []
    for char in PRINTABLE_ASCII:
        rows = ["" if char in undefined else f"{char}{hardblank}{index}" for index in range(height)]
        glyph_rows.extend(f"{row}@" for row in rows[:-1])
        glyph_rows.append(f"{rows[-1]}@@")
    return "\n".join([header, *comments, *glyph_rows]) + "\n"


class TestFigletFontParser:
    def test_parses_all_printable_ascii_glyphs(self) -> None:
        font = FigletFontParser().parse(build_flf())
        assert font.height == 2
        assert set(font.glyphs) == set(PRINTABLE_ASCII)

    def test_strips_endmarks_and_replaces_hardblank(self) -> None:
        font = FigletFontParser().parse(build_flf())
        assert font.glyphs["A"] == ("A 0", "A 1")

    def test_skips_comment_lines(self) -> None:
        font = FigletFontParser().parse(build_flf(comments=("first comment", "second comment")))
        assert font.glyphs[" "] == ("  0", "  1")

    def test_rejects_missing_signature(self) -> None:
        with pytest.raises(InvalidFigletFontException, match="signature"):
            FigletFontParser().parse("not a font")

    @pytest.mark.parametrize(
        "header",
        ["flf2a$ x 2 10 0 0", "flf2a$ 0 2 10 0 0", "flf2a$ 2 2 10 0 -1"],
        ids=["non-numeric-height", "zero-height", "negative-comments"],
    )
    def test_rejects_invalid_header_values(self, header: str) -> None:
        source = "\n".join([header, *build_flf().splitlines()[1:]])
        with pytest.raises(InvalidFigletFontException, match="invalid header value"):
            FigletFontParser().parse(source)

    def test_rejects_multi_character_hardblank(self) -> None:
        source = build_flf().replace("flf2a$", "flf2a$$", 1)
        with pytest.raises(InvalidFigletFontException, match="hardblank"):
            FigletFontParser().parse(source)

    def test_rejects_glyph_rows_without_endmarks(self) -> None:
        source = build_flf().replace("A$1@@", "A$1", 1)
        with pytest.raises(InvalidFigletFontException, match="glyph 'A'"):
            FigletFontParser().parse(source)

    def test_drops_undefined_glyphs_but_keeps_space(self) -> None:
        font = FigletFontParser().parse(build_flf(undefined=" }"))
        assert "}" not in font.glyphs
        assert font.glyphs[" "] == ("", "")

    def test_rejects_malformed_header(self) -> None:
        with pytest.raises(InvalidFigletFontException, match="malformed header"):
            FigletFontParser().parse("flf2a$ 2 2")

    def test_rejects_empty_source(self) -> None:
        with pytest.raises(InvalidFigletFontException):
            FigletFontParser().parse("")

    def test_rejects_truncated_glyph_table(self) -> None:
        truncated = "\n".join(build_flf().splitlines()[:10])
        with pytest.raises(InvalidFigletFontException, match="not enough glyph rows"):
            FigletFontParser().parse(truncated)


class TestFigletFontLoader:
    def test_loads_user_font_from_path(self, tmp_path: Path) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(height=3), encoding="utf-8")
        assert FigletFontLoader().load(font_path).height == 3

    def test_accepts_string_path(self, tmp_path: Path) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(), encoding="utf-8")
        assert FigletFontLoader().load(str(font_path)).height == 2

    def test_falls_back_to_latin1_encoding(self, tmp_path: Path) -> None:
        font_path = tmp_path / "latin1.flf"
        font_path.write_text(build_flf(comments=("caf\u00e9",)), encoding="latin-1")
        assert FigletFontLoader().load(font_path).height == 2

    def test_rejects_missing_file(self, tmp_path: Path) -> None:
        missing_path = tmp_path / "missing.flf"
        with pytest.raises(UnreachableFigletFontException, match=r"missing\.flf") as error:
            FigletFontLoader().load(missing_path)
        assert error.value.path == missing_path

    def test_rejects_directory(self, tmp_path: Path) -> None:
        with pytest.raises(UnreachableFigletFontException):
            FigletFontLoader().load(tmp_path)

    @pytest.mark.parametrize("bundled_font", list(BundledFont))
    def test_loads_every_bundled_font(self, bundled_font: BundledFont) -> None:
        font = FigletFontLoader().load_bundled(bundled_font)
        assert set("Argenta See you 0123456789").issubset(font.glyphs)

    def test_compiles_dump_next_to_source(self, tmp_path: Path) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(), encoding="utf-8")
        FigletFontLoader().load(font_path)
        assert font_path.with_suffix(".flfd").is_file()

    def test_reuses_existing_dump(self, tmp_path: Path) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(), encoding="utf-8")
        original = FigletFontLoader().load(font_path)
        recorded_mtime = font_path.stat().st_mtime_ns
        font_path.write_text(build_flf(height=9), encoding="utf-8")
        os.utime(font_path, ns=(recorded_mtime, recorded_mtime))
        assert FigletFontLoader().load(font_path).glyphs == original.glyphs

    def test_recompiles_outdated_dump(self, tmp_path: Path) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(), encoding="utf-8")
        FigletFontLoader().load(font_path)
        recorded_mtime = font_path.stat().st_mtime_ns
        font_path.write_text(build_flf(height=9), encoding="utf-8")
        # Advance the source timestamp even when both writes share a filesystem clock tick.
        updated_mtime = recorded_mtime + 1_000_000_000
        os.utime(font_path, ns=(updated_mtime, updated_mtime))
        assert FigletFontLoader().load(font_path).height == 9

    def test_recovers_from_corrupted_dump(self, tmp_path: Path) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(height=4), encoding="utf-8")
        font_path.with_suffix(".flfd").write_bytes(b"garbage")
        assert FigletFontLoader().load(font_path).height == 4
        assert FigletFontLoader().load(font_path.with_suffix(".flfd")).height == 4

    def test_recovers_from_unreadable_dump(self, tmp_path: Path, mocker: MockerFixture) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(), encoding="utf-8")
        font_path.with_suffix(".flfd").write_bytes(b"")
        original_read_bytes = Path.read_bytes

        def flaky_read_bytes(self: Path) -> bytes:
            if self.suffix == ".flfd":
                raise OSError("denied")
            return original_read_bytes(self)

        mocker.patch.object(Path, "read_bytes", flaky_read_bytes)
        assert FigletFontLoader().load(font_path).height == 2

    def test_loads_dump_when_source_is_missing(self, tmp_path: Path) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(height=5), encoding="utf-8")
        FigletFontLoader().load(font_path)
        font_path.unlink()
        assert FigletFontLoader().load(font_path).height == 5

    def test_loads_dump_by_direct_path(self, tmp_path: Path) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(height=6), encoding="utf-8")
        FigletFontLoader().load(font_path)
        assert FigletFontLoader().load(font_path.with_suffix(".flfd")).height == 6

    def test_rejects_malformed_dump_path(self, tmp_path: Path) -> None:
        dump_path = tmp_path / "custom.flfd"
        dump_path.write_bytes(b"not a dump")
        with pytest.raises(InvalidFigletFontException, match="compiled font format"):
            FigletFontLoader().load(dump_path)

    def test_rejects_corrupted_dump_payload(self, tmp_path: Path) -> None:
        dump_path = tmp_path / "custom.flfd"
        dump_path.write_bytes(b"FLFD\x01not-marshal")
        with pytest.raises(InvalidFigletFontException, match="corrupted"):
            FigletFontLoader().load(dump_path)

    def test_rejects_missing_dump_path(self, tmp_path: Path) -> None:
        with pytest.raises(UnreachableFigletFontException):
            FigletFontLoader().load(tmp_path / "missing.flfd")

    def test_survives_unwritable_dump_location(self, tmp_path: Path, mocker: MockerFixture) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(), encoding="utf-8")

        def denied_write_bytes(self: Path, _data: bytes) -> int:
            raise OSError("denied")

        mocker.patch.object(Path, "write_bytes", denied_write_bytes)
        assert FigletFontLoader().load(font_path).height == 2

    def test_compile_writes_dump(self, tmp_path: Path) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(height=7), encoding="utf-8")
        target = FigletFontLoader().compile(font_path)
        assert target == font_path.with_suffix(".flfd")
        assert FigletFontLoader().load(target).height == 7

    def test_compile_writes_to_explicit_target(self, tmp_path: Path) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(height=3), encoding="utf-8")
        target = tmp_path / "out" / "dump.flfd"
        target.parent.mkdir()
        assert FigletFontLoader().compile(font_path, target) == target
        assert FigletFontLoader().load(target).height == 3

    def test_compile_rejects_missing_source(self, tmp_path: Path) -> None:
        with pytest.raises(UnreachableFigletFontException):
            FigletFontLoader().compile(tmp_path / "missing.flf")

    def test_compile_rejects_unwritable_target(self, tmp_path: Path, mocker: MockerFixture) -> None:
        font_path = tmp_path / "custom.flf"
        font_path.write_text(build_flf(), encoding="utf-8")

        def denied_write_bytes(self: Path, _data: bytes) -> int:
            raise OSError("denied")

        mocker.patch.object(Path, "write_bytes", denied_write_bytes)
        with pytest.raises(UnreachableFigletFontException):
            FigletFontLoader().compile(font_path)

    def test_bundled_falls_back_to_source_on_bad_dump(self, mocker: MockerFixture) -> None:
        def broken_load(self: object, *_args: object, **_kwargs: object) -> FigletFont:
            raise InvalidFigletFontException("broken")

        FigletFontLoader._bundled_fonts.clear()
        mocker.patch.object(FigletFontCompiler, "load", broken_load)
        font = FigletFontLoader().load_bundled(BundledFont.TARTY1)
        assert set("Argenta").issubset(font.glyphs)
        FigletFontLoader._bundled_fonts.clear()

    def test_bundled_font_is_cached(self) -> None:
        FigletFontLoader._bundled_fonts.clear()
        loader = FigletFontLoader()
        assert loader.load_bundled(BundledFont.TARTY1) is loader.load_bundled(BundledFont.TARTY1)
        FigletFontLoader._bundled_fonts.clear()

    def test_rejects_dump_with_mismatched_glyph_table(self, tmp_path: Path) -> None:
        dump_path = tmp_path / "custom.flfd"
        dump_path.write_bytes(b"FLFD\x01" + marshal.dumps((0, 2, "ab", "x")))
        with pytest.raises(InvalidFigletFontException, match="mismatched"):
            FigletFontLoader().load(dump_path)

    @pytest.mark.parametrize("bundled_font", list(BundledFont))
    def test_bundled_dump_matches_parsed_source(self, bundled_font: BundledFont) -> None:
        fonts_dir = files("argenta.app.presentation.ascii_art").joinpath("_fonts")
        parsed = FigletFontParser().parse(
            fonts_dir.joinpath(f"{bundled_font}.flf").read_bytes().decode("utf-8")
        )
        dumped = FigletFontCompiler().load(fonts_dir.joinpath(f"{bundled_font}.flfd").read_bytes())
        assert dumped == parsed
        assert FigletFontLoader().load_bundled(bundled_font) == parsed


class TestLazyGlyphs:
    def make_glyphs(self) -> Mapping[str, tuple[str, ...]]:
        return (
            FigletFontCompiler()
            .load(
                FigletFontCompiler().dump(
                    FigletFont(height=2, glyphs={"a": ("a0", "a1"), "b": ("b0", "b1")}),
                    source_mtime_ns=0,
                )
            )
            .glyphs
        )

    def test_materializes_glyph_on_access(self) -> None:
        assert self.make_glyphs()["a"] == ("a0", "a1")

    def test_memoizes_materialized_glyph(self) -> None:
        glyphs = self.make_glyphs()
        assert glyphs["a"] is glyphs["a"]

    def test_raises_key_error_on_unknown_char(self) -> None:
        with pytest.raises(KeyError):
            self.make_glyphs()["z"]

    def test_supports_mapping_protocol(self) -> None:
        glyphs = self.make_glyphs()
        assert len(glyphs) == 2
        assert set(glyphs) == {"a", "b"}
        assert "a" in glyphs
        assert "z" not in glyphs
        assert glyphs.get("z") is None

    def test_equals_plain_dict(self) -> None:
        glyphs = self.make_glyphs()
        assert glyphs == {"a": ("a0", "a1"), "b": ("b0", "b1")}
        assert glyphs != {"a": ("x",)}
        assert glyphs != "not a mapping"


class TestFigletFontFetcher:
    def stub_urlopen(self, mocker: MockerFixture, payloads: dict[str, bytes]) -> list[str]:
        requested: list[str] = []

        class FakeResponse:
            def __init__(self, body: bytes) -> None:
                self._body = body

            def read(self) -> bytes:
                return self._body

            def __enter__(self) -> Self:
                return self

            def __exit__(self, *_args: object) -> None:
                pass

        def fake_urlopen(url: str, **_kwargs: object) -> FakeResponse:
            requested.append(url)
            if url not in payloads:
                raise OSError("404")
            return FakeResponse(payloads[url])

        mocker.patch("argenta.app.presentation.ascii_art.fetcher.urlopen", new=fake_urlopen)
        return requested

    def test_fetches_font_by_name(self, tmp_path: Path, mocker: MockerFixture) -> None:
        font_bytes = build_flf(height=3).encode("utf-8")
        fetcher = FigletFontFetcher(cache_dir=tmp_path / "cache")
        payloads = {fetcher.sources[0].format(name="myfont"): font_bytes}
        self.stub_urlopen(mocker, payloads)

        target = fetcher.fetch("myfont", tmp_path)
        assert target == tmp_path / "myfont.flf"
        assert target.read_bytes() == font_bytes
        assert target.with_suffix(".flfd").is_file()

    def test_tries_alternative_sources_and_cases(
        self, tmp_path: Path, mocker: MockerFixture
    ) -> None:
        font_bytes = build_flf().encode("utf-8")
        fetcher = FigletFontFetcher(cache_dir=tmp_path / "cache")
        payloads = {fetcher.sources[1].format(name="Myfont"): font_bytes}
        requested = self.stub_urlopen(mocker, payloads)

        fetcher.fetch("myfont", tmp_path)
        assert len(requested) == 4
        assert requested[-1] == fetcher.sources[1].format(name="Myfont")

    def test_fetches_from_direct_url(self, tmp_path: Path, mocker: MockerFixture) -> None:
        url = "https://example.com/fonts/doom.flf"
        self.stub_urlopen(mocker, {url: build_flf().encode("utf-8")})
        target = FigletFontFetcher(cache_dir=tmp_path / "cache").fetch(url, tmp_path)
        assert target.name == "doom.flf"

    def test_rejects_unsafe_font_name(self, tmp_path: Path) -> None:
        with pytest.raises(InvalidFigletFontException, match="invalid font name"):
            FigletFontFetcher().fetch("../../etc/passwd", tmp_path)

    def test_encodes_font_names_with_spaces(self, tmp_path: Path, mocker: MockerFixture) -> None:
        font_bytes = build_flf().encode("utf-8")
        fetcher = FigletFontFetcher(cache_dir=tmp_path / "cache")
        payloads = {fetcher.sources[0].format(name="ANSI%20Shadow"): font_bytes}
        requested = self.stub_urlopen(mocker, payloads)

        fetcher.fetch("ANSI Shadow", tmp_path)
        assert requested[0].endswith("/ANSI%20Shadow.flf")

    def test_serves_second_fetch_from_cache(self, tmp_path: Path, mocker: MockerFixture) -> None:
        font_bytes = build_flf().encode("utf-8")
        fetcher = FigletFontFetcher(cache_dir=tmp_path / "cache")
        payloads = {fetcher.sources[0].format(name="myfont"): font_bytes}
        requested = self.stub_urlopen(mocker, payloads)

        for name in ("one", "two"):
            (tmp_path / name).mkdir()
            fetcher.fetch("myfont", tmp_path / name)
        assert len(requested) == 1
        assert (tmp_path / "two" / "myfont.flf").read_bytes() == font_bytes

    def test_no_cache_downloads_every_time(self, tmp_path: Path, mocker: MockerFixture) -> None:
        fetcher = FigletFontFetcher(use_cache=False)
        payloads = {fetcher.sources[0].format(name="myfont"): build_flf().encode("utf-8")}
        requested = self.stub_urlopen(mocker, payloads)

        for name in ("one", "two"):
            (tmp_path / name).mkdir()
            fetcher.fetch("myfont", tmp_path / name)
        assert len(requested) == 2

    def test_fetch_cached_returns_cache_path(self, tmp_path: Path, mocker: MockerFixture) -> None:
        fetcher = FigletFontFetcher(cache_dir=tmp_path / "cache")
        payloads = {fetcher.sources[0].format(name="myfont"): build_flf().encode("utf-8")}
        requested = self.stub_urlopen(mocker, payloads)

        cached = fetcher.fetch_cached("myfont")
        assert cached.parent == tmp_path / "cache"
        assert cached.name.endswith("-myfont.flf")
        assert cached.is_file()
        assert fetcher.fetch_cached("myfont") == cached
        assert len(requested) == 1

    def test_does_not_cache_invalid_download(self, tmp_path: Path, mocker: MockerFixture) -> None:
        fetcher = FigletFontFetcher(cache_dir=tmp_path / "cache")
        payloads = {fetcher.sources[0].format(name="bad"): b"not a font"}
        self.stub_urlopen(mocker, payloads)

        with pytest.raises(InvalidFigletFontException):
            fetcher.fetch_cached("bad")
        assert not list((tmp_path / "cache").iterdir())

    def test_raises_when_all_sources_fail(self, tmp_path: Path, mocker: MockerFixture) -> None:
        self.stub_urlopen(mocker, {})
        with pytest.raises(FigletFontFetchException, match="myfont"):
            FigletFontFetcher(cache_dir=tmp_path / "cache").fetch("myfont", tmp_path)

    def test_removes_invalid_downloaded_file(self, tmp_path: Path, mocker: MockerFixture) -> None:
        fetcher = FigletFontFetcher(use_cache=False)
        payloads = {fetcher.sources[0].format(name="bad"): b"not a font"}
        self.stub_urlopen(mocker, payloads)

        with pytest.raises(InvalidFigletFontException):
            fetcher.fetch("bad", tmp_path)
        assert not (tmp_path / "bad.flf").exists()

    def test_rejects_unwritable_target(self, tmp_path: Path, mocker: MockerFixture) -> None:
        fetcher = FigletFontFetcher(use_cache=False)
        self.stub_urlopen(
            mocker, {fetcher.sources[0].format(name="font"): build_flf().encode("utf-8")}
        )

        def denied_write_bytes(self: Path, _data: bytes) -> int:
            raise OSError("denied")

        mocker.patch.object(Path, "write_bytes", denied_write_bytes)
        with pytest.raises(UnreachableFigletFontException):
            fetcher.fetch("font", tmp_path)

    def test_lists_available_fonts(self, mocker: MockerFixture) -> None:
        payload = (
            b'{"tree": [{"path": "fonts/slant.flf"}, {"path": "README.md"}, {"path": "Doom.flf"}]}'
        )
        self.stub_urlopen(mocker, dict.fromkeys(FigletFontFetcher.index_sources, payload))
        assert FigletFontFetcher().list_available() == ["Doom", "slant"]

    def test_list_raises_on_malformed_index(self, mocker: MockerFixture) -> None:
        self.stub_urlopen(mocker, dict.fromkeys(FigletFontFetcher.index_sources, b"not json"))
        with pytest.raises(FigletFontFetchException, match="remote font index"):
            FigletFontFetcher().list_available()

    def test_list_raises_when_index_unreachable(self, mocker: MockerFixture) -> None:
        self.stub_urlopen(mocker, {})
        with pytest.raises(FigletFontFetchException, match="remote font index"):
            FigletFontFetcher().list_available()

    def test_rejects_unwritable_cache_dir(self, tmp_path: Path, mocker: MockerFixture) -> None:
        fetcher = FigletFontFetcher(cache_dir=tmp_path / "cache")
        self.stub_urlopen(
            mocker, {fetcher.sources[0].format(name="font"): build_flf().encode("utf-8")}
        )

        def denied_write_bytes(self: Path, _data: bytes) -> int:
            raise OSError("denied")

        mocker.patch.object(Path, "write_bytes", denied_write_bytes)
        with pytest.raises(UnreachableFigletFontException):
            fetcher.fetch_cached("font")

    def test_rejects_unreadable_cache_entry(self, tmp_path: Path, mocker: MockerFixture) -> None:
        fetcher = FigletFontFetcher(cache_dir=tmp_path / "cache")
        cached = fetcher._cache_path("myfont")
        cached.parent.mkdir(parents=True)
        cached.write_bytes(b"stale")
        original_read_bytes = Path.read_bytes

        def denied_read_bytes(self: Path) -> bytes:
            if self == cached:
                raise OSError("denied")
            return original_read_bytes(self)

        mocker.patch.object(Path, "read_bytes", denied_read_bytes)
        with pytest.raises(UnreachableFigletFontException, match="myfont"):
            fetcher.fetch("myfont", tmp_path)


class TestAsciiArtRenderer:
    font = FigletFont(height=2, glyphs={"a": ("a1", "a2"), "b": ("b1", "b2")})

    def test_joins_glyphs_row_by_row(self) -> None:
        assert AsciiArtRenderer().render("ab", self.font) == "a1b1\na2b2"

    def test_rejects_characters_missing_from_font(self) -> None:
        with pytest.raises(MissingGlyphsException, match="'\\?', 'я'") as error:
            AsciiArtRenderer().render("a?b\nя", self.font)
        assert error.value.missing_chars == {"?", "я"}

    def test_renders_each_text_line_separately(self) -> None:
        assert AsciiArtRenderer().render("a\nb", self.font) == "a1\na2\nb1\nb2"

    def test_does_not_double_separator_after_trailing_empty_row(self) -> None:
        padded_font = FigletFont(height=2, glyphs={"a": ("a1", "")})
        assert AsciiArtRenderer().render("a\na", padded_font) == "a1\na1\n"

    def test_renders_empty_text_as_empty_string(self) -> None:
        assert AsciiArtRenderer().render("", self.font) == ""


class TestAppCustomFonts:
    def test_uses_user_supplied_fonts(self) -> None:
        font = FigletFont(height=1, glyphs={char: (char * 2,) for char in PRINTABLE_ASCII})
        app = App(initial_message="Hi", initial_message_font=font, farewell_message_font=font)
        assert "HHii" in app._initial_message

    def test_fails_fast_on_text_the_font_cannot_render(self) -> None:
        with pytest.raises(FigletFontException):
            App(initial_message="Привет")
