class InvalidDescriptionInstanceException(Exception):
    def __str__(self):
        return "Invalid Description Instance"


class RepeatedCommandException(Exception):
    def __str__(self):
        return "Commands in handler cannot be repeated"


class RepeatedFlagNameException(Exception):
    def __str__(self):
        return "Repeated flag name in register command"


class TooManyTransferredArgsException(Exception):
    def __str__(self):
        return "Too many transferred arguments"


class RequiredArgumentNotPassedException(Exception):
    def __str__(self):
        return "Required argument not passed"


class NotValidInputFlagHandlerHasBeenAlreadyCreatedException(Exception):
    def __str__(self):
        return "Invalid Input Flag Handler has already been created"


class IncorrectNumberOfHandlerArgsException(Exception):
    def __str__(self):
        return "Incorrect Input Flags Handler has incorrect number of arguments"
