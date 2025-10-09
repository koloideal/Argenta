from argparse import ArgumentParser, Namespace

from argenta.orchestrator.argparser.arguments.models import (
    BooleanArgument,
    ValueArgument,
    RequiredArgument,
)


class ArgParser:
    def __init__(
        self,
        processed_args: list[RequiredArgument | ValueArgument | BooleanArgument], *,
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
        self._processed_args: list[RequiredArgument | ValueArgument | BooleanArgument] = processed_args
        
        for arg in processed_args:
            if isinstance(arg, BooleanArgument):
                _ = self._entity.add_argument(arg.string_entity,    
                                            action=arg.action,
                                            help=arg.help,
                                            required=arg.is_required,
                                            deprecated=arg.is_deprecated)
            else:
                _ = self._entity.add_argument(arg.string_entity,    
                                            action=arg.action,
                                            help=arg.help,
                                            default=arg.default,
                                            choices=arg.possible_values,
                                            required=arg.is_required,
                                            deprecated=arg.is_deprecated)

    def parse_args(self) -> Namespace:
        return self._entity.parse_args()
