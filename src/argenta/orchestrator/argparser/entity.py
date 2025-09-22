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
        self._name = name
        self._description = description
        self._epilog = epilog

        self._entity: ArgumentParser = ArgumentParser(prog=name, description=description, epilog=epilog)
        self._args: list[PositionalArgument | OptionalArgument | BooleanArgument] = processed_args

    def set_args(
        self, args: list[PositionalArgument | OptionalArgument | BooleanArgument]
    ) -> None:
        """
        Public. Sets the arguments to be processed
        :param args: processed arguments
        :return: None
        """
        self._args.extend(args)

    def register_args(self) -> None:
        """
        Private. Registers initialized command line arguments
        :return: None
        """
        for arg in self._args:
            if isinstance(arg, PositionalArgument):
                self._entity.add_argument(arg.get_string_entity())
            elif isinstance(arg, OptionalArgument):
                self._entity.add_argument(arg.get_string_entity())
            elif isinstance(arg, BooleanArgument): # pyright: ignore[reportUnnecessaryIsInstance]
                self._entity.add_argument(arg.get_string_entity(), action="store_true")
            else:
                raise NotImplementedError()

    def parse_args(self) -> Namespace:
        return self._entity.parse_args()
