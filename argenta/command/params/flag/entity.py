from typing import Literal


class Flag:
    def __init__(self, flag_name: str,
                 flag_prefix: Literal['-', '--', '---'] = '-',
                 ignore_flag_value_register: bool = False,
                 possible_flag_values: list[str] = False):
        self._flag_name = flag_name
        self._flag_prefix = flag_prefix
        self.possible_flag_values = possible_flag_values
        self.ignore_flag_value_register = ignore_flag_value_register

        self._value = None

    def get_string_entity(self):
        string_entity: str = self._flag_prefix + self._flag_name
        return string_entity

    def get_flag_name(self):
        return self._flag_name

    def get_flag_prefix(self):
        return self._flag_prefix

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def validate_input_flag_value(self, input_flag_value: str):
        if self.possible_flag_values:
            if self.ignore_flag_value_register:
                if input_flag_value.lower() in [x.lower() for x in self.possible_flag_values]:
                    return True
                else:
                    return False
            else:
                if input_flag_value in self.possible_flag_values:
                    return True
                else:
                    return False
        else:
            return True
