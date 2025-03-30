from argenta.router import Router


class RegisteredRouters:
    def __init__(self, registered_routers: list[Router] = None) -> None:
        self._registered_routers = registered_routers if registered_routers else []

    def get_registered_routers(self) -> list[Router]:
        return self._registered_routers

    def add_registered_router(self, router: Router):
        self._registered_routers.append(router)

    def add_registered_routers(self, *routers: Router):
        self._registered_routers.extend(routers)

    def __iter__(self):
        return iter(self._registered_routers)

    def __next__(self):
        return next(iter(self._registered_routers))