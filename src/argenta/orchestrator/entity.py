from argparse import Namespace

from argenta.app import App
from argenta.orchestrator.argparser import ArgParser


class Orchestrator:
    def __init__(self, arg_parser: ArgParser | None = None):
        """
        Public. An orchestrator and configurator that defines the behavior of an integrated system, one level higher than the App
        :param arg_parser: Cmd argument parser and configurator at startup
        :return: None
        """
        self._arg_parser: ArgParser | None = arg_parser

    def start_polling(self, app: App) -> None:
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
        if self._arg_parser:
            return self._arg_parser.parse_args()
        else:
            return None
