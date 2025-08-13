from argparse import Namespace
from typing import Optional

from argenta.app import App
from argenta.orchestrator.argparser import ArgParser


class Orchestrator:
    def __init__(self, arg_parser: Optional[ArgParser] = None):
        """
        Public. An orchestrator and configurator that defines the behavior of an integrated system, one level higher than the App
        :param arg_parser: Cmd argument parser and configurator at startup
        :return: None
        """
        self._arg_parser: Optional[ArgParser] = arg_parser

    def start_polling(self, app: App) -> None:
        """
        Public. Starting the user input processing cycle
        :param app: a running application
        :return: None
        """
        if self._arg_parser:
            self._arg_parser.register_args()
        app.run_polling()

    def get_input_args(self) -> Optional[Namespace]:
        """
        Public. Returns the arguments parsed
        :return: None
        """
        if self._arg_parser:
            return self._arg_parser.parse_args()
        else:
            return None
