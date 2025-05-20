from typing import Iterator

from argenta.router import Router


class RegisteredRouters:
    def __init__(self, registered_routers: list[Router] | None = None) -> None:
        """
        Private. Combines registered routers
        :param registered_routers: list of the registered routers
        :return: None
        """
        self._registered_routers = registered_routers if registered_routers else []

    def get_registered_routers(self) -> list[Router]:
        """
        Private. Returns the registered routers
        :return: registered routers as list[Router]
        """
        return self._registered_routers

    def add_registered_router(self, router: Router) -> None:
        """
        Private. Adds a new registered router
        :param router: registered router
        :return: None
        """
        self._registered_routers.append(router)

    def __iter__(self) -> Iterator[Router]:
        return iter(self._registered_routers)

    def __next__(self) -> Router:
        return next(iter(self._registered_routers))
