from argparse import Namespace

from argenta.app import App
from argenta.orchestrator.argparser import ArgParser


class Orchestrator:
    def __init__(self, arg_parser: ArgParser = False):
        """
        Public. An orchestrator and configurator that defines the behavior of an integrated system, one level higher than the App
        :param arg_parser: Cmd argument parser and configurator at startup
        :return: None
        """
        self.arg_parser: ArgParser | False = arg_parser
        if arg_parser:
            self.arg_parser.register_args()

    @staticmethod
    def start_polling(app: App) -> None:
        """
        Public. Starting the user input processing cycle
        :param app: a running application
        :return: None
        """
        app.run_polling()

    def get_input_args(self) -> Namespace | None:
        """
        Public. Returns the arguments parsed
        :return: None
        """
        if self.arg_parser:
            return self.arg_parser.entity.parse_args()
        else:
            return None
