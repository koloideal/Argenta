from collections.abc import Callable
from contextlib import redirect_stdout
from functools import partial
from io import StringIO

from rich.text import Text

from argenta.app.presentation.layout import BlockKind
from argenta.app.presentation.renderers import Renderer
from argenta.app.protocols import Printer
from argenta.repl.config import REPLConfig
from argenta.repl.dividing_line import DynamicDividingLine, StaticDividingLine


def _capture_stdout(produce: Callable[[], None]) -> str:
    buffer = StringIO()
    with redirect_stdout(buffer):
        produce()
    return buffer.getvalue()


def _static_line(dividing_line: StaticDividingLine | DynamicDividingLine) -> str:
    """Private. Uncaptured output cannot size a dynamic line: fall back
    to a static line of the default length with the same unit"""
    if isinstance(dividing_line, StaticDividingLine):
        return dividing_line.line()
    return StaticDividingLine(dividing_line.get_unit_part()).line()


class TerminalLayout:
    """
    Public. Layout of an interactive terminal session: command and system
    output is framed by the dividing line because a prompt sits between
    consecutive outputs; other blocks are separated by blank-line gaps
    """

    def __init__(self, printer: Printer, renderer: Renderer, config: REPLConfig) -> None:
        """
        :param printer: system messages text output function
        :param renderer: renders the dividing line markup
        :param config: dividing line and gap configuration
        """
        self._printer = printer
        self._renderer = renderer
        self._config = config
        self._gaps_before: dict[BlockKind, int] = {
            BlockKind.STARTUP_MESSAGES: config.startup_messages_gap,
            BlockKind.COMMAND_GROUPS: config.command_groups_gap,
        }

    def present(
        self, kind: BlockKind, produce: Callable[[], None], *, capturable: bool = True
    ) -> None:
        """
        Public. Prints the gap configured for the block kind, then the
        block; command and system output is framed
        :param kind: semantic kind of the block
        :param produce: prints the block content
        :param capturable: False when stdout of the producer must not be intercepted
        :return: None
        """
        self._blank_lines(self._gaps_before.get(kind, 0))
        if kind in {BlockKind.OUTPUT, BlockKind.SYSTEM}:
            self._framed(produce, capturable=capturable)
        else:
            produce()

    def read_input(self, read: Callable[[], str]) -> str:
        """
        Public. Surrounds an input prompt with the prompt gap
        :param read: reads one line of user input
        :return: the entered line
        """
        self._blank_lines(self._config.prompt_gap)
        raw_input = read()
        self._blank_lines(self._config.prompt_gap)
        return raw_input

    def _framed(self, produce: Callable[[], None], *, capturable: bool) -> None:
        dividing_line = self._config.dividing_line
        if dividing_line is None:
            produce()
        elif isinstance(dividing_line, DynamicDividingLine) and capturable:
            captured = _capture_stdout(produce)
            framed_text = Text.from_ansi(captured.strip("\n")).markup
            self._frame(dividing_line.line_for(captured), partial(self._printer, framed_text))
        else:
            self._frame(_static_line(dividing_line), produce)

    def _frame(self, raw_line: str, body: Callable[[], None]) -> None:
        line = self._renderer.render_dividing_line(raw_line)
        self._printer(line)
        self._blank_lines(self._config.frame_padding)
        body()
        self._blank_lines(self._config.frame_padding)
        self._printer(line)

    def _blank_lines(self, count: int) -> None:
        for _ in range(count):
            self._printer("")
