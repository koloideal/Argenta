__all__ = ["Viewer"]

import re
from contextlib import redirect_stdout
from io import StringIO
from typing import Callable, Iterable, TypeAlias

from rich.text import Text

from argenta.app import DynamicDividingLine, StaticDividingLine
from argenta.app.presentation.renderers import Renderer
from argenta.app.protocols import DescriptionMessageGenerator, Printer
from argenta.app.registered_routers.entity import RegisteredRouters

AVAILABLE_DIVIDING_LINES: TypeAlias = StaticDividingLine | DynamicDividingLine | None


class Viewer:
    ANSI_ESCAPE_RE: re.Pattern[str] = re.compile(r"\u001b\[[0-9;]*m")

    def __init__(
            self,
            printer: Printer,
            renderer: Renderer,
            dividing_line: AVAILABLE_DIVIDING_LINES,
            override_system_messages: bool
    ):
        self._printer = printer
        self._renderer = renderer
        self._dividing_line = dividing_line
        self._override_system_messages = override_system_messages
        self._stdout_buffer: StringIO = StringIO()

    def _capture_stdout(self, func: Callable[[], None]) -> str:
        self._stdout_buffer.seek(0)
        self._stdout_buffer.truncate(0)
        with redirect_stdout(self._stdout_buffer):
            func()
        return self._stdout_buffer.getvalue()

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

    def view_initial_message(self, initial_message: str) -> None:
        self._printer(initial_message)

    def view_framed_text_from_generator(
        self,
        output_text_generator: Callable[[], None],
        is_stdout_redirected_by_router: bool = False,
    ) -> None:
        match (self._dividing_line, is_stdout_redirected_by_router):
            case (None, bool()):
                output_text_generator()
            case (DynamicDividingLine(), False):
                stdout_result = self._capture_stdout(
                    lambda: output_text_generator()
                )
                clear_text = self.ANSI_ESCAPE_RE.sub("", stdout_result)
                max_length_line = max([len(line) for line in clear_text.split("\n")])
                max_length_line = (
                    max_length_line
                    if 10 <= max_length_line <= 100
                    else 100
                    if max_length_line > 100
                    else 10
                )
                dynamic_dividing_line_as_str: str = self._dividing_line.get_full_dynamic_line(
                    length=max_length_line, is_override=self._override_system_messages
                )
                self._printer(dynamic_dividing_line_as_str + "\n")
                self._printer(Text.from_ansi(stdout_result.strip("\n")).markup)
                self._printer('\n' + dynamic_dividing_line_as_str)

            case (StaticDividingLine() as dividing_line, bool()) | (DynamicDividingLine() as dividing_line, True):
                static_dividing_line_as_str: str = StaticDividingLine(dividing_line.get_unit_part()).get_full_static_line(
                    is_override=self._override_system_messages
                )
                self._printer(static_dividing_line_as_str + '\n')
                output_text_generator()
                self._printer('\n' + static_dividing_line_as_str)
            case _:
                raise NotImplementedError(f"Dividing line with type {self._dividing_line} is not implemented")
