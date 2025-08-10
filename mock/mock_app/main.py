from mock.mock_app.routers import work_router

from argenta import App, Orchestrator
from argenta.app import PredefinedMessages, DynamicDividingLine, AutoCompleter
from argenta.orchestrator import ArgParser
from argenta.orchestrator.argparser import BooleanArgument


arg_parser = ArgParser(processed_args=[BooleanArgument("repeat")])
app: App = App(
    dividing_line=DynamicDividingLine(),
    autocompleter=AutoCompleter(),
    repeat_command_groups=False,
)
orchestrator: Orchestrator = Orchestrator(arg_parser)


def main():
    app.include_router(work_router)

    app.add_message_on_startup(PredefinedMessages.USAGE)
    app.add_message_on_startup(PredefinedMessages.AUTOCOMPLETE)
    app.add_message_on_startup(PredefinedMessages.HELP)

    orchestrator.start_polling(app)


if __name__ == "__main__":
    main()
