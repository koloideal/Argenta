from re import Pattern
from typing import Literal

from argenta.command.flag.base_flag.entity import BaseFlag


class InputFlag(BaseFlag):
    def __init__(self, flag_name: str,
                 flag_prefix: Literal['-', '--', '---'] = '--',
                 possible_flag_values: list[str] | Pattern[str] | False = True):
        super().__init__(flag_name, flag_prefix, possible_flag_values)
        self._flag_value = None

    def get_value(self):
        return self._flag_value

    def set_value(self, value):
        self._flag_value = value
