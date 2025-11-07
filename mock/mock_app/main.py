from argenta import App, Orchestrator
from argenta.app import PredefinedMessages
from argenta.app.dividing_line.models import StaticDividingLine, DynamicDividingLine
from mock.mock_app.routers import work_router

app: App = App(
    dividing_line=DynamicDividingLine('^'),
)
orchestrator: Orchestrator = Orchestrator()


def main():
    app.include_router(work_router)

    app.add_message_on_startup(PredefinedMessages.USAGE)
    app.add_message_on_startup(PredefinedMessages.AUTOCOMPLETE)
    app.add_message_on_startup(PredefinedMessages.HELP)

    orchestrator.start_polling(app)


if __name__ == "__main__":
    main()
    
    