from argenta.app import App
from argenta.orchestrator.argparse import ArgParse


class Orchestrator:
    def __init__(self, arg_parser: ArgParse):
        """
        An orchestrator and configurator that defines the behavior of an integrated system, one level higher than the App
        :param arg_parser: Cmd argument parser and configurator at startup
        """
        self.arg_parser: ArgParse = arg_parser
        self.arg_parser.register_args()

    @staticmethod
    def start_polling(app: App) -> None:
        """
        Starting the user input processing cycle
        :param app: a running application
        :return:
        """
        app.run_polling()

    def get_args(self):
        """
        Returns the arguments parsed
        :return:
        """
        return self.arg_parser.entity.parse_args()
        