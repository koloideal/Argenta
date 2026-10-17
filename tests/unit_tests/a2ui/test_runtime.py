from collections.abc import Iterator

import pytest
from pytest_mock import MockerFixture

from argenta import App, Command, Response, Router
from argenta.a2ui import AgentRuntime, MemoryTransport
from argenta.a2ui.models import A2UIConfig, Message
from argenta.a2ui.runtime import _find_command
from argenta.command.flag import Flag, Flags, PossibleValues


def _log_updates(transport: MemoryTransport) -> list[str]:
    logs: list[str] = []
    for message in transport.sent:
        update = message.get("updateDataModel")
        if not isinstance(update, dict):
            continue
        value = update.get("value")
        if update.get("path") == A2UIConfig().log_model_path and isinstance(value, str):
            logs.append(value)
    return logs


def _kinds(transport: MemoryTransport) -> list[str]:
    return [next(key for key in message if key != "version") for message in transport.sent]


def _app_with(handler=None) -> App:
    app = App()
    router = Router(title="Main")
    router.command("hello")(handler or (lambda _response: None))
    app.include_router(router)
    return app


def _section(message: Message, key: str) -> Message:
    value = message[key]
    assert isinstance(value, dict)
    return value


def test_run_emits_initial_messages_and_cleanup() -> None:
    app = _app_with()
    transport = MemoryTransport(incoming=[{"action": {"name": "q", "context": {}}}])

    AgentRuntime(app, transport).run()

    kinds = _kinds(transport)
    assert kinds[0] == "createSurface"
    assert _section(transport.sent[0], "createSurface")["surfaceId"] == "main"
    assert kinds[1] == "updateComponents"
    assert kinds[2] == "updateDataModel"
    assert kinds[-1] == "deleteSurface"
    assert _section(transport.sent[-1], "deleteSurface") == {"surfaceId": "main"}


def test_verbose_reports_lifecycle_to_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    app = _app_with()
    transport = MemoryTransport(incoming=[{"action": {"name": "q", "context": {}}}])

    AgentRuntime(app, transport, verbose=True).run()

    err = capsys.readouterr().err
    assert "[agent]" in err
    assert "surface 'main' emitted" in err
    assert "action 'q' received" in err
    assert "action 'q' dispatched" in err
    assert "surface deleted, shutting down" in err


def test_quiet_by_default(capsys: pytest.CaptureFixture[str]) -> None:
    app = _app_with()
    transport = MemoryTransport(incoming=[{"action": {"name": "q", "context": {}}}])

    AgentRuntime(app, transport).run()

    err = capsys.readouterr().err
    assert "surface deleted, shutting down" in err
    assert "received" not in err


def test_keyboard_interrupt_graceful_shutdown(capsys: pytest.CaptureFixture[str]) -> None:
    class _InterruptingTransport(MemoryTransport):
        def actions(self) -> Iterator[Message]:
            yield {"action": {"name": "hello", "context": {}}}
            raise KeyboardInterrupt

    app = _app_with()
    transport = _InterruptingTransport()

    AgentRuntime(app, transport).run()

    assert _kinds(transport)[-1] == "deleteSurface"
    assert "interrupted" in capsys.readouterr().err


def test_run_sends_initial_message_to_log() -> None:
    app = App(override_system_messages=True, initial_message="Welcome banner", printer=print)
    transport = MemoryTransport(incoming=[{"action": {"name": "q", "context": {}}}])

    AgentRuntime(app, transport).run()

    assert "Welcome banner" in _log_updates(transport)[0]


def test_action_dispatches_and_captures_output() -> None:
    def handler(_response: Response) -> None:
        print("handler output")

    app = _app_with(handler)
    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "hello", "context": {}}},
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    logs = _log_updates(transport)
    assert any("handler output" in log for log in logs)


def test_context_becomes_flags() -> None:
    captured: list[tuple[object, bool]] = []

    def handler(response: Response) -> None:
        env = response.input_flags.get_flag_by_name("env")
        force = response.input_flags.get_flag_by_name("force")
        captured.append((env.input_value if env else None, force is not None))

    app = App()
    router = Router()
    router.command(
        Command(
            "deploy",
            flags=Flags(
                [
                    Flag("env", possible_values=["prod", "dev"]),
                    Flag("force", possible_values=PossibleValues.NEITHER),
                ]
            ),
        )
    )(handler)
    app.include_router(router)

    transport = MemoryTransport(
        incoming=[
            {
                "action": {
                    "name": "deploy",
                    "context": {"env": "prod", "force": True, "extra": {"nested": "dict"}},
                }
            },
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    assert captured == [("prod", True)]


def test_list_context_value_unwrapped() -> None:
    captured: list[str | None] = []

    def handler(response: Response) -> None:
        env = response.input_flags.get_flag_by_name("env")
        captured.append(env.input_value if env else None)

    app = App()
    router = Router()
    router.command(Command("deploy", flags=Flags([Flag("env", possible_values=["prod", "dev"])])))(
        handler
    )
    app.include_router(router)

    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "deploy", "context": {"env": ["prod"]}}},
            {"action": {"name": "deploy", "context": {"env": []}}},
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    assert captured == ["prod", None]


def test_transport_closed_after_run() -> None:
    class _SpyTransport(MemoryTransport):
        def __init__(self) -> None:
            super().__init__(incoming=[])
            self.closed = False

        def close(self) -> None:
            self.closed = True

    app = _app_with()
    transport = _SpyTransport()

    AgentRuntime(app, transport).run()

    assert transport.closed


