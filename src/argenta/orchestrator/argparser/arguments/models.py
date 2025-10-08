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


class PositionalArgument(BaseArgument):
    def __init__(self, name: str):
        """
        Public. Required argument at startup
        :param name: name of the argument, must not start with minus (-)
        """
        self.name: str = name

    @property
    @override
    def string_entity(self) -> str:
        return self.name


class OptionalArgument(BaseArgument):
    def __init__(self, name: str, prefix: Literal["-", "--", "---"] = "--"):
        """
        Public. Optional argument, must have the value
        :param name: name of the argument
        :param prefix: prefix of the argument
        """
        self.name: str = name
        self.prefix: Literal["-", "--", "---"] = prefix

    @property
    @override
    def string_entity(self) -> str:
        return self.prefix + self.name


class BooleanArgument(BaseArgument):
    def __init__(self, name: str, prefix: Literal["-", "--", "---"] = "--"):
        """
        Public. Boolean argument, does not require a value
        :param name: name of the argument
        :param prefix: prefix of the argument
        """
        self.name: str = name
        self.prefix: Literal["-", "--", "---"] = prefix

    @property
    @override
    def string_entity(self) -> str:
        return self.prefix + self.name
