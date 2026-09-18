from argenta import App, Orchestrator
from argenta.command import Router, Command, Response

router = Router(title="Example")

@router.command(Command("hello", description="Say hello"))
def hello_handler(response: Response):
    print("Hello, world!")

app = App()
app.include_router(router)

orchestrator = Orchestrator()

if __name__ == "__main__":
    orchestrator.run_repl(app)
