from rich.markup import escape

from argenta.app.presentation.renderers import Renderer
from argenta.app.protocols import (DescriptionMessageGenerator, EmptyCommandHandler,
                                   MostSimilarCommandGetter, NonStandardBehaviorHandler,
                                   Printer)
from argenta.command import InputCommand
from argenta.response.entity import Response


class BehaviorHandlersFabric:
    def __init__(
        self,
        printer: Printer,
        renderer: Renderer,
        most_similar_command_getter: MostSimilarCommandGetter,
    ) -> None:
        self._printer = printer
        self._renderer = renderer
        self._most_similar_command_getter = most_similar_command_getter

    def generate_incorrect_input_syntax_handler(self) -> NonStandardBehaviorHandler[str]:
        return lambda raw_command: self._printer(
            self._renderer.render_text_for_incorrect_input_syntax_handler(
                raw_command=escape(raw_command)
            )
        )

    def generate_repeated_input_flags_handler(self) -> NonStandardBehaviorHandler[str]:
        return lambda raw_command: self._printer(
            self._renderer.render_text_for_repeated_input_flags_handler(
                raw_command=escape(raw_command)
            )
        )

    def generate_empty_input_command_handler(self) -> EmptyCommandHandler:
        return lambda: self._printer(self._renderer.render_text_for_empty_input_command_handler())

    def generate_unknown_command_handler(self) -> NonStandardBehaviorHandler[InputCommand]:
        def unknown_command_handler(command: InputCommand) -> None:
            command_trigger: str = command.trigger
            most_similar_command_trigger: str | None = self._most_similar_command_getter(command_trigger)
            self._printer(
                self._renderer.render_text_for_unknown_command_handler(
                    command_trigger=command_trigger,
                    most_similar_command_trigger=most_similar_command_trigger
                )
            )
        return unknown_command_handler

    def generate_exit_command_handler(self, farewell_message: str) -> NonStandardBehaviorHandler[Response]:
        return lambda _: self._printer(farewell_message)

    def generate_description_message_generator(self) -> DescriptionMessageGenerator:
        return lambda command, description: self._renderer.render_text_for_description_message_generator(
            command=command,
            description=description
        )


class BehaviorHandlersSettersMixin:
    def __init__(
        self,
        description_message_generator: DescriptionMessageGenerator,
        incorrect_input_syntax_handler: NonStandardBehaviorHandler[str],
        repeated_input_flags_handler: NonStandardBehaviorHandler[str],
        empty_input_command_handler: EmptyCommandHandler,
        unknown_command_handler: NonStandardBehaviorHandler[InputCommand],
        exit_command_handler: NonStandardBehaviorHandler[Response]
    ):
        self._description_message_generator: DescriptionMessageGenerator = description_message_generator
        self._incorrect_input_syntax_handler: NonStandardBehaviorHandler[str] = incorrect_input_syntax_handler
        self._repeated_input_flags_handler: NonStandardBehaviorHandler[str] = repeated_input_flags_handler
        self._empty_input_command_handler: EmptyCommandHandler = empty_input_command_handler
        self._unknown_command_handler: NonStandardBehaviorHandler[InputCommand] = unknown_command_handler
        self._exit_command_handler: NonStandardBehaviorHandler[Response] = exit_command_handler

    def set_description_message_pattern(self, _: DescriptionMessageGenerator, /) -> None:
        self._description_message_generator = _

    def set_incorrect_input_syntax_handler(self, _: NonStandardBehaviorHandler[str], /) -> None:
        self._incorrect_input_syntax_handler = _

    def set_repeated_input_flags_handler(self, _: NonStandardBehaviorHandler[str], /) -> None:
        self._repeated_input_flags_handler = _

    def set_unknown_command_handler(self, _: NonStandardBehaviorHandler[InputCommand], /) -> None:
        self._unknown_command_handler = _

    def set_empty_command_handler(self, _: EmptyCommandHandler, /) -> None:
        """
        Public. Sets the handler for empty commands when entering a command
        :param _: handler for empty commands when entering a command
        :return: None
        """
        self._empty_input_command_handler = _

    def set_exit_command_handler(self, _: NonStandardBehaviorHandler[Response], /) -> None:
        """
        Public. Sets the handler for exit command when entering a command
        :param _: handler for exit command when entering a command
        :return: None
        """
        self._exit_command_handler = _
