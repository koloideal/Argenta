import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from dishka import Container
from rich.console import Console

from argenta.app.presentation.ascii_art import (
    AsciiArtRenderer,
    FigletFontException,
    FigletFontFetcher,
    FigletFontLoader,
)

PREVIEW_TEXT = "Argenta"


def _render_preview(font_path: Path) -> str:
    loaded_font = FigletFontLoader().load(font_path)
    return AsciiArtRenderer().render(PREVIEW_TEXT, loaded_font)


def preview_font_handler(
    container: Container,
    font: str,
    cache_dir: str | None,
    no_cache: bool,
) -> None:
    console = container.get(Console)
    try:
        if no_cache:
            with TemporaryDirectory() as temp_dir:
                font_path = FigletFontFetcher(use_cache=False).fetch(font, temp_dir)
                console.print(_render_preview(font_path))
        else:
            font_path = FigletFontFetcher(cache_dir=cache_dir).fetch_cached(font)
            console.print(_render_preview(font_path))
    except FigletFontException as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        sys.exit(1)
