from abc import ABC, abstractmethod
from typing import Literal


class BaseArgument(ABC):
    """
    Private. Base class for all arguments
    """
    @abstractmethod
    def get_string_entity(self) -> str:
        """
        Public. Returns the string representation of the argument
        :return: the string representation as a str
        """
        pass


class PositionalArgument(BaseArgument):
    def __init__(self, name: str):
        """
        Public. Required argument at startup
        :param name: name of the argument, must not start with minus (-)
        """
        self.name = name

    def get_string_entity(self) -> str:
        return self.name


class OptionalArgument(BaseArgument):
    def __init__(self, name: str, prefix: Literal["-", "--", "---"] = "--"):
        """
        Public. Optional argument, must have the value
        :param name: name of the argument
        :param prefix: prefix of the argument
        """
        self.name = name
        self.prefix = prefix

    def get_string_entity(self) -> str:
        return self.prefix + self.name


class BooleanArgument(BaseArgument):
    def __init__(self, name: str, prefix: Literal["-", "--", "---"] = "--"):
        """
        Public. Boolean argument, does not require a value
        :param name: name of the argument
        :param prefix: prefix of the argument
        """
        self.name = name
        self.prefix = prefix

    def get_string_entity(self) -> str:
        return self.prefix + self.name
