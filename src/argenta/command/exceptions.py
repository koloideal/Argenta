__all__ = [
    "InputCommandException",
    "UnprocessedInputFlagException",
    "RepeatedInputFlagsException",
    "EmptyInputCommandException",
]

from abc import ABC, abstractmethod
from typing import override

from argenta.command.flag.models import Flag, InputFlag


class InputCommandException(ABC, Exception):
    """
    Private. Base exception class for all exceptions raised when parse input command
    """

    @override
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class UnprocessedInputFlagException(InputCommandException):
    """
    Private. Raised when an unprocessed input flag is detected
    """

    @override
    def __str__(self) -> str:
        return "Unprocessed Input Flags"


class RepeatedInputFlagsException(InputCommandException):
    """
    Private. Raised when repeated input flags are detected
    """

    def __init__(self, flag: Flag | InputFlag):
        self.flag: Flag | InputFlag = flag
        super().__init__()

    @override
    def __str__(self) -> str:
        string_entity: str = self.flag.string_entity
        return f"Repeated Input Flags\nDuplicate flag was detected in the input: '{string_entity}'"


class EmptyInputCommandException(InputCommandException):
    """
    Private. Raised when an empty input command is detected
    """

    @override
    def __str__(self) -> str:
        return "Input Command is empty"
