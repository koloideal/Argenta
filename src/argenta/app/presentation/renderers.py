from typing import Iterable, Protocol

from art import text2art

from argenta.app.protocols import DescriptionMessageGenerator
from argenta.app.registered_routers.entity import RegisteredRouters


class Renderer(Protocol):
    @staticmethod
    def render_prompt(
            text: str
    ) -> str: ...
    @staticmethod
    def render_initial_message(
            text: str
    ) -> str: ...
    @staticmethod
    def render_farewell_message(
            text: str
    ) -> str: ...
    @staticmethod
    def render_messages_on_startup(
            messages: Iterable[str]
    ) -> str: ...
    @staticmethod
    def render_text_for_description_message_generator(
            command: str,
            description: str
    ) -> str: ...
    @staticmethod
    def render_command_groups_description(
            description_message_generator: DescriptionMessageGenerator,
            registered_routers: RegisteredRouters
    ) -> str: ...
    @staticmethod
    def render_text_for_incorrect_input_syntax_handler(
            raw_command: str
    ) -> str: ...
    @staticmethod
    def render_text_for_repeated_input_flags_handler(
            raw_command: str
    ) -> str: ...
    @staticmethod
    def render_text_for_empty_input_command_handler() -> str: ...
    @staticmethod
    def render_text_for_unknown_command_handler(
            command_trigger: str,
            most_similar_command_trigger: str | None
    ) -> str: ...


class RichRenderer(Renderer):
    @staticmethod
    def render_prompt(text: str) -> str:
        return f"<gray><b>{text}</b></gray>"

    @staticmethod
    def render_initial_message(text: str) -> str:
        return f"[bold red]{text2art(text, font='tarty1')}[/bold red]"

    @staticmethod
    def render_farewell_message(text: str) -> str:
        return (
            "[bold red]"
            + str(text2art(text, font="chanky"))
            + "[/bold red]\n"
            + "[red i]https://github.com/koloideal/Argenta[/red i] | [red bold i]made by kolo[/red bold i]"
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
        return "\n" + "\n".join(messages)

    @staticmethod
    def render_command_groups_description(
        description_message_generator: DescriptionMessageGenerator,
        registered_routers: RegisteredRouters
    ) -> str:
        command_groups_description = ""
        for registered_router in registered_routers:
            command_groups_description += "\n\n" + registered_router.title
            for command_handler in registered_router.command_handlers:
                handled_command = command_handler.handled_command
                command_groups_description += '\n' + description_message_generator(
                    handled_command.trigger,
                    handled_command.description,
                )
        return command_groups_description

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
        command_trigger: str,
        most_similar_command_trigger: str | None
    ) -> str:
        return (
            f"[red]Unknown command:[/red] [blue]{command_trigger}[/blue]"
            + (f"[red], most similar:[/red][blue]{most_similar_command_trigger}[/blue]"
            if most_similar_command_trigger else "")
        )


class PlainRenderer(Renderer):
    @staticmethod
    def render_prompt(text: str) -> str:
        return text

    @staticmethod
    def render_initial_message(text: str) -> str:
        return text

    @staticmethod
    def render_farewell_message(text: str) -> str:
        return f"\n{text} | https://github.com/koloideal/Argenta | made by kolo"

    @staticmethod
    def render_text_for_description_message_generator(command: str, description: str) -> str:
        return f"{command} *=*=* {description}"

    def render_messages_on_startup(self, messages: Iterable[str]) -> str:
        return "\n" + "\n".join(messages)

    @staticmethod
    def render_command_groups_description(
        description_message_generator: DescriptionMessageGenerator,
        registered_routers: RegisteredRouters,
    ) -> str:
        command_groups_description = ""
        for registered_router in registered_routers:
            command_groups_description += "\n\n" + registered_router.title
            for command_handler in registered_router.command_handlers:
                handled_command = command_handler.handled_command
                command_groups_description += "\n" + description_message_generator(
                    handled_command.trigger,
                    handled_command.description,
                )
        return command_groups_description

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
        command_trigger: str,
        most_similar_command_trigger: str | None
    ) -> str:
        return (
            f"Unknown command: {command_trigger}"
            + (f", most similar: {most_similar_command_trigger}"
            if most_similar_command_trigger else "")
        )

