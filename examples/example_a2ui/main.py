from argenta import App, Orchestrator
from argenta.app import PredefinedMessages, StaticDividingLine
from examples.example_a2ui.routers import release_router

app: App = App(dividing_line=StaticDividingLine("~"))
orchestrator: Orchestrator = Orchestrator()


def main() -> None:
    app.include_router(release_router)
    app.add_message_on_startup(PredefinedMessages.HELP)
    orchestrator.run_repl(app)


if __name__ == "__main__":
    main()
