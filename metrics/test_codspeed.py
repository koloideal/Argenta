"""CodSpeed entry point: every benchmark registered in ``metrics.benchmarks``.

Run with ``pytest metrics/test_codspeed.py --codspeed``.
"""

import pytest
from pytest_codspeed import BenchmarkFixture

from metrics.benchmarks.core.models import Benchmark
from metrics.benchmarks.entity import benchmarks


@pytest.mark.parametrize(
    "registered_benchmark",
    benchmarks.get_all_benchmarks(),
    ids=lambda bench: f"{bench.type_}.{bench.name.removeprefix('benchmark_')}",
)
def test_benchmark(benchmark: BenchmarkFixture, registered_benchmark: Benchmark) -> None:
    benchmark(registered_benchmark.func)
