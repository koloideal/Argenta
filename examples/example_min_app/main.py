from argenta import App, Orchestrator
from examples.example_min_app.routers import router

app: App = App(prompt=">>> ")
orchestrator: Orchestrator = Orchestrator()


def main() -> None:
    app.include_router(router)
    orchestrator.run_repl(app)


if __name__ == "__main__":
    main()
