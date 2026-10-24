from dataclasses import dataclass
from types import SimpleNamespace

from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.document import Document
from prompt_toolkit.history import InMemoryHistory

from argenta.app.autocompleter._ext_features_impl import HistoryCompleter
from metrics.benchmarks.entity import benchmarks


@dataclass(frozen=True, slots=True)
class AutocompleteConfig:
    benchmark_type: str = "command_autocomplete"
    history_entries_count: int = 20
    many_commands_count: int = 50
    extreme_commands_count: int = 2100


def _completer_with_commands(command_count: int, history_entries_count: int) -> HistoryCompleter:
    history = InMemoryHistory()
    for history_index in range(history_entries_count):
        history.append_string(f"old{history_index} --flag value")
    static_commands = {f"command{command_index}" for command_index in range(command_count)}
    return HistoryCompleter(history, static_commands)


def _complete(completer: HistoryCompleter, text: str) -> None:
    list(completer.get_completions(Document(text), CompleteEvent()))


_CONFIG = AutocompleteConfig()
_COMPLETERS = SimpleNamespace(
    many=_completer_with_commands(_CONFIG.many_commands_count, _CONFIG.history_entries_count),
    extreme=_completer_with_commands(_CONFIG.extreme_commands_count, _CONFIG.history_entries_count),
)


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Many commands (50 commands, prefix match)"
)
def benchmark_autocomplete_many_commands() -> None:
    _complete(_COMPLETERS.many, "comm")


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="No match (50 commands, history scan)"
)
def benchmark_autocomplete_no_match() -> None:
    _complete(_COMPLETERS.many, "zzz")


@benchmarks.register(
    type_=_CONFIG.benchmark_type,
    description="Extreme (100 commands, 20 aliases each, prefix match)",
)
def benchmark_autocomplete_extreme() -> None:
    _complete(_COMPLETERS.extreme, "comm")
