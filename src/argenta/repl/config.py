from dataclasses import dataclass
from typing import Annotated

from argenta.repl.dividing_line import DynamicDividingLine, StaticDividingLine


@dataclass(frozen=True, slots=True)
class REPLConfig:
    """
    Public. Terminal layout of the REPL runtime: the dividing line that
    frames command output and the blank-line gaps between blocks
    """

    dividing_line: Annotated[
        StaticDividingLine | DynamicDividingLine | None,
        "Line framing command and system output above and below; None draws no frame",
    ] = None
    prompt_gap: Annotated[int, "Blank lines printed before and after the input prompt"] = 1
    frame_padding: Annotated[
        int, "Blank lines between the dividing line and the framed output, on both sides"
    ] = 1
    startup_messages_gap: Annotated[
        int, "Blank lines between the banner and the startup messages"
    ] = 1
    command_groups_gap: Annotated[
        int, "Blank lines before the list of available commands (also in repeat mode)"
    ] = 2
