class InvalidDescriptionInstanceException(Exception):
    def __str__(self):
        return "Invalid Description Instance"


class RepeatedCommandException(Exception):
    def __str__(self):
        return "Commands in handler cannot be repeated"


class RepeatedFlagNameException(Exception):
    def __str__(self):
        return "Repeated flag name in register command"


class CurrentCommandDoesNotProcessFlagsException(Exception):
    def __str__(self):
        return "Current command does not process flags"


class TooManyTransferredArgsException(Exception):
    def __str__(self):
        return "Too many transferred arguments"


class RequiredArgumentNotPassedException(Exception):
    def __str__(self):
        return "Required argument not passed"
