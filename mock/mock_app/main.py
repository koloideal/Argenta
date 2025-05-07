from mock.mock_app.handlers.routers import work_router

from argenta.app import App
from argenta.app.defaults import PredefinedMessages
from argenta.app.dividing_line import DynamicDividingLine
from argenta.app.autocompleter import AutoCompleter
from argenta.orchestrator import Orchestrator
from argenta.orchestrator.argparser import ArgParser
from argenta.orchestrator.argparser.arguments import BooleanArgument


arg_parser = ArgParser(processed_args=[BooleanArgument('repeat')])
app: App = App(dividing_line=DynamicDividingLine(),
               autocompleter=AutoCompleter(),
               repeat_command_groups=False,)
orchestrator: Orchestrator = Orchestrator(arg_parser)


def main():
    app.include_router(work_router)

    app.add_message_on_startup(PredefinedMessages.USAGE)
    app.add_message_on_startup(PredefinedMessages.AUTOCOMPLETE)
    app.add_message_on_startup(PredefinedMessages.HELP)

    orchestrator.start_polling(app)

if __name__ == "__main__":
    main()
