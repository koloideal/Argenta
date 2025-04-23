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



class InputFlag(BaseFlag):
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



class BaseFlags(ABC):
    """
    Private. Base class for groups of flags
    """
    __slots__ = ('_flags',)

    @abstractmethod
    def get_flags(self):
        """
        Public. Returns a list of flags
        :return: list of flags
        """
        pass

    @abstractmethod
    def add_flag(self, flag: Flag | InputFlag):
        """
        Public. Adds a flag to the list of flags
        :param flag: flag to add
        :return: None
        """
        pass

    @abstractmethod
    def add_flags(self, flags: list[Flag] | list[InputFlag]):
        """
        Public. Adds a list of flags to the list of flags
        :param flags: list of flags to add
        :return: None
        """
        pass

    @abstractmethod
    def get_flag(self, name: str):
        """
        Public. Returns the flag entity by its name or None if not found
        :param name: the name of the flag to get
        :return: entity of the flag or None
        """
        pass

    def __iter__(self):
        return iter(self._flags)

    def __next__(self):
        return next(iter(self))

    def __getitem__(self, item):
        return self._flags[item]



class Flags(BaseFlags, ABC):
    def __init__(self, *flags: Flag):
        """
        Public. A model that combines the registered flags
        :param flags: the flags that will be registered
        :return: None
        """
        self._flags = flags if flags else []

    def get_flags(self) -> list[Flag]:
        return self._flags

    def add_flag(self, flag: Flag):
        self._flags.append(flag)

    def add_flags(self, flags: list[Flag]):
        self._flags.extend(flags)

    def get_flag(self, name: str) -> Flag | None:
        if name in [flag.get_name() for flag in self._flags]:
            return list(filter(lambda flag: flag.get_name() == name, self._flags))[0]
        else:
            return None



class InputFlags(BaseFlags, ABC):
    def __init__(self, *flags: InputFlag):
        """
        Public. A model that combines the input flags of the input command
        :param flags: all input flags
        :return: None
        """
        self._flags = flags if flags else []

    def get_flags(self) -> list[InputFlag]:
        return self._flags

    def add_flag(self, flag: InputFlag):
        self._flags.append(flag)

    def add_flags(self, flags: list[InputFlag]):
        self._flags.extend(flags)

    def get_flag(self, name: str) -> InputFlag | None:
        if name in [flag.get_name() for flag in self._flags]:
            return list(filter(lambda flag: flag.get_name() == name, self._flags))[0]
        else:
            return None

