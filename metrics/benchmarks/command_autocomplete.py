from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.document import Document
from prompt_toolkit.history import InMemoryHistory

from argenta.app.autocompleter._ext_features_impl import HistoryCompleter
from metrics.benchmarks.entity import benchmarks

_HISTORY_ENTRIES_COUNT = 20
_MANY_COMMANDS_COUNT = 50
_EXTREME_COMMANDS_COUNT = 2100


def _completer_with_commands(command_count: int) -> HistoryCompleter:
    history = InMemoryHistory()
    for history_index in range(_HISTORY_ENTRIES_COUNT):
        history.append_string(f"old{history_index} --flag value")
    static_commands = {f"command{command_index}" for command_index in range(command_count)}
    return HistoryCompleter(history, static_commands)


def _complete(completer: HistoryCompleter, text: str) -> None:
    list(completer.get_completions(Document(text), CompleteEvent()))


_MANY_COMPLETER = _completer_with_commands(_MANY_COMMANDS_COUNT)
_EXTREME_COMPLETER = _completer_with_commands(_EXTREME_COMMANDS_COUNT)


@benchmarks.register(
    type_="command_autocomplete", description="Many commands (50 commands, prefix match)"
)
def benchmark_autocomplete_many_commands() -> None:
    _complete(_MANY_COMPLETER, "comm")


@benchmarks.register(
    type_="command_autocomplete", description="No match (50 commands, history scan)"
)
def benchmark_autocomplete_no_match() -> None:
    _complete(_MANY_COMPLETER, "zzz")


@benchmarks.register(
    type_="command_autocomplete",
    description="Extreme (100 commands, 20 aliases each, prefix match)",
)
def benchmark_autocomplete_extreme() -> None:
    _complete(_EXTREME_COMPLETER, "comm")
