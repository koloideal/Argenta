from argenta import App, Orchestrator
from argenta.app import StaticDividingLine

from .handlers import router

app = App(initial_message="metrics", prompt=">>> ", dividing_line=StaticDividingLine('~', length=70))
orchestrator = Orchestrator()


def main() -> None:
    app.include_router(router)
    orchestrator.start_polling(app)


if __name__ == "__main__":
    main()
