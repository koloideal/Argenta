__all__ = [
    "ArgSpace",
    "ArgParser",
]

import sys
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

        self._name_object_paired_args: dict[str, InputArgument] = {}
        self._type_object_paired_args: dict[type[BaseArgument], list[InputArgument]] = {
            BooleanArgument: [],
            ValueArgument: []
        }

        self._setup_getters()

    @classmethod
    def from_namespace(
        cls,
        namespace: Namespace,
        processed_args: list[ValueArgument | BooleanArgument]
    ) -> Self:
        name_type_paired_processed_args: dict[str, type[BaseArgument]] = {
            arg.name: type(arg) for arg in processed_args
        }
        parsed_arguments: list[InputArgument] = []

        for name, value in vars(namespace).items():
            parsed_arguments.append(
                InputArgument(
                    name=name,
                    value=value,
                    founder_class=name_type_paired_processed_args[name]
                )
            )

        return cls(parsed_arguments)

    def _setup_getters(self) -> None:
        if not self.all_arguments:
            return
        for input_arg in self.all_arguments:
            self._name_object_paired_args[input_arg.name] = input_arg
            self._type_object_paired_args[input_arg.founder_class].append(input_arg)

    def get_by_name(self, name: str) -> InputArgument | None:
        return self._name_object_paired_args.get(name)

    def get_by_type(self, arg_type: type[BaseArgument]) -> list[InputArgument] | list[Never]:
        return self._type_object_paired_args.get(arg_type, [])


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
        if sys.version_info >= (3, 13):
            for arg in processed_args:
                if isinstance(arg, BooleanArgument):
                    _ = self._core.add_argument(
                        arg.string_entity,
                        action=arg.action,
                        help=arg.help,
                        deprecated=arg.is_deprecated
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
        else:
            for arg in processed_args:
                if isinstance(arg, BooleanArgument):
                    _ = self._core.add_argument(
                        arg.string_entity,
                        action=arg.action,
                        help=arg.help,
                    )
                else:
                    _ = self._core.add_argument(
                        arg.string_entity,
                        action=arg.action,
                        help=arg.help,
                        default=arg.default,
                        choices=arg.possible_values,
                        required=arg.is_required
                    )
                
