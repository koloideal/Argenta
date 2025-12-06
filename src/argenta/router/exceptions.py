__all__ = ["RepeatedFlagNameException", "RequiredArgumentNotPassedException", "TriggerContainSpacesException"]

from typing import override


class RepeatedFlagNameException(Exception):
    """
    Private. Raised when a repeated flag name is registered
    """

    @override
    def __str__(self) -> str:
        return "Repeated registered flag names in register command"


class RequiredArgumentNotPassedException(Exception):
    """
    Private. Raised when a required argument is not passed
    """

    @override
    def __str__(self) -> str:
        return "Required argument with type Response not passed"


class TriggerContainSpacesException(Exception):
    """
    Private. Raised when there is a space in the trigger being registered
    """

    @override
    def __str__(self) -> str:
        return "Command trigger cannot contain spaces"
