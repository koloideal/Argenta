from argenta.command.params.flag.entity import Flag


class FlagsGroup:
    def __init__(self, flags: list[Flag] = None):
        self._flags: list[Flag] = [] if not flags else flags

    def get_flags(self) -> list[Flag]:
        return self._flags

    def add_flag(self, flag: Flag):
        self._flags.append(flag)

    def add_flags(self, flags: list[Flag]):
        self._flags.extend(flags)

    def unparse_to_dict(self):
        result_dict: dict[str, dict] = {}
        for flag in self._flags:
            result_dict[flag.get_flag_name()] = {
                'name': flag.get_flag_name(),
                'string_entity': flag.get_string_entity(),
                'prefix': flag.get_flag_prefix(),
                'value': flag.get_value()
            }
        return result_dict

    def __iter__(self):
        return iter(self._flags)

    def __next__(self):
        return next(iter(self))

    def __getitem__(self, item):
        return self._flags[item]
