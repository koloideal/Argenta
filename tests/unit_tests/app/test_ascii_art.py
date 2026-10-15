from pathlib import Path

import pytest

from argenta.app import App
from argenta.app.presentation.ascii_art import (
    AsciiArtRenderer,
    BundledFont,
    FigletFont,
    FigletFontException,
    FigletFontLoader,
    FigletFontParser,
    InvalidFigletFontException,
    MissingGlyphsException,
    UnreachableFigletFontException,
)

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
