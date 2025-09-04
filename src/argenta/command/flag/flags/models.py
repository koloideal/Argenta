from argenta.command.flag.models import InputFlag, Flag
from typing import Generic, Optional, Self, TypeVar


FlagType = TypeVar("FlagType")


class BaseFlags(Generic[FlagType]):
    def __init__(self, flags: Optional[list[FlagType]] = None) -> None:
        """
        Public. A model that combines the registered flags
        :param flags: the flags that will be registered
        :return: None
        """
        self._flags: list[FlagType] = flags if flags else []

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

    def __iter__(self):
        return iter(self._flags)

    def __next__(self):
        return next(iter(self))

    def __getitem__(self, item: int) -> FlagType:
        return self._flags[item]

    def __bool__(self):
        return bool(self._flags)

    def __eq__(self, other: Self): # pyright: ignore[reportIncompatibleMethodOverride]
        if not isinstance(other, Self):
            return NotImplemented
        
        if len(self.get_flags()) != len(other.get_flags()):
            return False
        else:
            for flag, other_flag in zip(self.get_flags(), other.get_flags()): 
                if not (flag == other_flag):
                    return False
        return True


class Flags(BaseFlags[Flag]):
    def get_flag(self, name: str) -> Flag | None:
        """
        Public. Returns the flag entity by its name or None if not found
        :param name: the name of the flag to get
        :return: entity of the flag or None
        """
        if name in [flag.get_name() for flag in self._flags]:
            return list(filter(lambda flag: flag.get_name() == name, self._flags))[0]
        else:
            return None


class InputFlags(BaseFlags[InputFlag]):
    def get_flag(self, name: str) -> InputFlag | None:
        """
        Public. Returns the flag entity by its name or None if not found
        :param name: the name of the flag to get
        :return: entity of the flag or None
        """
        if name in [flag.get_name() for flag in self._flags]:
            return list(filter(lambda flag: flag.get_name() == name, self._flags))[0]
        else:
            return None

