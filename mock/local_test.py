from rich.console import Console

from argenta.app.presentation.renderers import RichRenderer, Renderer, PlainRenderer, RendererMixin


def main(rend: Renderer):
    pass

def mm(tr) -> str | None:
    pass

main(RichRenderer(print, mm))
main(PlainRenderer(print, mm))
main()