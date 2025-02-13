class InvalidCommandInstanceException(Exception):
    def __str__(self):
        return "Invalid Command Instance"


class InvalidDescriptionInstanceException(Exception):
    def __str__(self):
        return "Invalid Description Instance"


class InvalidFlagsInstanceException(Exception):
    def __str__(self):
        return "Invalid Flags Instance"
