from mock.mock_app.handlers.routers import work_router, settings_router

from argenta.app import App
from argenta.app.defaults import PredeterminedMessages
from argenta.app.dividing_line import DynamicDividingLine
from argenta.app.autocompleter import AutoCompleter
from argenta.orchestrator import Orchestrator
from argenta.orchestrator.argparse import ArgParse
from argenta.orchestrator.argparse.arguments import (PositionalArgument,
                                                     OptionalArgument,
                                                     BooleanArgument)


arg_parser = ArgParse(args=[PositionalArgument('test'), OptionalArgument('some'), BooleanArgument('verbose')])
app: App = App(dividing_line=DynamicDividingLine(),
               autocompleter=AutoCompleter('./mock/.hist'))
orchestrator: Orchestrator = Orchestrator(arg_parser)


def main():
    app.include_routers(work_router, settings_router)

    app.add_message_on_startup(PredeterminedMessages.USAGE)
    app.add_message_on_startup(PredeterminedMessages.AUTOCOMPLETE)
    app.add_message_on_startup(PredeterminedMessages.HELP)

    print(orchestrator.get_args())
    #orchestrator.start_polling(app)

if __name__ == "__main__":
    main()