def test_transport_closed_when_stream_raises() -> None:
    class _BrokenTransport(MemoryTransport):
        def __init__(self) -> None:
            super().__init__()
            self.closed = False

        def actions(self) -> Iterator[Message]:
            raise RuntimeError("stream died")

        def close(self) -> None:
            self.closed = True

    app = _app_with()
    transport = _BrokenTransport()

    with pytest.raises(RuntimeError, match="stream died"):
        AgentRuntime(app, transport).run()

    assert transport.closed


def test_checkbox_false_skips_flag() -> None:
    captured: list[bool] = []

    def handler(response: Response) -> None:
        captured.append(response.input_flags.get_flag_by_name("force") is not None)

    app = App()
    router = Router()
    router.command(
        Command("run", flags=Flags([Flag("force", possible_values=PossibleValues.NEITHER)]))
    )(handler)
    app.include_router(router)

    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "run", "context": {"force": False}}},
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    assert captured == [False]


def test_empty_context_value_skips_flag() -> None:
    captured: list[int] = []

    def handler(response: Response) -> None:
        captured.append(len(response.input_flags.flags))

    app = App()
    router = Router()
    router.command(Command("c", flags=Flags([Flag("f", possible_values=PossibleValues.ALL)])))(
        handler
    )
    app.include_router(router)

    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "c", "context": {"f": ""}}},
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    assert captured == [0]


def test_unknown_command_action_logged() -> None:
    app = _app_with()
    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "bogus", "context": {}}},
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    logs = _log_updates(transport)
    assert any("Unknown command" in log for log in logs)


def test_alias_dispatch() -> None:
    seen: list[bool] = []

    def handler(_response: Response) -> None:
        seen.append(True)

    app = App()
    router = Router()
    router.command(Command("deploy", aliases={"dep"}))(handler)
    app.include_router(router)

    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "dep", "context": {}}},
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    assert seen == [True]


def test_non_action_messages_ignored() -> None:
    app = _app_with()
    transport = MemoryTransport(
        incoming=[
            {"error": {"code": 3, "message": "client error"}},
            {"somethingElse": {}},
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    assert _kinds(transport)[-1] == "deleteSurface"


def test_malformed_action_ignored() -> None:
    app = _app_with()
    transport = MemoryTransport(
        incoming=[
            {"action": {"context": {}}},
            {"action": "not-a-dict"},
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    assert _kinds(transport)[-1] == "deleteSurface"


def test_handler_without_output_does_not_send_log() -> None:
    app = _app_with()
    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "hello", "context": {}}},
            {"action": {"name": "q", "context": {}}},
        ]
    )
    runtime = AgentRuntime(app, transport)

    runtime.run()

    assert len(_log_updates(transport)) == 2


def test_log_flush_emits_full_buffer() -> None:
    def handler(_response: Response) -> None:
        for index in range(30):
            print(f"line{index}")

    app = _app_with(handler)
    transport = MemoryTransport(incoming=[{"action": {"name": "hello", "context": {}}}])

    AgentRuntime(app, transport).run()

    last_log = _log_updates(transport)[-1]
    assert "line0" in last_log
    assert "line29" in last_log


def test_log_capped_at_max_lines() -> None:
    def handler(_response: Response) -> None:
        for index in range(600):
            print(f"line{index}")

    app = _app_with(handler)
    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "hello", "context": {}}},
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    last_log = _log_updates(transport)[-1]
    assert len(last_log.split("\n")) <= 700
    assert "line0" not in last_log


def test_exit_action_breaks_loop() -> None:
    app = _app_with()
    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "q", "context": {}}},
            {"action": {"name": "hello", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    logs = _log_updates(transport)
    assert not any("hello output" in log for log in logs)


def test_delete_surface_on_stream_end() -> None:
    app = _app_with()
    transport = MemoryTransport(incoming=[])

    AgentRuntime(app, transport).run()

    assert _kinds(transport)[-1] == "deleteSurface"


def test_handler_exception_logged_and_loop_continues() -> None:
    def handler(_response: Response) -> None:
        raise RuntimeError("boom")

    app = _app_with(handler)
    transport = MemoryTransport(
        incoming=[
            {"action": {"name": "hello", "context": {}}},
            {"action": {"name": "q", "context": {}}},
        ]
    )

    AgentRuntime(app, transport).run()

    logs = _log_updates(transport)
    assert any("RuntimeError" in log for log in logs)
    assert _kinds(transport)[-1] == "deleteSurface"


def test_command_lookup_returns_none_without_handler(mocker: MockerFixture) -> None:
    app = _app_with()
    router = app.registered_routers.get_router_by_trigger("hello")
    assert router is not None
    mocker.patch.object(
        router.command_handlers, "get_command_handler_by_trigger", return_value=None
    )

    assert _find_command(app, "hello") is None


def test_protocol_version_pinned() -> None:
    app = _app_with()
    transport = MemoryTransport(incoming=[])

    AgentRuntime(app, transport).run()

    assert all(message["version"] == A2UIConfig().protocol_version for message in transport.sent)


def test_theme_propagated_to_create_surface() -> None:
    app = _app_with()
    transport = MemoryTransport(incoming=[])

    AgentRuntime(
        app,
        transport,
        A2UIConfig(surface_id="ui2", theme={"primaryColor": "#7C4DFF"}),
    ).run()

    surface = _section(transport.sent[0], "createSurface")
    assert surface["surfaceId"] == "ui2"
    assert surface["theme"] == {"primaryColor": "#7C4DFF"}
