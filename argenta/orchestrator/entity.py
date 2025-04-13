from argparse import ArgumentParser

from argenta.app import App
from argenta.orchestrator.argparse.arguments import (PositionalArgument,
                                                     OptionalArgument,
                                                     BooleanArgument)


class Orchestrator:
    def __init__(self, *args: PositionalArgument | OptionalArgument | BooleanArgument):
        """
        An orchestrator and configurator that defines the behavior of an integrated system, one level higher than the App
        :param args: logged command line arguments at startup
        """
        self.args = args
        self.argparse: ArgumentParser = ArgumentParser()
        self._register_args()

    @staticmethod
    def start_polling(app: App) -> None:
        """
        Starting the user input processing cycle
        :param app: a running application
        :return:
        """
        app.run_polling()

    def get_args(self):
        return self.argparse.parse_args()

    def _register_args(self):
        """
        Registers initialized command line arguments
        :return:
        """
        for arg in self.args:
            if type(arg) is PositionalArgument:
                self.argparse.add_argument(arg.get_string_entity())
            elif type(arg) is OptionalArgument:
                self.argparse.add_argument(arg.get_string_entity())
            elif type(arg) is BooleanArgument:
                self.argparse.add_argument(arg.get_string_entity(), action='store_const')
        