__all__ = [
    "SystemProvider",
]

from dishka import Provider, Scope, provide

from argenta.data_bridge import DataBridge
from argenta.orchestrator.argparser import ArgParser
from argenta.orchestrator.argparser.entity import ArgSpace


class SystemProvider(Provider):
    @provide(scope=Scope.APP)
    def get_argspace(self, arg_parser: ArgParser) -> ArgSpace:
        return arg_parser.parsed_argspace

    @provide(scope=Scope.APP)
    def get_data_bridge(self) -> DataBridge:
        return DataBridge()
