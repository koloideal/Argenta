from argenta import App, Command, Orchestrator, Response, Router

router = Router(title="Example")

@router.command(Command("hello", description="Say hello"))
def hello_handler(response: Response):
    print("Hello, world!")


def create_app() -> App:
    app = App()
    app.include_router(router)
    return app


def main() -> None:
    orchestrator = Orchestrator()
    orchestrator.run_repl(create_app())

if __name__ == "__main__":
    main()
