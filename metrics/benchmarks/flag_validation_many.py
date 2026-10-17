import re

from argenta.command.flag import Flag, InputFlag, PossibleValues
from metrics.benchmarks.entity import benchmarks

_BENCHMARK_TYPE = "flag_validation"
_TEN_FLAGS_COUNT = 10
_FIFTY_FLAGS_COUNT = 50
_HUNDRED_FLAGS_COUNT = 100


def _validate_flags(flags_count: int) -> None:
    flags = [
        Flag(f"flag{flag_index}", possible_values=PossibleValues.ALL)
        for flag_index in range(flags_count)
    ]
    input_flags = [
        InputFlag(f"flag{flag_index}", input_value=f"value{flag_index}")
        for flag_index in range(flags_count)
    ]

    for flag, input_flag in zip(flags, input_flags, strict=True):
        flag.validate_input_flag_value(input_flag.input_value)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Multiple flags validation (10 flags)")
def benchmark_validate_ten_flags() -> None:
    _validate_flags(_TEN_FLAGS_COUNT)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Multiple flags validation (50 flags)")
def benchmark_validate_fifty_flags() -> None:
    _validate_flags(_FIFTY_FLAGS_COUNT)


@benchmarks.register(type_=_BENCHMARK_TYPE, description="Extreme (100 flags with regex validation)")
def benchmark_validate_hundred_flags_regex() -> None:
    pattern = re.compile(r"^[a-zA-Z0-9_-]+$")
    flags = [
        Flag(f"flag{flag_index}", possible_values=pattern)
        for flag_index in range(_HUNDRED_FLAGS_COUNT)
    ]
    input_flags = [
        InputFlag(f"flag{flag_index}", input_value=f"valid_value_{flag_index}")
        for flag_index in range(_HUNDRED_FLAGS_COUNT)
    ]

    for flag, input_flag in zip(flags, input_flags, strict=True):
        flag.validate_input_flag_value(input_flag.input_value)
