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


class OnlyOneMainRouterIsAllowedException(Exception):
    def __init__(self, existing_main_router):
        self.existing_main_router = existing_main_router

    def __str__(self):
        return ("Only One Main Router Allowed\n"
                f"Existing main router is: {self.existing_main_router}")


class MissingMainRouterException(Exception):
    def __str__(self):
        return ("Missing Main Router\n"
                "One of the registered routers must be the main one")


class MissingHandlerForUnknownCommandsException(Exception):
    def __str__(self):
        return ("Missing Handlers For Unknown Commands On The Main Router\n"
                "The main router must have a declared handler for unknown commands")


class HandlerForUnknownCommandsOnNonMainRouterException(Exception):
    def __str__(self):
        return '\nThe handler for unknown commands can only be declared for the main router'


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
