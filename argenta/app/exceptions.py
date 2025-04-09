class InvalidRouterInstanceException(Exception):
    def __str__(self):
        return "Invalid Router Instance"


class NoRegisteredRoutersException(Exception):
    def __str__(self):
        return "No Registered Router Found"


class NoRegisteredHandlersException(Exception):
    def __init__(self, router_name):
        self.router_name = router_name
    def __str__(self):
        return f"No Registered Handlers Found For '{self.router_name}'"
