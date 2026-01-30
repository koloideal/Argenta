from typing import Iterable

from argenta.app.presentation.renderers import Renderer
from argenta.app.protocols import Printer, DescriptionMessageGenerator
from argenta.app.registered_routers.entity import RegisteredRouters


class Viewer:
    def __init__(self, printer: Printer, renderer: Renderer):
        self._printer = printer
        self._renderer = renderer

    def view_messages_on_startup(self, messages: Iterable[str]) -> None:
        self._printer(self._renderer.render_messages_on_startup(messages))

    def view_command_groups_description(
        self,
        description_message_generator: DescriptionMessageGenerator,
        registered_routers: RegisteredRouters
    ) -> None:
        self._printer(
            self._renderer.render_command_groups_description(
                description_message_generator,
                registered_routers
            )
        )

