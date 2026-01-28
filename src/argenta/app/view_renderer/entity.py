from typing import Protocol, Iterable

from art import text2art
from rich.markup import escape

from argenta.response.entity import Response
from argenta.command.models import InputCommand
from argenta.app.protocols import (
    DescriptionMessageGenerator,
    EmptyCommandHandler,
    MostSimilarCommandGetter,
    NonStandardBehaviorHandler,
    Printer,
)


class ConcatenateRenderer:
    def render_concatenated_messages_on_startup(self, messages: Iterable[str]) -> str:
        return "\n".join(messages)


class ViewRenderer(Protocol):
    def render_prompt(self, text: str) -> str: ...

    def render_initial_message(self, text: str) -> str: ...

    def render_farewell_message(self, text: str) -> str: ...

    def generate_formatted_description_message_gen(self) -> DescriptionMessageGenerator: ...

    def generate_formatted_incorrect_input_syntax_handler(self) -> NonStandardBehaviorHandler[str]: ...

    def generate_formatted_repeated_input_flags_handler(self) -> NonStandardBehaviorHandler[str]: ...

    def generate_formatted_empty_input_command_handler(self) -> EmptyCommandHandler: ...

    def generate_formatted_unknown_command_handler(self) -> NonStandardBehaviorHandler[InputCommand]: ...

    def generate_formatted_exit_command_handler(self, farewell_message: str) -> NonStandardBehaviorHandler[Response]: ...


class RichRenderer(ViewRenderer):
    def __init__(self, print_func: Printer, most_similar_command_getter: MostSimilarCommandGetter) -> None:
        self._print_func = print_func
        self._most_similar_command_getter = most_similar_command_getter

    def render_prompt(self, text: str) -> str:
        return f"<gray><b>{text}</b></gray>"

    def render_initial_message(self, text: str) -> str:
        return f"[bold red]{text2art(text, font='tarty1')}[/bold red]"

    def render_farewell_message(self, text: str) -> str:
        return (
            "[bold red]"
            + str(text2art(text, font="chanky"))
            + "[/bold red]\n"
            + "[red i]https://github.com/koloideal/Argenta[/red i] | [red bold i]made by kolo[/red bold i]"
        )

    def generate_formatted_description_message_gen(self) -> DescriptionMessageGenerator:
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
                f"[red]Unknown command:[/red][blue]{escape(cmd_trg)}[/blue][red]" +
                (f", most similar:[/red][blue]{mst_sim_cmd}[/blue]"
                if mst_sim_cmd
                else "")
            )

        return unknown_command_handler

    def generate_formatted_exit_command_handler(self, farewell_message: str) -> NonStandardBehaviorHandler[Response]:
        return lambda _: self._print_func(farewell_message)


class PlainRenderer(ViewRenderer):
    def __init__(self, print_func: Printer, most_similar_command_getter: MostSimilarCommandGetter) -> None:
        self._print_func = print_func
        self._most_similar_command_getter = most_similar_command_getter

    def render_prompt(self, text: str) -> str:
        return text

    def render_initial_message(self, text: str) -> str:
        return text

    def render_farewell_message(self, text: str) -> str:
        return f"{text} | https://github.com/koloideal/Argenta | made by kolo"

    def generate_formatted_description_message_gen(self) -> DescriptionMessageGenerator:
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

    def generate_formatted_exit_command_handler(self, farewell_message: str) -> NonStandardBehaviorHandler[Response]:
        return lambda _: self._print_func(farewell_message)
