from argenta import App, Command, Orchestrator, Response, Router
from argenta.a2ui import SSETransport
from argenta.command import Flag

router = Router(title="Main commands")


@router.command(Command("hello", flags=Flag("name"), description="Prints a greeting"))
def hello_handler(response: Response) -> None:
    name = response.input_flags.get_flag_by_name("name")
    print(f"Hello, {name.input_value if name else 'world'}!")


app = App(override_system_messages=True)
app.include_router(router)

if __name__ == "__main__":
    # Same app, different runtime: an SSE server on 127.0.0.1:8765
    Orchestrator().run_agent(app, SSETransport(), verbose=True)
