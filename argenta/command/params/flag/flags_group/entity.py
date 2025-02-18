from argenta.command.params.flag.entity import Flag
from argenta.command.params.flag.input_flag.entity import InputFlag


class FlagsGroup:
    def __init__(self, flags: list[Flag | InputFlag] = None):
        self._flags: list[Flag | InputFlag] = [] if not flags else flags

    def get_flags(self):
        return self._flags

    def add_flag(self, flag: Flag | InputFlag):
        self._flags.append(flag)

    def add_flags(self, flags: list[Flag | InputFlag]):
        self._flags.extend(flags)

    def __iter__(self):
        return iter(self._flags)

    def __next__(self):
        return next(iter(self))
