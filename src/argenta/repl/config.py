from dataclasses import dataclass

from argenta.repl.dividing_line import DynamicDividingLine, StaticDividingLine


@dataclass(frozen=True, slots=True)
class REPLConfig:
    """
    Public. Terminal layout of the REPL runtime: the dividing line that
    frames command output and the blank-line gaps between blocks
    """

    dividing_line: StaticDividingLine | DynamicDividingLine | None = None
    prompt_gap: int = 1
    frame_padding: int = 1
    startup_messages_gap: int = 1
    command_groups_gap: int = 2
