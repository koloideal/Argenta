__all__ = ["RegisteredRouters"]

from typing import Iterator, Optional

from argenta.router import Router


class RegisteredRouters:
    def __init__(self, registered_routers: Optional[list[Router]] = None) -> None:
        """
        Private. Combines registered routers
        :param registered_routers: list of the registered routers
        :return: None
        """
        self.registered_routers: list[Router] = registered_routers if registered_routers else []

    def add_registered_router(self, router: Router, /) -> None:
        """
        Private. Adds a new registered router
        :param router: registered router
        :return: None
        """
        self.registered_routers.append(router)

    def __iter__(self) -> Iterator[Router]:
        return iter(self.registered_routers)

    def __next__(self) -> Router:
        return next(iter(self.registered_routers))
