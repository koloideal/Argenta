from collections.abc import Iterable
from typing import Protocol

from argenta.app.presentation.ascii_art import AsciiArtRenderer, FigletFont
from argenta.app.protocols import DescriptionMessageGenerator
from argenta.app.registered_routers.entity import RegisteredRouters


class Renderer(Protocol):
    @staticmethod
    def render_prompt(text: str) -> str: ...

    def render_initial_message(self, text: str) -> str: ...

    def render_farewell_message(self, text: str) -> str: ...

    @staticmethod
    def render_messages_on_startup(messages: Iterable[str]) -> str: ...

    @staticmethod
    def render_text_for_description_message_generator(command: str, description: str) -> str: ...

    @staticmethod
    def render_command_groups_description(
        description_message_generator: DescriptionMessageGenerator,
        registered_routers: RegisteredRouters,
    ) -> str: ...

    @staticmethod
    def render_text_for_incorrect_input_syntax_handler(raw_command: str) -> str: ...

    @staticmethod
    def render_text_for_repeated_input_flags_handler(raw_command: str) -> str: ...

    @staticmethod
    def render_text_for_empty_input_command_handler() -> str: ...

    @staticmethod
    def render_text_for_unknown_command_handler(
        command_trigger: str, most_similar_command_trigger: str | None
    ) -> str: ...

    @staticmethod
    def render_dividing_line(line: str) -> str: ...


def _command_groups_text(
    description_message_generator: DescriptionMessageGenerator,
    registered_routers: RegisteredRouters,
) -> str:
    sections: list[str] = []
    for registered_router in registered_routers:
        lines = [registered_router.title]
        for command_handler in registered_router.command_handlers:
            handled_command = command_handler.handled_command
            lines.append(
                description_message_generator(handled_command.trigger, handled_command.description)
            )
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


class RichRenderer(Renderer):
    def __init__(self, initial_message_font: FigletFont, farewell_message_font: FigletFont) -> None:
        self._initial_message_font: FigletFont = initial_message_font
        self._farewell_message_font: FigletFont = farewell_message_font
        self._ascii_art_renderer: AsciiArtRenderer = AsciiArtRenderer()

    @staticmethod
    def render_prompt(text: str) -> str:
        return f"<gray><b>{text}</b></gray>"

    def render_initial_message(self, text: str) -> str:
        ascii_art = self._ascii_art_renderer.render(text, self._initial_message_font)
        return f"[bold red]{ascii_art}[/bold red]"

    def render_farewell_message(self, text: str) -> str:
        ascii_art = self._ascii_art_renderer.render(text, self._farewell_message_font)
        return (
            f"[bold red]{ascii_art}[/bold red]\n"
            "[red i]https://github.com/koloideal/Argenta[/red i] | "
            "[red bold i]made by kolo[/red bold i]"
        )

    @staticmethod
    def render_text_for_description_message_generator(command: str, description: str) -> str:
        return (
            f"[bold red]<{command}>[/bold red] "
            f"[blue dim]*=*=*[/blue dim] "
            f"[bold yellow italic]{description}[/bold yellow italic]"
        )

    @staticmethod
    def render_messages_on_startup(messages: Iterable[str]) -> str:
        return "\n".join(messages)

    @staticmethod
    def render_command_groups_description(
        description_message_generator: DescriptionMessageGenerator,
        registered_routers: RegisteredRouters,
    ) -> str:
        return _command_groups_text(description_message_generator, registered_routers)

    @staticmethod
    def render_dividing_line(line: str) -> str:
        return f"[dim]{line}[/dim]"

    @staticmethod
    def render_text_for_incorrect_input_syntax_handler(raw_command: str) -> str:
        return f"[red bold]Incorrect flag syntax: {raw_command}[/red bold]"

    @staticmethod
    def render_text_for_repeated_input_flags_handler(raw_command: str) -> str:
        return f"[red bold]Repeated input flags: {raw_command}[/red bold]"

    @staticmethod
    def render_text_for_empty_input_command_handler() -> str:
        return "[red bold]Empty input command[/red bold]"

    @staticmethod
    def render_text_for_unknown_command_handler(
        command_trigger: str, most_similar_command_trigger: str | None
    ) -> str:
        most_similar_part = (
            f"[red], most similar:[/red] [blue]{most_similar_command_trigger}[/blue]"
            if most_similar_command_trigger
            else ""
        )
        return f"[red]Unknown command:[/red] [blue]{command_trigger}[/blue]{most_similar_part}"


class PlainRenderer(Renderer):
    @staticmethod
    def render_prompt(text: str) -> str:
        return text

    @staticmethod
    def render_initial_message(text: str) -> str:
        return text

    @staticmethod
    def render_farewell_message(text: str) -> str:
        return f"{text} | https://github.com/koloideal/Argenta | made by kolo"

    @staticmethod
    def render_text_for_description_message_generator(command: str, description: str) -> str:
        return f"{command} *=*=* {description}"

    @staticmethod
    def render_messages_on_startup(messages: Iterable[str]) -> str:
        return "\n".join(messages)

    @staticmethod
    def render_command_groups_description(
        description_message_generator: DescriptionMessageGenerator,
        registered_routers: RegisteredRouters,
    ) -> str:
        return _command_groups_text(description_message_generator, registered_routers)

    @staticmethod
    def render_dividing_line(line: str) -> str:
        return line

    @staticmethod
    def render_text_for_incorrect_input_syntax_handler(raw_command: str) -> str:
        return f"Incorrect flag syntax: {raw_command}"

    @staticmethod
    def render_text_for_repeated_input_flags_handler(raw_command: str) -> str:
        return f"Repeated input flags: {raw_command}"

    @staticmethod
    def render_text_for_empty_input_command_handler() -> str:
        return "Empty input command"

    @staticmethod
    def render_text_for_unknown_command_handler(
        command_trigger: str, most_similar_command_trigger: str | None
    ) -> str:
        most_similar_part = (
            f", most similar: {most_similar_command_trigger}"
            if most_similar_command_trigger
            else ""
        )
        return f"Unknown command: {command_trigger}{most_similar_part}"
