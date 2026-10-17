import re

from argenta.command.flag import Flag, PossibleValues
from metrics.benchmarks.entity import benchmarks

_BENCHMARK_TYPE = "flag_validation"
_LARGE_VALUES_COUNT = 50


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Single flag with PossibleValues.ALL")
def benchmark_validate_all_single_flag() -> None:
    flag = Flag("test", possible_values=PossibleValues.ALL)
    flag.validate_input_flag_value("some_value")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Single flag with PossibleValues.NEITHER")
def benchmark_validate_neither_single_flag() -> None:
    flag = Flag("test", possible_values=PossibleValues.NEITHER)
    flag.validate_input_flag_value("")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="List validation (5 possible values)")
def benchmark_validate_list_small() -> None:
    flag = Flag("env", possible_values=["dev", "staging", "prod", "test", "local"])
    flag.validate_input_flag_value("prod")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="List validation (50 possible values)")
def benchmark_validate_list_large() -> None:
    possible_values = [f"value{value_index}" for value_index in range(_LARGE_VALUES_COUNT)]
    flag = Flag("option", possible_values=possible_values)
    flag.validate_input_flag_value("value25")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Regex validation (simple pattern)")
def benchmark_validate_regex_simple() -> None:
    pattern = re.compile(r"^\d+$")
    flag = Flag("port", possible_values=pattern)
    flag.validate_input_flag_value("8080")


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Regex validation (complex pattern)")
def benchmark_validate_regex_complex() -> None:
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    flag = Flag("email", possible_values=pattern)
    flag.validate_input_flag_value("user@example.com")
