__all__ = [
    "benchmark_validate_all_single_flag",
    "benchmark_validate_neither_single_flag",
    "benchmark_validate_list_small",
    "benchmark_validate_list_large",
    "benchmark_validate_regex_simple",
    "benchmark_validate_regex_complex",
    "benchmark_validate_multiple_flags_10",
    "benchmark_validate_multiple_flags_50",
    "benchmark_validate_extreme_100_flags",
]

import re

from argenta.command.flag import Flag, InputFlag, PossibleValues

from .entity import benchmarks


@benchmarks.register(type_="flag_validation", description="Single flag with PossibleValues.ALL")
def benchmark_validate_all_single_flag() -> None:
    flag = Flag("test", possible_values=PossibleValues.ALL)
    flag.validate_input_flag_value("some_value")


@benchmarks.register(type_="flag_validation", description="Single flag with PossibleValues.NEITHER")
def benchmark_validate_neither_single_flag() -> None:
    flag = Flag("test", possible_values=PossibleValues.NEITHER)
    flag.validate_input_flag_value("")


@benchmarks.register(type_="flag_validation", description="List validation (5 possible values)")
def benchmark_validate_list_small() -> None:
    flag = Flag("env", possible_values=["dev", "staging", "prod", "test", "local"])
    flag.validate_input_flag_value("prod")


@benchmarks.register(type_="flag_validation", description="List validation (50 possible values)")
def benchmark_validate_list_large() -> None:
    possible_values = [f"value{i}" for i in range(50)]
    flag = Flag("option", possible_values=possible_values)
    flag.validate_input_flag_value("value25")


@benchmarks.register(type_="flag_validation", description="Regex validation (simple pattern)")
def benchmark_validate_regex_simple() -> None:
    pattern = re.compile(r"^\d+$")
    flag = Flag("port", possible_values=pattern)
    flag.validate_input_flag_value("8080")


@benchmarks.register(type_="flag_validation", description="Regex validation (complex pattern)")
def benchmark_validate_regex_complex() -> None:
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    flag = Flag("email", possible_values=pattern)
    flag.validate_input_flag_value("user@example.com")


@benchmarks.register(type_="flag_validation", description="Multiple flags validation (10 flags)")
def benchmark_validate_multiple_flags_10() -> None:
    flags = [Flag(f"flag{i}", possible_values=PossibleValues.ALL) for i in range(10)]
    input_flags = [InputFlag(f"flag{i}", input_value=f"value{i}") for i in range(10)]

    for flag, input_flag in zip(flags, input_flags):
        flag.validate_input_flag_value(input_flag.input_value)


@benchmarks.register(type_="flag_validation", description="Multiple flags validation (50 flags)")
def benchmark_validate_multiple_flags_50() -> None:
    flags = [Flag(f"flag{i}", possible_values=PossibleValues.ALL) for i in range(50)]
    input_flags = [InputFlag(f"flag{i}", input_value=f"value{i}") for i in range(50)]

    for flag, input_flag in zip(flags, input_flags):
        flag.validate_input_flag_value(input_flag.input_value)


@benchmarks.register(
    type_="flag_validation", description="Extreme (100 flags with regex validation)"
)
def benchmark_validate_extreme_100_flags() -> None:
    pattern = re.compile(r"^[a-zA-Z0-9_-]+$")
    flags = [Flag(f"flag{i}", possible_values=pattern) for i in range(100)]
    input_flags = [InputFlag(f"flag{i}", input_value=f"valid_value_{i}") for i in range(100)]

    for flag, input_flag in zip(flags, input_flags):
        flag.validate_input_flag_value(input_flag.input_value)
