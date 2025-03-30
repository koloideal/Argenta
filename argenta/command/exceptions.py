from argenta.command.flag.input_flag.entity import InputFlag
from argenta.command.flag.registered_flag.entity import Flag


class UnprocessedInputFlagException(Exception):
    def __str__(self):
        return "Unprocessed Input Flags"


class RepeatedInputFlagsException(Exception):
    def __init__(self, flag: Flag | InputFlag):
        self.flag = flag
    def __str__(self):
        return ("Repeated Input Flags\n"
                f"Duplicate flag was detected in the input: '{self.flag.get_string_entity()}'")


class EmptyInputCommandException(Exception):
    def __str__(self):
        return "Input Command is empty"