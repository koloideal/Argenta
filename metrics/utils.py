__all__ = [
    "get_time_of_pre_cycle_setup",
    "attempts_to_average",
    "run_benchmark",
    "BenchmarkResult"
]

import io
from contextlib import redirect_stdout
import time
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from argenta import App
from metrics.registry import Benchmark


def get_time_of_pre_cycle_setup(app: App) -> float:
    start = time.monotonic()
    with redirect_stdout(io.StringIO()):
        app._pre_cycle_setup()  # pyright: ignore[reportPrivateUsage]
    end = time.monotonic()
    return end - start


def attempts_to_average(bench_attempts: list[float], iterations: int) -> Decimal:
    return Decimal(sum(bench_attempts) / iterations).quantize(Decimal("0.00001"), rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class BenchmarkResult:
    type_: str
    name: str
    description: str
    iterations: int
    avg_time: Decimal


def run_benchmark(benchmark: Benchmark) -> BenchmarkResult:
    bench_attempts: list[float] = []
    for _ in range(benchmark.iterations):
        bench_attempts.append(benchmark.run())
    avg = attempts_to_average(bench_attempts, benchmark.iterations)
    return BenchmarkResult(benchmark.type_, benchmark.name, benchmark.description, benchmark.iterations, avg)
