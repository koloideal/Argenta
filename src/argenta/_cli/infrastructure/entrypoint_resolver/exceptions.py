class ResolverError(Exception):
    pass


class ResolveFromStringError(ResolverError):
    pass


class EntrypointError(Exception):
    def __init__(self, entrypoint_as_repr: str) -> None:
        self.entrypoint_as_repr = entrypoint_as_repr


class EntrypointNotCallableError(EntrypointError):
    def __str__(self):
        return f"Entrypoint {self.entrypoint_as_repr} is not callable"


class CallableEntrypointNotMatchRequiredSignatureError(EntrypointError):
    def __str__(self) -> str:
        return f"Callable entrypoint {self.entrypoint_as_repr} not match with required signature Callable[[], ...]"


class EntrypointNotAppInstanceError(EntrypointError):
    def __str__(self):
        return f"Entrypoint {self.entrypoint_as_repr} is not instance of App"
