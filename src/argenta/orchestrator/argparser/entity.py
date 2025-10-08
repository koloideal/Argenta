from argparse import ArgumentParser, Namespace

from argenta.orchestrator.argparser.arguments.models import (
    BooleanArgument,
    OptionalArgument,
    PositionalArgument,
)


class ArgParser:
    def __init__(
        self,
        processed_args: list[PositionalArgument | OptionalArgument | BooleanArgument], *,
        name: str = "Argenta",
        description: str = "Argenta available arguments",
        epilog: str = "github.com/koloideal/Argenta | made by kolo",
    ) -> None:
        """
        Public. Cmd argument parser and configurator at startup
        :param name: the name of the ArgParse instance
        :param description: the description of the ArgParse instance
        :param epilog: the epilog of the ArgParse instance
        :param processed_args: registered and processed arguments
        """
        self._name: str = name
        self._description: str = description
        self._epilog: str = epilog

        self._entity: ArgumentParser = ArgumentParser(prog=name, description=description, epilog=epilog)
        self._processed_args: list[PositionalArgument | OptionalArgument | BooleanArgument] = processed_args
        
        for arg in processed_args:
            if isinstance(arg, PositionalArgument) or isinstance(arg, OptionalArgument):
                _ = self._entity.add_argument(arg.string_entity)
            else: 
                _ = self._entity.add_argument(arg.string_entity, action="store_true")

    def parse_args(self) -> Namespace:
        return self._entity.parse_args()
