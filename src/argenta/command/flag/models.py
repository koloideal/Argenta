__all__ = ["PossibleValues", "ValidationStatus", "Flag", "InputFlag", "InputFlags", "Flags"]

from enum import Enum
from re import Pattern
from typing import Any, Container, Generic, Iterator, Literal, TypeVar, override

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
        possible_values: Container[str] | Pattern[str] | PossibleValues = PossibleValues.ALL,
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
        self.possible_values: Container[str] | Pattern[str] | PossibleValues = possible_values

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
        :param input_value: the value of the input flag
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


FlagType = TypeVar("FlagType")


class BaseFlags(Generic[FlagType]):
    def __init__(self, flags: list[FlagType] | None = None) -> None:
        """
        Public. A model that combines the registered flags
        :param flags: the flags that will be registered
        :return: None
        """
        self.flags: list[FlagType] = flags if flags else []

    def add_flag(self, flag: FlagType) -> None:
        """
        Public. Adds a flag to the list of flags
        :param flag: flag to add
        :return: None
        """
        self.flags.append(flag)

    def add_flags(self, flags: list[FlagType]) -> None:
        """
        Public. Adds a list of flags to the list of flags
        :param flags: list of flags to add
        :return: None
        """
        self.flags.extend(flags)

    def __len__(self) -> int:
        return len(self.flags)

    def __iter__(self) -> Iterator[FlagType]:
        return iter(self.flags)

    def __getitem__(self, flag_index: int) -> FlagType:
        return self.flags[flag_index]

    def __bool__(self) -> bool:
        return bool(self.flags)


class Flags(BaseFlags[Flag]):
    def get_flag_by_name(self, name: str) -> Flag | None:
        """
        Public. Returns the flag entity by its name or None if not found
        :param name: the name of the flag to get
        :return: entity of the flag or None
        """
        return next((flag for flag in self.flags if flag.name == name), None)

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Flags):
            return False

        if len(self.flags) != len(other.flags):
            return False

        flag_pairs: Iterator[tuple[Flag, Flag]] = zip(self.flags, other.flags)
        return all(s_flag == o_flag for s_flag, o_flag in flag_pairs)

    def __contains__(self, flag_to_check: object) -> bool:
        if isinstance(flag_to_check, Flag):
            for flag in self.flags:
                if flag == flag_to_check:
                    return True
            return False
        else:
            raise TypeError


class InputFlags(BaseFlags[InputFlag]):
    def get_flag_by_name(
            self,
            name: str,
            with_status: ValidationStatus | None = None,
            default: Any = None
    ) -> InputFlag | None:
        """
        Public. Returns the flag entity by its name or None if not found
        :param default:
        :param with_status:
        :param name: the name of the flag to get
        :return: entity of the flag or None
        """
        if with_status is None:
            return next((flag for flag in self.flags if flag.name == name), default)
        else:
            return next((flag for flag in self.flags if flag.name == name and flag.status == with_status), default)

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InputFlags):
            return False

        if len(self.flags) != len(other.flags):
            return False

        paired_flags: Iterator[tuple[InputFlag, InputFlag]] = zip(self.flags, other.flags)

        return all(my_flag == other_flag for my_flag, other_flag in paired_flags)

    def __contains__(self, ingressable_item: object) -> bool:
        if isinstance(ingressable_item, InputFlag):
            for flag in self.flags:
                if flag == ingressable_item:
                    return True
            return False
        else:
            raise TypeError
