from pathlib import Path

from argenta import App
from argenta.app.presentation.ascii_art import FigletFontLoader

font_loader = FigletFontLoader()

app = App(
    initial_message="Storage CLI",
    initial_message_font=font_loader.load(Path("fonts/slant.flf")),
    farewell_message="Goodbye",
    farewell_message_font=font_loader.load(Path("fonts/mini.flf")),
)
