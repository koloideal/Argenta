from ..params.flag.input_flag.entity import InputFlag


class InvalidInputFlagException(Exception):
    def __init__(self, flag: InputFlag):
        self.flag = flag
    def __str__(self):
        return ("Invalid Input Flags\n"
                f"Unknown or invalid input flag: '{self.flag.get_string_entity()} {self.flag.get_value()}'")

class IncorrectInputFlagException(Exception):
    def __str__(self):
        return "Incorrect Input Flags"


class RepeatedInputFlagsException(Exception):
    def __init__(self, flag: InputFlag):
        self.flag = flag
    def __str__(self):
        return ("Repeated Input Flags\n"
                f"Duplicate flag was detected in the input: '{self.flag.get_string_entity()}'")


class InvalidInputFlagsHandlerHasBeenAlreadyCreatedException(Exception):
    def __str__(self):
        return "Invalid Input Flags Handler has already been created"


class IncorrectNumberArgsInvalidInputFlagsHandlerException(Exception):
    def __str__(self):
        return "Incorrect Input Flags Handler has incorrect number of arguments"



