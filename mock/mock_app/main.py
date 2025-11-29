from argenta import App, Orchestrator
from argenta.app import PredefinedMessages
from argenta.orchestrator.argparser import ArgParser, BooleanArgument
from argenta.app.dividing_line.models import DynamicDividingLine
from mock.mock_app.routers import work_router

app: App = App(
    dividing_line=DynamicDividingLine('^'),
)
argparser = ArgParser([BooleanArgument('some')])
orchestrator: Orchestrator = Orchestrator(argparser)

print(argparser.parsed_argspace.get_by_type(BooleanArgument))

def main():
    app.include_router(work_router)

    app.add_message_on_startup(PredefinedMessages.USAGE)
    app.add_message_on_startup(PredefinedMessages.AUTOCOMPLETE)
    app.add_message_on_startup(PredefinedMessages.HELP)

    orchestrator.start_polling(app)

if __name__ == "__main__":
    orchestrator.start_polling(app)
    