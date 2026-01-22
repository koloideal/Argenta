__all__ = [
    "benchmark_parse_simple_command",
    "benchmark_command_with_few_flags",
    "benchmark_command_with_flags_and_values",
    "benchmark_command_with_mixed_prefixes",
    "benchmark_command_with_long_values",
    "benchmark_command_with_quoted_values",
    "benchmark_extreme_many_flags"
]

from argenta.command.models import InputCommand

from .entity import benchmarks


@benchmarks.register(type_="input_command_parse", description="Simple command (no flags)")
def benchmark_parse_simple_command() -> None:
    InputCommand.parse("start")


@benchmarks.register(type_="input_command_parse", description="Command with few flags (3 flags)")
def benchmark_command_with_few_flags() -> None:
    InputCommand.parse("start -a -b -c")


@benchmarks.register(type_="input_command_parse", description="Command with flags and values (5 flags)")
def benchmark_command_with_flags_and_values() -> None:
    InputCommand.parse("start --host localhost --port 8080 --debug --verbose -c config.json")


@benchmarks.register(type_="input_command_parse", description="Command with mixed prefixes (-, --, ---)")
def benchmark_command_with_mixed_prefixes() -> None:
    InputCommand.parse("cmd -a --bb ---ccc -d value --ee value2 ---fff value3")


@benchmarks.register(type_="input_command_parse", description="Command with long values (10 flags)")
def benchmark_command_with_long_values() -> None:
    long_value = "a" * 100
    cmd = f"process --data {long_value} --config {long_value} --output {long_value}"
    InputCommand.parse(cmd)


@benchmarks.register(type_="input_command_parse", description="Command with quoted values (5 flags)")
def benchmark_command_with_quoted_values() -> None:
    InputCommand.parse("cmd --text 'hello world' --path '/usr/local/bin' --msg \"test message\"")


@benchmarks.register(type_="input_command_parse", description="Extreme (50 flags with values)")
def benchmark_extreme_many_flags() -> None:
    flags = " ".join(f"--flag{i} value{i}" for i in range(50))
    InputCommand.parse(f"command {flags}")
