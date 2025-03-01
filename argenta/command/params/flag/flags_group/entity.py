from argenta.command.params.flag.entity import Flag


class FlagsGroup:
    def __init__(self, flags: list[Flag] = None):
        self._flags: list[Flag] = [] if not flags else flags

    def get_flags(self):
        return self._flags

    def add_flag(self, flag: Flag):
        self._flags.append(flag)

    def add_flags(self, flags: list[Flag]):
        self._flags.extend(flags)

    def __iter__(self):
        return iter(self._flags)

    def __next__(self):
        return next(iter(self))

    def __getitem__(self, item):
        return self._flags[item]
