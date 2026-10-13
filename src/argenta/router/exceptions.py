from typing import override


class RepeatedFlagNameException(Exception):
    """
    Private. Raised when a repeated flag name is registered
    """

    @override
    def __init__(self, repeated_flags: set[str], trigger: str) -> None:
        self.repeated_flags = repeated_flags
        self.trigger = trigger
        super().__init__()

    @override
    def __str__(self) -> str:
        return f"Repeated flag names {self.repeated_flags} in command '{self.trigger}'"


class RepeatedTriggerNameException(Exception):
    """
    Private. Raised when a repeated trigger name is registered
    """

    @override
    def __init__(self, repeated_triggers: set[str]) -> None:
        self.repeated_triggers = repeated_triggers
        super().__init__()

    @override
    def __str__(self) -> str:
        return f"Repeated trigger names: {self.repeated_triggers}"


class RepeatedAliasNameException(Exception):
    """
    Private. Raised when a repeated alias name is registered
    """

    @override
    def __init__(self, repeated_aliases: set[str]) -> None:
        self.repeated_aliases = repeated_aliases
        super().__init__()

    @override
    def __str__(self) -> str:
        return f"Repeated aliases names: {self.repeated_aliases}"


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
