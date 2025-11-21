__all__ = [
    "ArgSpace",
    "ArgParser",
]

from argparse import ArgumentParser, Namespace
from typing import Never, Self

from argenta.orchestrator.argparser.arguments.models import (
    BaseArgument,
    BooleanArgument,
    InputArgument,
    ValueArgument,
)


class ArgSpace:
    def __init__(self, all_arguments: list[InputArgument]) -> None:
        self.all_arguments = all_arguments

    @classmethod
    def from_namespace(
        cls, namespace: Namespace, processed_args: list[ValueArgument | BooleanArgument]
    ) -> Self:
        name_type_paired_args: dict[str, type[BaseArgument]] = {arg.name: type(arg) for arg in processed_args}
        return cls(
            [
                InputArgument(name=name, value=value, founder_class=name_type_paired_args[name])
                for name, value in vars(namespace).items()
            ]
        )

    def get_by_name(self, name: str) -> InputArgument | None:
        for arg in self.all_arguments:
            if arg.name == name:
                return arg
        return None

    def get_by_type(self, arg_type: type[BaseArgument]) -> list[InputArgument] | list[Never]:
        return [arg for arg in self.all_arguments if arg.founder_class is arg_type]


class ArgParser:
    def __init__(
        self,
        processed_args: list[ValueArgument | BooleanArgument],
        *,
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
        self.name: str = name
        self.description: str = description
        self.epilog: str = epilog
        self.processed_args: list[ValueArgument | BooleanArgument] = processed_args

        self.parsed_argspace: ArgSpace = ArgSpace([])

        self._core: ArgumentParser = ArgumentParser(prog=name, description=description, epilog=epilog)
        self._register_args(processed_args)

    def _parse_args(self) -> None:
        self.parsed_argspace = ArgSpace.from_namespace(
            namespace=self._core.parse_args(), processed_args=self.processed_args
        )

    def _register_args(self, processed_args: list[ValueArgument | BooleanArgument]) -> None:
        for arg in processed_args:
            if isinstance(arg, BooleanArgument):
                _ = self._core.add_argument(
                    arg.string_entity, action=arg.action, help=arg.help, deprecated=arg.is_deprecated
                )
            else:
                _ = self._core.add_argument(
                    arg.string_entity,
                    action=arg.action,
                    help=arg.help,
                    default=arg.default,
                    choices=arg.possible_values,
                    required=arg.is_required,
                    deprecated=arg.is_deprecated,
                )
