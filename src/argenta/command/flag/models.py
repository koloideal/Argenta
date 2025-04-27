from typing import Literal, Pattern
from abc import ABC, abstractmethod


class BaseFlag(ABC):
    def __init__(self, name: str,
                 prefix: Literal['-', '--', '---'] = '--') -> None:
        """
        Private. Base class for flags
        :param name: the name of the flag
        :param prefix: the prefix of the flag
        :return: None
        """
        self._name = name
        self._prefix = prefix

    def get_string_entity(self) -> str:
        """
        Public. Returns a string representation of the flag
        :return: string representation of the flag as str
        """
        string_entity: str = self._prefix + self._name
        return string_entity

    def get_name(self) -> str:
        """
        Public. Returns the name of the flag
        :return: the name of the flag as str
        """
        return self._name

    def get_prefix(self) -> str:
        """
        Public. Returns the prefix of the flag
        :return: the prefix of the flag as str
        """
        return self._prefix



class Flag(BaseFlag):
    def __init__(self, name: str,
                 prefix: Literal['-', '--', '---'] = '--',
                 possible_values: list[str] | Pattern[str] | False = True) -> None:
        """
        Public. The entity of the flag being registered for subsequent processing
        :param name: The name of the flag
        :param prefix: The prefix of the flag
        :param possible_values: The possible values of the flag, if False then the flag cannot have a value
        :return: None
        """
        super().__init__(name, prefix)
        self.possible_values = possible_values

    def validate_input_flag_value(self, input_flag_value: str | None):
        """
        Private. Validates the input flag value
        :param input_flag_value: The input flag value to validate
        :return: whether the entered flag is valid as bool
        """
        if self.possible_values is False:
            if input_flag_value is None:
                return True
            else:
                return False
        elif isinstance(self.possible_values, Pattern):
            if isinstance(input_flag_value, str):
                is_valid = bool(self.possible_values.match(input_flag_value))
                if bool(is_valid):
                    return True
                else:
                    return False
            else:
                return False

        elif isinstance(self.possible_values, list):
            if input_flag_value in self.possible_values:
                return True
            else:
                return False
        else:
            return True



class ValidInputFlag(BaseFlag):
    def __init__(self, name: str,
                 prefix: Literal['-', '--', '---'] = '--',
                 value: str = None):
        """
        Public. The entity of the flag of the entered command
        :param name: the name of the input flag
        :param prefix: the prefix of the input flag
        :param value: the value of the input flag
        :return: None
        """
        super().__init__(name, prefix)
        self._flag_value = value

    def get_value(self) -> str | None:
        """
        Public. Returns the value of the flag
        :return: the value of the flag as str
        """
        return self._flag_value

    def set_value(self, value):
        """
        Private. Sets the value of the flag
        :param value: the fag value to set
        :return: None
        """
        self._flag_value = value



class UndefinedInputFlag(ValidInputFlag): pass



class InvalidValueInputFlag(ValidInputFlag): pass

