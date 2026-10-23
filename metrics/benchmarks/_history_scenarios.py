"""Helpers for benchmarks that complete commands from loaded history."""

from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.document import Document
from prompt_toolkit.history import History

from argenta.app.autocompleter._ext_features_impl import HistoryCompleter


async def load_history(history: History) -> list[str]:
    return [entry async for entry in history.load()]


def complete(completer: HistoryCompleter, prefix: str) -> None:
    list(completer.get_completions(Document(prefix), CompleteEvent()))
