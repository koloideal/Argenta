from argenta.command.flag.models import Flag, InputFlag


class BaseInputCommandException(Exception):
    """
    Private. Base exception class for all exceptions raised when parse input command
    """

    pass


class UnprocessedInputFlagException(BaseInputCommandException):
    """
    Private. Raised when an unprocessed input flag is detected
    """

    def __str__(self):
        return "Unprocessed Input Flags"


class RepeatedInputFlagsException(BaseInputCommandException):
    """
    Private. Raised when repeated input flags are detected
    """

    def __init__(self, flag: Flag | InputFlag):
        self.flag = flag

    def __str__(self):
        return (
            "Repeated Input Flags\n"
            f"Duplicate flag was detected in the input: '{self.flag.get_string_entity()}'"
        )


class EmptyInputCommandException(BaseInputCommandException):
    """
    Private. Raised when an empty input command is detected
    """

    def __str__(self):
        return "Input Command is empty"
