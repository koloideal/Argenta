from argenta.command.flag.models import Flag, InputFlag
from abc import ABC, abstractmethod


class InputCommandException(ABC, Exception):
    """
    Private. Base exception class for all exceptions raised when parse input command
    """

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class UnprocessedInputFlagException(InputCommandException):
    """
    Private. Raised when an unprocessed input flag is detected
    """

    def __str__(self) -> str:
        return "Unprocessed Input Flags"


class RepeatedInputFlagsException(InputCommandException):
    """
    Private. Raised when repeated input flags are detected
    """

    def __init__(self, flag: Flag | InputFlag):
        self.flag = flag

    def __str__(self) -> str:
        string_entity: str = self.flag.string_entity
        return (
            "Repeated Input Flags\n"
            f"Duplicate flag was detected in the input: '{string_entity}'"
        )


class EmptyInputCommandException(InputCommandException):
    """
    Private. Raised when an empty input command is detected
    """

    def __str__(self) -> str:
        return "Input Command is empty"
