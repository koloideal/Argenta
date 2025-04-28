from argenta.command.flag.models import InputFlag, Flag
from typing import Generic, TypeVar



FlagType = TypeVar('FlagType')


class BaseFlags(Generic[FlagType]):
    def __init__(self, *flags: FlagType):
        """
        Public. A model that combines the registered flags
        :param flags: the flags that will be registered
        :return: None
        """
        self._flags = flags if flags else []

    def get_flags(self) -> list[FlagType]:
        """
        Public. Returns a list of flags
        :return: list of flags as list[FlagType]
        """
        return self._flags

    def add_flag(self, flag: FlagType):
        """
        Public. Adds a flag to the list of flags
        :param flag: flag to add
        :return: None
        """
        self._flags.append(flag)

    def add_flags(self, flags: list[FlagType]):
        """
        Public. Adds a list of flags to the list of flags
        :param flags: list of flags to add
        :return: None
        """
        self._flags.extend(flags)

    def get_flag(self, name: str) -> FlagType | None:
        """
        Public. Returns the flag entity by its name or None if not found
        :param name: the name of the flag to get
        :return: entity of the flag or None
        """
        if name in [flag.get_name() for flag in self._flags]:
            return list(filter(lambda flag: flag.get_name() == name, self._flags))[0]
        else:
            return None

    def __iter__(self):
        return iter(self._flags)

    def __next__(self):
        return next(iter(self))

    def __getitem__(self, item):
        return self._flags[item]


class Flags(BaseFlags[Flag]): pass


class InputFlags(BaseFlags[InputFlag]): pass


class ValidInputFlags(InputFlags): pass


class UndefinedInputFlags(InputFlags): pass


class InvalidValueInputFlags(InputFlags): pass

