from argenta import App, Orchestrator
from .handlers import router


app = App(initial_message="metrics")
orchestrator = Orchestrator()


def main() -> None:
    app.include_router(router)
    orchestrator.start_polling(app)


if __name__ == "__main__":
    main()
