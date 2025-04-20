class RepeatedFlagNameException(Exception):
    """
    Private. Raised when a repeated flag name is registered
    """
    def __str__(self):
        return "Repeated registered_flag name in register command"


class TooManyTransferredArgsException(Exception):
    """
    Private. Raised when too many arguments are passed
    """
    def __str__(self):
        return "Too many transferred arguments"


class RequiredArgumentNotPassedException(Exception):
    """
    Private. Raised when a required argument is not passed
    """
    def __str__(self):
        return "Required argument not passed"


class IncorrectNumberOfHandlerArgsException(Exception):
    """
    Private. Raised when incorrect number of arguments are passed
    """
    def __str__(self):
        return "Handler has incorrect number of arguments"


class TriggerCannotContainSpacesException(Exception):
    """
    Private. Raised when there is a space in the trigger being registered
    """
    def __str__(self):
        return "Command trigger cannot contain spaces"
