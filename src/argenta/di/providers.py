__all__ = [
    'SystemProvider',
]

from dishka import Provider, Scope, provide

from argenta.orchestrator.argparser import ArgParser
from argenta.orchestrator.argparser.entity import ArgSpace


class SystemProvider(Provider):
    def __init__(self, arg_parser: ArgParser):
        super().__init__()
        self._arg_parser: ArgParser = arg_parser

    @provide(scope=Scope.APP)
    def get_argspace(self) -> ArgSpace:
        return self._arg_parser.parsed_argspace
