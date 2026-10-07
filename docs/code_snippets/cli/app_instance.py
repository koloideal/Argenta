from argenta import App, Command, Orchestrator, Response, Router

router = Router(title="Example")

@router.command(Command("hello", description="Say hello"))
def hello_handler(response: Response):
    print("Hello, world!")

app = App()
app.include_router(router)

orchestrator = Orchestrator()

if __name__ == "__main__":
    orchestrator.run_repl(app)
