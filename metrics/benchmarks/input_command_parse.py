from argenta.command.models import InputCommand
from metrics.benchmarks.entity import benchmarks

_BENCHMARK_TYPE = "input_command_parse"
_EXTREME_FLAGS_COUNT = 50


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Simple command (no flags)")
def benchmark_parse_simple_command() -> None:
    InputCommand.parse("start")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Command with few flags (3 flags)")
def benchmark_command_with_few_flags() -> None:
    InputCommand.parse("start -a -b -c")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Command with flags and values (5 flags)")
def benchmark_command_with_flags_and_values() -> None:
    InputCommand.parse("start --host localhost --port 8080 --debug --verbose -c config.json")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Command with mixed prefixes (-, --, ---)")
def benchmark_command_with_mixed_prefixes() -> None:
    InputCommand.parse("cmd -a --bb ---ccc -d value --ee value2 ---fff value3")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Command with long values (10 flags)")
def benchmark_command_with_long_values() -> None:
    long_value = "a" * 100
    cmd = f"process --data {long_value} --config {long_value} --output {long_value}"
    InputCommand.parse(cmd)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Command with quoted values (5 flags)")
def benchmark_command_with_quoted_values() -> None:
    InputCommand.parse("cmd --text 'hello world' --path '/usr/local/bin' --msg \"test message\"")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Extreme (50 flags with values)")
def benchmark_extreme_many_flags() -> None:
    flags = " ".join(
        f"--flag{flag_index} value{flag_index}" for flag_index in range(_EXTREME_FLAGS_COUNT)
    )
    InputCommand.parse(f"command {flags}")
