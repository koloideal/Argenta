from abc import ABC, abstractmethod
from typing import Literal, override


class BaseArgument(ABC):
    """
    Private. Base class for all arguments
    """
    @property
    @abstractmethod
    def string_entity(self) -> str:
        """
        Public. Returns the string representation of the argument
        :return: the string representation as a str
        """
        raise NotImplementedError


class RequiredArgument(BaseArgument):
    def __init__(self, name: str, *,
                       prefix: Literal["-", "--", "---"] = "--",
                       help: str = "Help for required argument",
                       default: str | None = None,
                       possible_values: list[str] | None = None,
                       is_required: bool = True,
                       is_deprecated: bool = False):
        """
        Public. Required argument at startup
        :param name: name of the argument, must not start with minus (-)
        :param prefix: prefix of the argument
        :param help: help message for the argument
        :param default: default value for the argument
        :param possible_values: list of possible values for the argument
        :param is_required: whether the argument is required
        :param is_deprecated: whether the argument is deprecated
        """
        self.name: str = name
        self.prefix: Literal["-", "--", "---"] = prefix
        self.help: str = help
        self.default: str | None = default
        self.possible_values: list[str] | None = possible_values
        self.is_required: bool = is_required
        self.is_deprecated: bool = is_deprecated
        self.action: str = "store"

    @property
    @override
    def string_entity(self) -> str:
        return self.prefix + self.name


class ValueArgument(BaseArgument):
    def __init__(self, name: str, *,
                       prefix: Literal["-", "--", "---"] = "--", 
                       help: str = "Help message for the value argument", 
                       possible_values: list[str] | None = None,
                       default: str | None = None,
                       is_required: bool = False,
                       is_deprecated: bool = False):
        """
        Public. Value argument, must have the value
        :param name: name of the argument
        :param prefix: prefix of the argument
        :param help: help message for the argument
        :param possible_values: list of possible values for the argument
        :param default: default value for the argument
        :param is_required: whether the argument is required
        :param is_deprecated: whether the argument is deprecated
        """
        self.name: str = name
        self.prefix: Literal["-", "--", "---"] = prefix
        self.help: str = help
        self.possible_values: list[str] | None = possible_values
        self.default: str | None = default
        self.is_required: bool = is_required
        self.is_deprecated: bool = is_deprecated
        self.action: str = "store"

    @property
    @override
    def string_entity(self) -> str:
        return self.prefix + self.name


class BooleanArgument(BaseArgument):
    def __init__(self, name: str, *,
                       prefix: Literal["-", "--", "---"] = "--",
                       help: str = "Help message for the boolean argument",
                       is_required: bool = False,
                       is_deprecated: bool = False):
        """
        Public. Boolean argument, does not require a value
        :param name: name of the argument
        :param prefix: prefix of the argument
        :param help: help message for the argument
        :param is_required: whether the argument is required
        :param is_deprecated: whether the argument is deprecated
        """
        self.name: str = name
        self.prefix: Literal["-", "--", "---"] = prefix
        self.help: str = help
        self.is_required: bool = is_required
        self.is_deprecated: bool = is_deprecated
        self.action: str = "store_true"

    @property
    @override
    def string_entity(self) -> str:
        return self.prefix + self.name
