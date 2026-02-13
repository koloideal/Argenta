# main.py
from .routers import router

from argenta import App, Orchestrator

app: App = App()
orchestrator: Orchestrator = Orchestrator()


def main() -> None:
    app.include_router(router)
    orchestrator.run_repl(app)


if __name__ == "__main__":
    main()
