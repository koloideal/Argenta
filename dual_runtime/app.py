"""Application factory shared by every runtime in this example."""

from typing import Final

from argenta import App

PROMPT: Final = "inventory> "


def build_app(*, plain: bool) -> App:
    """
    Builds the inventory application for a concrete runtime

    :param plain: True renders system output as plain text — required
           for non-terminal renderers (A2UI agents, transcripts);
           False keeps the Rich rendering and the figlet banner
    :return: configured App without routers
    """
    if plain:
        return App(
            prompt=PROMPT,
            initial_message="Inventory",
            farewell_message="Done",
            override_system_messages=True,
            printer=print,
        )
    return App(prompt=PROMPT, initial_message="Inventory", farewell_message="Done")
