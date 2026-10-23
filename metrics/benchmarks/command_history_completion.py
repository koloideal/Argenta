import asyncio
import atexit
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from prompt_toolkit.history import FileHistory, ThreadedHistory

from argenta.app.autocompleter._ext_features_impl import HistoryCompleter
from metrics.benchmarks._history_scenarios import complete, load_history
from metrics.benchmarks.entity import benchmarks


@dataclass(frozen=True, slots=True)
class HistoryCompletionConfig:
    benchmark_type: str = "command_history_completion"
    small_history_count: int = 1000
    large_history_count: int = 10000
    stress_history_count: int = 100000
    missing_prefix: str = "missing"


def _history_completer(entry_count: int, history_directory: Path) -> HistoryCompleter:
    filename = history_directory / f"history-{entry_count}"
    filename.write_text(
        "".join(f"\n+history{index} --flag value\n" for index in range(entry_count)),
        encoding="utf-8",
    )
    history = ThreadedHistory(FileHistory(filename))
    asyncio.run(load_history(history))
    completer = HistoryCompleter(history, {"status"})
    complete(completer, _CONFIG.missing_prefix)
    return completer


def _history_completers() -> SimpleNamespace:
    directory = TemporaryDirectory(prefix="argenta-history-bench-")
    atexit.register(directory.cleanup)
    history_directory = Path(directory.name)
    return SimpleNamespace(
        directory=directory,
        small=_history_completer(_CONFIG.small_history_count, history_directory),
        large=_history_completer(_CONFIG.large_history_count, history_directory),
        stress=_history_completer(_CONFIG.stress_history_count, history_directory),
    )


_CONFIG = HistoryCompletionConfig()
_COMPLETERS = _history_completers()


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Loaded file history (1,000 entries)"
)
def benchmark_file_history_small() -> None:
    complete(_COMPLETERS.small, _CONFIG.missing_prefix)


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Loaded file history (10,000 entries)"
)
def benchmark_file_history_large() -> None:
    complete(_COMPLETERS.large, _CONFIG.missing_prefix)


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Loaded file history (100,000 entries)"
)
def benchmark_file_history_stress() -> None:
    complete(_COMPLETERS.stress, _CONFIG.missing_prefix)


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="One match in 10,000 loaded file entries"
)
def benchmark_file_history_match() -> None:
    complete(_COMPLETERS.large, "history9999 ")
