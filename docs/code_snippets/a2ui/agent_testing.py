from argenta import App, Command, Response, Router
from argenta.a2ui import AgentRuntime, MemoryTransport
from argenta.a2ui.models import Message


def _kinds(messages: list[Message]) -> list[str]:
    return [next(key for key in message if key != "version") for message in messages]


def _log_texts(messages: list[Message]) -> list[str]:
    texts: list[str] = []
    for message in messages:
        update = message.get("updateDataModel")
        if not isinstance(update, dict) or update.get("path") != "/log":
            continue
        entries = update["value"]
        if isinstance(entries, list):
            texts.extend(str(entry["text"]) for entry in entries if isinstance(entry, dict))
    return texts


def test_agent_dispatches_action() -> None:
    app = App(override_system_messages=True)
    router = Router(title="Main")

    @router.command(Command("hello", description="Prints a greeting"))
    def hello_handler(response: Response) -> None:
        print("hello from the agent")

    app.include_router(router)

    # Script mode: replay two actions — a command, then the exit command
    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "hello", "context": {}}},
            {"action": {"name": "q", "context": {}}},
        ]
    )
    AgentRuntime(app, transport).run()

    assert _kinds(transport.sent)[:3] == ["createSurface", "updateComponents", "updateDataModel"]
    assert _kinds(transport.sent)[-1] == "deleteSurface"
    assert "hello from the agent" in _log_texts(transport.sent)
