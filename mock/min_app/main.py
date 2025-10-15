# main.py
from argenta import App, Orchestrator
from .routers import router

app: App = App()
orchestrator: Orchestrator = Orchestrator()

def main() -> None:
    app.include_router(router)
    orchestrator.start_polling(app)

if __name__ == '__main__':
    main()
    