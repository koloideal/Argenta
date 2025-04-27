from argenta.command.flag import Flag, ValidInputFlag



class Flags:
    def __init__(self, *flags: Flag):
        """
        Public. A model that combines the registered flags
        :param flags: the flags that will be registered
        :return: None
        """
        self._flags = flags if flags else []

    def get_flags(self) -> list[Flag]:
        """
        Public. Returns a list of flags
        :return: list of flags
        """
        return self._flags

    def add_flag(self, flag: Flag):
        """
        Public. Adds a flag to the list of flags
        :param flag: flag to add
        :return: None
        """
        self._flags.append(flag)

    def add_flags(self, flags: list[Flag]):
        """
        Public. Adds a list of flags to the list of flags
        :param flags: list of flags to add
        :return: None
        """
        self._flags.extend(flags)

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

    def __iter__(self):
        return iter(self._flags)

    def __next__(self):
        return next(iter(self))

    def __getitem__(self, item):
        return self._flags[item]



class ValidInputFlags(ValidInputFlag):
    pass


class UndefinedInputFlags(ValidInputFlags):
    pass


class InvalidValueInputFlags(ValidInputFlags):
    pass

