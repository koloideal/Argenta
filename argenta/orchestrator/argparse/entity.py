from argparse import ArgumentParser

from argenta.orchestrator.argparse.arguments.models import (BooleanArgument,
                                                            OptionalArgument,
                                                            PositionalArgument)


class ArgParse:
    def __init__(self, name: str = 'Argenta',
                 description: str = 'Argenta available arguments',
                 epilog: str = 'github.com/koloideal/Argenta | made by kolo',
                 args: list[PositionalArgument | OptionalArgument | BooleanArgument] = None) -> None:
        """
        Cmd argument parser and configurator at startup
        :param name: the name of the ArgParse instance
        :param description: the description of the ArgParse instance
        :param epilog: the epilog of the ArgParse instance
        :param args: registered and processed arguments
        """
        self.name = name
        self.description = description
        self.epilog = epilog

        self.entity = ArgumentParser(prog=name, description=description, epilog=epilog)
        self.args: list[PositionalArgument | OptionalArgument | BooleanArgument] | None = args

    def set_args(self, *args: PositionalArgument | OptionalArgument | BooleanArgument):
        """
        Sets the arguments to be processed
        :param args: processed arguments
        :return:
        """
        self.args.extend(args)

    def register_args(self):
        """
        Registers initialized command line arguments
        :return:
        """
        for arg in self.args:
            if type(arg) is PositionalArgument:
                self.entity.add_argument(arg.get_string_entity())
            elif type(arg) is OptionalArgument:
                self.entity.add_argument(arg.get_string_entity())
            elif type(arg) is BooleanArgument:
                self.entity.add_argument(arg.get_string_entity(), action='store_true')
