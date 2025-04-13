from abc import ABC, abstractmethod
from typing import Literal


class BaseArgument(ABC):
    @abstractmethod
    def get_string_entity(self):
        """
        Returns the string representation of the argument
        :return:
        """
        pass


class PositionalArgument(BaseArgument):
    def __init__(self, name: str):
        """
        Required argument at startup
        :param name: name of the argument, must not start with minus (-)
        """
        self.name = name

    def get_string_entity(self):
        return self.name


class OptionalArgument(BaseArgument):
    def __init__(self, name: str, prefix: Literal['-', '--', '---'] = '--'):
        """
        Optional argument, must have the value
        :param name: name of the argument
        :param prefix: prefix of the argument
        """
        self.name = name
        self.prefix = prefix

    def get_string_entity(self):
        return self.prefix + self.name


class BooleanArgument(BaseArgument):
    def __init__(self, name: str, prefix: Literal['-', '--', '---'] = '--'):
        """
        Boolean argument, does not require a value
        :param name: name of the argument
        :param prefix: prefix of the argument
        """
        self.name = name
        self.prefix = prefix

    def get_string_entity(self):
        return self.prefix + self.name
