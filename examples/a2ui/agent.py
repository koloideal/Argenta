from argenta import App, Orchestrator
from argenta.app import StaticDividingLine
from argenta.app.presentation.ascii_art import AsciiArtRenderer, BundledFont, FigletFontLoader
from examples.a2ui.routers import release_router

_banner: str = AsciiArtRenderer().render(
    "Argenta", FigletFontLoader().load_bundled(BundledFont.TARTY1)
)
app: App = App(
    initial_message=_banner,
    dividing_line=StaticDividingLine("~"),
    override_system_messages=True,
    printer=print,
)
orchestrator: Orchestrator = Orchestrator()


def main() -> None:
    app.include_router(release_router)
    orchestrator.run_repl(app)


if __name__ == "__main__":
    main()
