class InvalidRouterInstanceException(Exception):
    def __str__(self):
        return "Invalid Router Instance"


class InvalidDescriptionMessagePatternException(Exception):
    def __init__(self, pattern: str):
        self.pattern = pattern
    def __str__(self):
        return ("Invalid Description Message Pattern\n"
                "Correct pattern example: [{command}] *=*=* {description}\n"
                "The pattern must contain two variables: `command` and `description` - description of the command\n"
                f"Your pattern: {self.pattern}")


class NoRegisteredRoutersException(Exception):
    def __str__(self):
        return "No Registered Router Found"


class NoRegisteredHandlersException(Exception):
    def __init__(self, router_name):
        self.router_name = router_name
    def __str__(self):
        return f"No Registered Handlers Found For '{self.router_name}'"


class RepeatedCommandInDifferentRoutersException(Exception):
    def __str__(self):
        return "Commands in different handlers cannot be repeated"


class IncorrectNumberOfHandlerArgsException(Exception):
    def __str__(self):
        return "Incorrect Input Flags Handler has incorrect number of arguments"
