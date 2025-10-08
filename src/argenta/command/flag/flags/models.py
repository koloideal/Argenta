from argenta.command.flag.models import InputFlag, Flag
from typing import Generic, TypeVar, override
from collections.abc import Iterator


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

    def __iter__(self) -> Iterator[FlagType]:
        return iter(self.flags)

    def __next__(self) -> FlagType:
        return next(iter(self))

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
            return NotImplemented

        if len(self.flags) != len(other.flags):
            return False

        flag_pairs: zip[tuple[Flag, Flag]] = zip(self.flags, other.flags)
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
    def get_flag_by_name(self, name: str) -> InputFlag | None:
        """
        Public. Returns the flag entity by its name or None if not found
        :param name: the name of the flag to get
        :return: entity of the flag or None
        """
        return next((flag for flag in self.flags if flag.name == name), None)
    
    @override
    def __eq__(self, other: object) -> bool: 
        if not isinstance(other, InputFlags):
            raise NotImplementedError

        if len(self.flags) != len(other.flags):
            return False

        paired_flags: zip[tuple[InputFlag, InputFlag]] = zip(self.flags, other.flags)

        return all(my_flag == other_flag for my_flag, other_flag in paired_flags)

    def __contains__(self, ingressable_item: object) -> bool:
        if isinstance(ingressable_item, InputFlag):
            for flag in self.flags:
                if flag == ingressable_item:
                    return True
            return False
        else:
            raise TypeError

