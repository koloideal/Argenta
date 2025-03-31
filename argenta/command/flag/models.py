from typing import Literal, Pattern
from abc import ABC, abstractmethod


class BaseFlag:
    def __init__(self, name: str,
                 prefix: Literal['-', '--', '---'] = '--',
                 possible_values: list[str] | Pattern[str] | False = True):
        self._name = name
        self._prefix = prefix
        self.possible_values = possible_values

    def get_string_entity(self):
        string_entity: str = self._prefix + self._name
        return string_entity

    def get_name(self):
        return self._name

    def get_prefix(self):
        return self._prefix



class InputFlag(BaseFlag):
    def __init__(self, name: str,
                 prefix: Literal['-', '--', '---'] = '--',
                 possible_values: list[str] | Pattern[str] | False = True):
        super().__init__(name, prefix, possible_values)
        self._flag_value = None

    def get_value(self):
        return self._flag_value

    def set_value(self, value):
        self._flag_value = value



class Flag(BaseFlag):
    def validate_input_flag_value(self, input_flag_value: str | None):
        if self.possible_values is False:
            if input_flag_value is None:
                return True
            else:
                return False
        elif isinstance(self.possible_values, Pattern):
            is_valid = bool(self.possible_values.match(input_flag_value))
            if bool(is_valid):
                return True
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
    __slots__ = ('_flags',)

    @abstractmethod
    def get_flags(self):
        pass

    @abstractmethod
    def add_flag(self, flag: Flag | InputFlag):
        pass

    @abstractmethod
    def add_flags(self, flags: list[Flag] | list[InputFlag]):
        pass

    @abstractmethod
    def get_flag(self, name: str):
        pass

    def __iter__(self):
        return iter(self._flags)

    def __next__(self):
        return next(iter(self))

    def __getitem__(self, item):
        return self._flags[item]



class Flags(BaseFlags, ABC):
    def __init__(self, *flags: Flag):
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

