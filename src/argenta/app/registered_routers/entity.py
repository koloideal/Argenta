__all__ = ["RegisteredRouters"]

from typing import Iterator

from argenta.router import Router


class RegisteredRouters:
    def __init__(self) -> None:
        """
        Private. Combines registered routers
        :param registered_routers: list of the registered routers
        :return: None
        """
        self.registered_routers: list[Router] = []
        self._paired_trigger_router: dict[str, Router] = {}

    def add_registered_router(self, router: Router, /) -> None:
        """
        Private. Adds a new registered router
        :param router: registered router
        :return: None
        """
        self.registered_routers.append(router)
        for trigger in (router.aliases | router.triggers):
            self._paired_trigger_router[trigger] = router
            
    def get_router_by_trigger(self, trigger: str) -> Router | None:
        return self._paired_trigger_router.get(trigger)
        
    def get_triggers(self) -> set[str]:
        return set(self._paired_trigger_router.keys())
        
    def __iter__(self) -> Iterator[Router]:
        return iter(self.registered_routers)
