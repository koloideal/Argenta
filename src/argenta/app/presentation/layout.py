from collections.abc import Callable
from enum import StrEnum
from typing import Protocol


class BlockKind(StrEnum):
    """
    Public. Semantic kind of a block the application emits; runtimes
    decide how each kind is laid out (gaps, frames, separators)
    """

    BANNER = "banner"
    STARTUP_MESSAGES = "startup_messages"
    COMMAND_GROUPS = "command_groups"
    OUTPUT = "output"
    SYSTEM = "system"
    FAREWELL = "farewell"
    ERROR = "error"


class Layout(Protocol):
    """
    Public. Runtime-owned presentation strategy: the application hands
    over every block as a producer that prints its content, the layout
    decides what surrounds it
    """

    def present(
        self, kind: BlockKind, produce: Callable[[], None], *, capturable: bool = True
    ) -> None:
        """
        Public. Presents one block
        :param kind: semantic kind of the block
        :param produce: prints the block content (system printer or handler output)
        :param capturable: False when stdout of the producer must not be
               intercepted (handlers that read interactive input)
        :return: None
        """
        raise NotImplementedError  # pragma: no cover
