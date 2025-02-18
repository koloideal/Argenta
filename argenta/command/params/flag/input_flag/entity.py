from ...flag.entity import Flag


class InputFlag(Flag):
    def set_value(self, value: str):
        self._value = value

    def get_value(self) -> str:
        return self._value


