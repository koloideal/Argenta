# main.py
from argenta import App, Orchestrator
from argenta.app import DynamicDividingLine

from .routers import router

app: App = App(prompt='>>> ', dividing_line=DynamicDividingLine('~'))
orchestrator: Orchestrator = Orchestrator()

def main() -> None:
    app.include_router(router)
    orchestrator.start_polling(app)

if __name__ == '__main__':
    main()
    