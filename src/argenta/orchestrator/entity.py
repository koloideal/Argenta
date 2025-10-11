from argenta.app import App
from argenta.orchestrator.argparser import ArgParser
from argenta.orchestrator.argparser.entity import ArgSpace


DEFAULT_ARGPARSER: ArgParser = ArgParser(processed_args=[])


class Orchestrator:
    def __init__(self, arg_parser: ArgParser = DEFAULT_ARGPARSER):
        """
        Public. An orchestrator and configurator that defines the behavior of an integrated system, one level higher than the App
        :param arg_parser: Cmd argument parser and configurator at startup
        :return: None
        """
        self._arg_parser: ArgParser = arg_parser

    def start_polling(self, app: App) -> None:
        """
        Public. Starting the user input processing cycle
        :param app: a running application
        :return: None
        """
        parsed_argspace: ArgSpace = self._arg_parser.parse_args()
        app.run_polling(argspace=parsed_argspace)
