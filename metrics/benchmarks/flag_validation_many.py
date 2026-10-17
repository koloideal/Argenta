import re
from dataclasses import dataclass

from argenta.command.flag import Flag, InputFlag, PossibleValues
from metrics.benchmarks.entity import benchmarks


@dataclass(frozen=True, slots=True)
class FlagBatchValidationConfig:
    benchmark_type: str = "flag_validation"
    ten_flags_count: int = 10
    fifty_flags_count: int = 50
    hundred_flags_count: int = 100


_CONFIG = FlagBatchValidationConfig()


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


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Multiple flags validation (10 flags)"
)
def benchmark_validate_ten_flags() -> None:
    _validate_flags(_CONFIG.ten_flags_count)


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Multiple flags validation (50 flags)"
)
def benchmark_validate_fifty_flags() -> None:
    _validate_flags(_CONFIG.fifty_flags_count)


@benchmarks.register(
    type_=_CONFIG.benchmark_type, description="Extreme (100 flags with regex validation)"
)
def benchmark_validate_hundred_flags_regex() -> None:
    pattern = re.compile(r"^[a-zA-Z0-9_-]+$")
    flags = [
        Flag(f"flag{flag_index}", possible_values=pattern)
        for flag_index in range(_CONFIG.hundred_flags_count)
    ]
    input_flags = [
        InputFlag(f"flag{flag_index}", input_value=f"valid_value_{flag_index}")
        for flag_index in range(_CONFIG.hundred_flags_count)
    ]

    for flag, input_flag in zip(flags, input_flags, strict=True):
        flag.validate_input_flag_value(input_flag.input_value)
