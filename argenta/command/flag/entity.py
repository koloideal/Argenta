from typing import Literal, Pattern


class Flag:
    def __init__(self, flag_name: str,
                 flag_prefix: Literal['-', '--', '---'] = '--',
                 possible_flag_values: list[str] | Pattern[str] | False = True):
        self._flag_name = flag_name
        self._flag_prefix = flag_prefix
        self.possible_flag_values = possible_flag_values

        self._flag_value = None

    def get_string_entity(self):
        string_entity: str = self._flag_prefix + self._flag_name
        return string_entity

    def get_flag_name(self):
        return self._flag_name

    def get_flag_prefix(self):
        return self._flag_prefix

    def get_value(self):
        return self._flag_value

    def set_value(self, value):
        self._flag_value = value

    def validate_input_flag_value(self, input_flag_value: str | None):
        if self.possible_flag_values is False:
            if input_flag_value is None:
                return True
            else:
                return False
        elif isinstance(self.possible_flag_values, Pattern):
            is_valid = bool(self.possible_flag_values.match(input_flag_value))
            if bool(is_valid):
                return True
            else:
                return False

        elif isinstance(self.possible_flag_values, list):
            if input_flag_value in self.possible_flag_values:
                return True
            else:
                return False
        else:
            return True
