import asyncio
from collections.abc import Iterable
from pathlib import Path
from threading import Event
from unittest.mock import patch

import pytest
from prompt_toolkit import PromptSession
from prompt_toolkit.application import create_app_session
from prompt_toolkit.completion import CompleteEvent, ThreadedCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.history import FileHistory, History, InMemoryHistory, ThreadedHistory
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

from argenta.app.autocompleter._ext_features_impl import HistoryCompleter


def _completions(completer: HistoryCompleter, prefix: str = "") -> list[str]:
    return [
        completion.text
        for completion in completer.get_completions(Document(prefix), CompleteEvent())
    ]


async def _load_history(history: History) -> None:
    async for _ in history.load():
        pass


def test_completion_does_not_load_file_history(tmp_path: Path) -> None:
    filename = tmp_path / "history"
    FileHistory(filename).append_string("restart server")
    history = FileHistory(filename)
    completer = HistoryCompleter(history, {"status"})

    with patch.object(history, "load_history_strings", wraps=history.load_history_strings) as load:
        assert _completions(completer) == ["status"]
        load.assert_not_called()

        asyncio.run(_load_history(history))
        assert _completions(completer) == ["restart server", "status"]
        assert _completions(completer, "re") == ["restart server"]
        load.assert_called_once()

        history.append_string("reload config")
        assert _completions(completer, "re") == ["reload config", "restart server"]
        load.assert_called_once()


def test_completion_invalidates_same_length_history_snapshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshot = ["restart server"]
    history = InMemoryHistory()
    monkeypatch.setattr(history, "get_strings", lambda: snapshot.copy())
    completer = HistoryCompleter(history, {"status"})

    assert _completions(completer) == ["restart server", "status"]

    snapshot[:] = ["reload config"]
    assert _completions(completer) == ["reload config", "status"]


@pytest.mark.parametrize("file_history", [False, True], ids=["memory", "threaded-file"])
def test_prompt_session_loads_history_for_completion(tmp_path: Path, file_history: bool) -> None:
    filename = tmp_path / "history"
    FileHistory(filename).append_string("restart server")
    backend = FileHistory(filename)
    history = ThreadedHistory(backend) if file_history else InMemoryHistory(["restart server"])
    completer = HistoryCompleter(history, {"status"})

    async def run_session() -> None:
        with (
            create_pipe_input() as input_pipe,
            create_app_session(input=input_pipe, output=DummyOutput()),
        ):
            session: PromptSession[str] = PromptSession(
                history=history, completer=ThreadedCompleter(completer)
            )
            prompt = asyncio.create_task(session.prompt_async())
            try:
                while "restart server" not in history.get_strings():
                    await asyncio.sleep(0.01)
                assert _completions(completer, "re") == ["restart server"]
                assert _completions(completer, "re") == ["restart server"]
                history.append_string("reload config")
                assert _completions(completer, "re") == ["reload config", "restart server"]

                input_pipe.send_text("exit\n")
                assert await prompt == "exit"
            finally:
                if not prompt.done():
                    prompt.cancel()
                    await asyncio.gather(prompt, return_exceptions=True)

    with patch.object(backend, "load_history_strings", wraps=backend.load_history_strings) as load:
        asyncio.run(asyncio.wait_for(run_session(), timeout=5))
        assert load.call_count == int(file_history)


def test_completion_updates_during_threaded_history_loading() -> None:
    partial_load = Event()
    finish_load = Event()

    class SlowHistory(History):
        def load_history_strings(self) -> Iterable[str]:
            yield "restart server"
            partial_load.set()
            assert finish_load.wait(timeout=5)
            yield "reload config"

        def store_string(self, string: str) -> None:
            pass

    history = ThreadedHistory(SlowHistory())
    completer = HistoryCompleter(history, {"status"})

    async def load_and_complete() -> None:
        loading = asyncio.create_task(_load_history(history))
        try:
            assert await asyncio.to_thread(partial_load.wait, 3)
            assert _completions(completer) == ["restart server", "status"]
        finally:
            finish_load.set()
            await loading
        assert _completions(completer) == ["reload config", "restart server", "status"]

    asyncio.run(asyncio.wait_for(load_and_complete(), timeout=5))


def test_completion_history_is_isolated_between_sessions(tmp_path: Path) -> None:
    first = FileHistory(tmp_path / "first-history")
    second = FileHistory(tmp_path / "second-history")
    first.append_string("first command")
    second.append_string("second command")
    first_completer = HistoryCompleter(first, {"status"})
    second_completer = HistoryCompleter(second, {"status"})

    assert _completions(first_completer) == ["first command", "status"]
    assert _completions(second_completer) == ["second command", "status"]
