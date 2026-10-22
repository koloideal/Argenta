import asyncio
import atexit
from pathlib import Path
from tempfile import TemporaryDirectory

from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.document import Document
from prompt_toolkit.history import FileHistory, History, ThreadedHistory

from argenta.app.autocompleter._ext_features_impl import HistoryCompleter
from metrics.benchmarks.entity import benchmarks

_BENCHMARK_TYPE = "command_history_completion"
_SMALL_HISTORY_COUNT = 1000
_LARGE_HISTORY_COUNT = 10000
_STRESS_HISTORY_COUNT = 100000
_MISSING_PREFIX = "missing"
_HISTORY_DIRECTORY = TemporaryDirectory(prefix="argenta-history-bench-")

atexit.register(_HISTORY_DIRECTORY.cleanup)


async def _load_history(history: History) -> list[str]:
    return [entry async for entry in history.load()]


def _complete(completer: HistoryCompleter, prefix: str) -> None:
    list(completer.get_completions(Document(prefix), CompleteEvent()))


def _history_completer(entry_count: int) -> HistoryCompleter:
    filename = Path(_HISTORY_DIRECTORY.name) / f"history-{entry_count}"
    filename.write_text(
        "".join(f"\n+history{index} --flag value\n" for index in range(entry_count)),
        encoding="utf-8",
    )
    history = ThreadedHistory(FileHistory(filename))
    asyncio.run(_load_history(history))
    completer = HistoryCompleter(history, {"status"})
    _complete(completer, _MISSING_PREFIX)
    return completer


_SMALL_COMPLETER = _history_completer(_SMALL_HISTORY_COUNT)
_LARGE_COMPLETER = _history_completer(_LARGE_HISTORY_COUNT)
_STRESS_COMPLETER = _history_completer(_STRESS_HISTORY_COUNT)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Loaded file history (1,000 entries)")
def benchmark_file_history_small() -> None:
    _complete(_SMALL_COMPLETER, _MISSING_PREFIX)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Loaded file history (10,000 entries)")
def benchmark_file_history_large() -> None:
    _complete(_LARGE_COMPLETER, _MISSING_PREFIX)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Loaded file history (100,000 entries)")
def benchmark_file_history_stress() -> None:
    _complete(_STRESS_COMPLETER, _MISSING_PREFIX)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="One match in 10,000 loaded file entries")
def benchmark_file_history_match() -> None:
    _complete(_LARGE_COMPLETER, "history9999 ")
