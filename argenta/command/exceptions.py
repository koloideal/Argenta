from .params.flag.entity import Flag


class InvalidCommandInstanceException(Exception):
    def __str__(self):
        return "Invalid Command Instance"


class InvalidDescriptionInstanceException(Exception):
    def __str__(self):
        return "Invalid Description Instance"


class InvalidFlagsInstanceException(Exception):
    def __str__(self):
        return "Invalid Flags Instance"


class UnprocessedInputFlagException(Exception):
    def __str__(self):
        return "Unprocessed Input Flags"


class RepeatedInputFlagsException(Exception):
    def __init__(self, flag: Flag):
        self.flag = flag
    def __str__(self):
        return ("Repeated Input Flags\n"
                f"Duplicate flag was detected in the input: '{self.flag.get_string_entity()}'")


class EmptyInputCommandException(Exception):
    def __str__(self):
        return "Input Command is empty"