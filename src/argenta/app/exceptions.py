class NoRegisteredHandlersException(Exception):
    """
    The router has no registered handlers
    """
    def __init__(self, router_name) -> None:
        self.router_name = router_name
    def __str__(self):
        return f"No Registered Handlers Found For '{self.router_name}'"
