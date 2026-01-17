__all__ = [
    "Benchmark",
    "Benchmarks",
    "BenchmarkResult",
    "BenchmarkGroupResult"
]

import io
from contextlib import redirect_stdout
from dataclasses import dataclass
import time
import gc
import statistics
from typing import Callable, override

from .exceptions import BenchmarkNotFound, BenchmarksNotFound


FuncForBenchmark = Callable[[], None]
MILLISECONDS_IN_SECONDS = 1000


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    type_: str
    name: str
    description: str
    iterations: int
    is_gc_disabled: bool
    avg_time: float
    median_time: float
    std_dev: float


@dataclass(frozen=True, slots=True)
class BenchmarkGroupResult:
    type_: str
    benchmark_results: list[BenchmarkResult]


class Benchmark:
    def __init__(
            self,
            func: FuncForBenchmark,
            *,
            type_: str,
            name: str,
            description: str
    ) -> None:
        self.func = func
        self.type_ = type_
        self.name = name
        self.description = description

    def single_run(self, is_gc_disabled: bool = False) -> float:
        if is_gc_disabled:
            was_gc_enabled = gc.isenabled()
            gc.disable()

            with redirect_stdout(io.StringIO()):
                start = time.perf_counter()
                self.func()
                end = time.perf_counter()

            if was_gc_enabled:
                gc.enable()
            gc.collect()

            return (end - start) * MILLISECONDS_IN_SECONDS
        else:
            with redirect_stdout(io.StringIO()):
                start = time.perf_counter()
                self.func()
                end = time.perf_counter()
            return (end - start) * MILLISECONDS_IN_SECONDS

    def multiple_runs(self, iterations: int, is_gc_disabled: bool = False) -> tuple[float, ...]:
        run_attempts: list[float] = []
        for _ in range(iterations):
            run_attempts.append(self.single_run(is_gc_disabled))
        return tuple(run_attempts)

    @override
    def __repr__(self) -> str:
        return f'Benchmark<{self.type_=}, {self.name=}, {self.description=}>'

    @override
    def __str__(self) -> str:
        return f'benchmark {self.name} with type {self.type_}'


class Benchmarks:
    def __init__(self, *benchmarks: Benchmark) -> None:
        self._benchmarks: list[Benchmark] = list(benchmarks)
        self._benchmarks_grouped_by_type: dict[str, list[Benchmark]] = {}
        self._benchmarks_paired_by_name: dict[str, Benchmark] = {}

    def register(
            self,
            type_: str,
            description: str = ""
    ) -> Callable[[FuncForBenchmark], FuncForBenchmark]:
        def decorator(func: FuncForBenchmark) -> FuncForBenchmark:
            benchmark = Benchmark(
                func,
                type_=type_,
                name=func.__name__,
                description=description or f'description for {func.__name__} with type {type_}',
            )
            self._benchmarks.append(benchmark)
            self._benchmarks_paired_by_name[func.__name__] = benchmark
            self._benchmarks_grouped_by_type.setdefault(type_, []).append(benchmark)
            return func
        return decorator

    def run_benchmark_by_name(self, name: str, iterations: int = 100, is_gc_disables: bool = False) -> BenchmarkResult:
        benchmark = self.get_benchmark_by_name(name)
        if not benchmark:
            raise BenchmarkNotFound(name)
        run_attempts: tuple[float, ...] = benchmark.multiple_runs(iterations, is_gc_disables)

        avg = round(statistics.mean(run_attempts), 4)
        median = round(statistics.median(run_attempts), 4)
        std_dev = round(statistics.stdev(run_attempts) if len(run_attempts) > 1 else 0, 4)

        return BenchmarkResult(
            type_=benchmark.type_,
            name=benchmark.name,
            description=benchmark.description,
            iterations=iterations,
            is_gc_disabled=is_gc_disables,
            avg_time=avg,
            median_time=median,
            std_dev=std_dev
        )

    def run_benchmarks_by_type(self, type_: str, iterations: int = 100, is_gc_disabled: bool = False) -> BenchmarkGroupResult:
        benchmarks = self.get_benchmarks_by_type(type_)
        if not benchmarks:
            raise BenchmarksNotFound(type_)
        benchmark_results: list[BenchmarkResult] = []

        for benchmark in benchmarks:
            benchmark_results.append(self.run_benchmark_by_name(benchmark.name, iterations, is_gc_disabled))

        return BenchmarkGroupResult(
            type_=type_,
            benchmark_results=benchmark_results
        )

    def run_benchmarks_grouped_by_type(self) -> list[BenchmarkGroupResult]:
        results: list[BenchmarkGroupResult] = []
        for type_, benchmarks in self._benchmarks_grouped_by_type.items():
            results.append(self.run_benchmarks_by_type(type_))
        return results

    def get_benchmarks_by_type(self, type_: str) -> list[Benchmark]:
        return self._benchmarks_grouped_by_type.get(type_, [])

    def get_benchmark_by_name(self, name: str) -> Benchmark | None:
        return self._benchmarks_paired_by_name.get(name)
