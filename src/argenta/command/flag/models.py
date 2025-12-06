__all__ = ["PossibleValues", "ValidationStatus", "Flag", "InputFlag"]

from enum import Enum
from re import Pattern
from typing import Literal, override


PREFIX_TYPE = Literal["-", "--", "---"]


class PossibleValues(Enum):
    NEITHER = "NEITHER"
    ALL = "ALL"


class ValidationStatus(Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    UNDEFINED = "UNDEFINED"


class Flag:
    def __init__(
        self,
        name: str,
        *,
        prefix: PREFIX_TYPE = "--",
        possible_values: list[str] | Pattern[str] | PossibleValues = PossibleValues.ALL,
    ) -> None:
        """
        Public. The entity of the flag being registered for subsequent processing
        :param name: The name of the flag
        :param prefix: The prefix of the flag
        :param possible_values: The possible values of the flag, if False then the flag cannot have a value
        :return: None
        """
        self.name: str = name
        self.prefix: PREFIX_TYPE = prefix
        self.possible_values: list[str] | Pattern[str] | PossibleValues = possible_values

    def validate_input_flag_value(self, input_flag_value: str) -> bool:
        """
        Private. Validates the input flag value
        :param input_flag_value: The input flag value to validate
        :return: whether the entered flag is valid as bool
        """ 
        if isinstance(self.possible_values, PossibleValues):
            if self.possible_values == PossibleValues.NEITHER:
                return input_flag_value == ''
            return input_flag_value != ''

        if isinstance(self.possible_values, Pattern):
            return bool(self.possible_values.match(input_flag_value))

        return input_flag_value in self.possible_values

    @property
    def string_entity(self) -> str:
        """
        Public. Returns a string representation of the flag
        :return: string representation of the flag as str
        """
        string_entity: str = self.prefix + self.name
        return string_entity

    @override
    def __str__(self) -> str:
        return self.string_entity

    @override
    def __repr__(self) -> str:
        return f"Flag<name={self.name}, prefix={self.prefix}>"

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Flag):
            return self.string_entity == other.string_entity
        else:
            raise NotImplementedError


class InputFlag:
    def __init__(
        self,
        name: str,
        *,
        input_value: str,
        prefix: PREFIX_TYPE = "--",
        status: ValidationStatus | None = None,
    ):
        """
        Public. The entity of the flag of the entered command
        :param name: the name of the input flag
        :param prefix: the prefix of the input flag
        :param value: the value of the input flag
        :return: None
        """
        self.name: str = name
        self.prefix: PREFIX_TYPE = prefix
        self.input_value: str = input_value
        self.status: ValidationStatus | None = status

    @property
    def string_entity(self) -> str:
        """
        Public. Returns a string representation of the flag
        :return: string representation of the flag as str
        """
        string_entity: str = self.prefix + self.name
        return string_entity

    @override
    def __str__(self) -> str:
        return f"{self.string_entity} {self.input_value}"

    @override
    def __repr__(self) -> str:
        return f"InputFlag<name={self.name}, prefix={self.prefix}, value={self.input_value}, status={self.status}>"

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, InputFlag):
            return self.name == other.name
        else:
            raise NotImplementedError
