from argenta import App, Orchestrator
from argenta.app import PredefinedMessages
from argenta.repl import DynamicDividingLine, REPLConfig
from examples.repl.app.routers import work_router

app: App = App()
orchestrator: Orchestrator = Orchestrator()


def main() -> None:
    app.include_router(work_router)

    app.add_message_on_startup(PredefinedMessages.USAGE)
    app.add_message_on_startup(PredefinedMessages.AUTOCOMPLETE)
    app.add_message_on_startup(PredefinedMessages.HELP)

    orchestrator.run_repl(app, REPLConfig(dividing_line=DynamicDividingLine("~")))


if __name__ == "__main__":
    main()
