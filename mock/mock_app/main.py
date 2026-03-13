from prompt_toolkit import HTML

from argenta import App, Orchestrator
from argenta.app import PredefinedMessages, StaticDividingLine, AutoCompleter
from argenta.app.dividing_line.models import DynamicDividingLine
from argenta.orchestrator import ArgParser
from mock.mock_app.routers import work_router

app: App = App(
    dividing_line=StaticDividingLine('~')
)
orchestrator: Orchestrator = Orchestrator(arg_parser=ArgParser(processed_args=[]))


def main():
    app.include_router(work_router)

    app.add_message_on_startup(PredefinedMessages.USAGE)
    app.add_message_on_startup(PredefinedMessages.AUTOCOMPLETE)
    app.add_message_on_startup(PredefinedMessages.HELP)

    orchestrator.run_repl(app)

if __name__ == "__main__":
    main()
    