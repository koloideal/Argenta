from abc import ABC, abstractmethod
from typing import Protocol, Iterable

from art import text2art
from rich.markup import escape

from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.response.entity import Response
from argenta.command.models import InputCommand
from argenta.app.protocols import (
    DescriptionMessageGenerator,
    EmptyCommandHandler,
    MostSimilarCommandGetter,
    NonStandardBehaviorHandler,
    Printer
)


class RendererMixin(ABC):
    def __init__(self, print_func: Printer, most_similar_command_getter: MostSimilarCommandGetter) -> None:
        self._print_func = print_func
        self._most_similar_command_getter = most_similar_command_getter

        self._cached_command_groups_description: str | None = None

    @staticmethod
    @abstractmethod
    def generate_formatted_description_message_gen() -> DescriptionMessageGenerator:
        raise NotImplementedError

    @staticmethod
    def render_messages_on_startup(messages: Iterable[str]) -> str:
        return "\n".join(messages)

    def render_command_groups_description(self, registered_routers: RegisteredRouters) -> str:
        if self._cached_command_groups_description:
            return self._cached_command_groups_description
        command_groups_description = ""
        for registered_router in registered_routers:
            command_groups_description += "\n" + registered_router.title
            for command_handler in registered_router.command_handlers:
                handled_command = command_handler.handled_command
                command_groups_description += self.generate_formatted_description_message_gen()(
                    handled_command.trigger,
                    handled_command.description,
                )
        self._cached_command_groups_description = command_groups_description
        return command_groups_description

    def generate_formatted_exit_command_handler(self, farewell_message: str) -> NonStandardBehaviorHandler[Response]:
        return lambda _: self._print_func(farewell_message)


class Renderer(Protocol):
    @staticmethod
    def render_prompt(text: str) -> str: ...

    @staticmethod
    def render_initial_message(text: str) -> str: ...

    @staticmethod
    def render_farewell_message(text: str) -> str: ...

    @staticmethod
    def render_messages_on_startup(messages: Iterable[str]) -> str: ...

    @staticmethod
    def generate_formatted_description_message_gen() -> DescriptionMessageGenerator: ...

    def render_command_groups_description(self, registered_routers: RegisteredRouters) -> str: ...

    def generate_formatted_incorrect_input_syntax_handler(self) -> NonStandardBehaviorHandler[str]: ...

    def generate_formatted_repeated_input_flags_handler(self) -> NonStandardBehaviorHandler[str]: ...

    def generate_formatted_empty_input_command_handler(self) -> EmptyCommandHandler: ...

    def generate_formatted_unknown_command_handler(self) -> NonStandardBehaviorHandler[InputCommand]: ...

    def generate_formatted_exit_command_handler(self, farewell_message: str) -> NonStandardBehaviorHandler[Response]: ...


class RichRenderer(RendererMixin):
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
    def generate_formatted_description_message_gen() -> DescriptionMessageGenerator:
        return lambda command, description: (
            f"[bold red]{escape('[' + command + ']')}[/bold red] "
            f"[blue dim]*=*=*[/blue dim] "
            f"[bold yellow italic]{escape(description)}[/bold yellow italic]"
        )

    def generate_formatted_incorrect_input_syntax_handler(self) -> NonStandardBehaviorHandler[str]:
        return lambda raw_command: self._print_func(f"[red bold]Incorrect flag syntax: {escape(raw_command)}[/red bold]")

    def generate_formatted_repeated_input_flags_handler(self) -> NonStandardBehaviorHandler[str]:
        return lambda raw_command: self._print_func(f"[red bold]Repeated input flags: {escape(raw_command)}[/red bold]")

    def generate_formatted_empty_input_command_handler(self) -> EmptyCommandHandler:
        return lambda: self._print_func("[red bold]Empty input command[/red bold]")

    def generate_formatted_unknown_command_handler(self) -> NonStandardBehaviorHandler[InputCommand]:
        def unknown_command_handler(command: InputCommand) -> None:
            cmd_trg: str = command.trigger
            mst_sim_cmd: str | None = self._most_similar_command_getter(cmd_trg)
            self._print_func(
                f"[red]Unknown command:[/red][blue]{escape(cmd_trg)}[/blue][red]"
                + (f", most similar:[/red][blue]{mst_sim_cmd}[/blue]" if mst_sim_cmd else "")
            )

        return unknown_command_handler


class PlainRenderer(RendererMixin):
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
    def generate_formatted_description_message_gen() -> DescriptionMessageGenerator:
        return lambda command, description: f"{command} *=*=* {description}"

    def generate_formatted_incorrect_input_syntax_handler(self) -> NonStandardBehaviorHandler[str]:
        return lambda raw_command: self._print_func(f"Incorrect flag syntax: {escape(raw_command)}")

    def generate_formatted_repeated_input_flags_handler(self) -> NonStandardBehaviorHandler[str]:
        return lambda raw_command: self._print_func(f"Repeated input flags: {escape(raw_command)}")

    def generate_formatted_empty_input_command_handler(self) -> EmptyCommandHandler:
        return lambda: self._print_func("Empty input command")

    def generate_formatted_unknown_command_handler(self) -> NonStandardBehaviorHandler[InputCommand]:
        def unknown_command_handler(command: InputCommand) -> None:
            cmd_trg: str = command.trigger
            mst_sim_cmd: str | None = self._most_similar_command_getter(cmd_trg)
            self._print_func(
                f"Unknown command: {escape(cmd_trg)}"
                + (f", most similar:{mst_sim_cmd}" if mst_sim_cmd else "")
            )

        return unknown_command_handler
