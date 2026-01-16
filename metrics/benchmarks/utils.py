__all__ = [
    "get_time_of_pre_cycle_setup",
    "get_time_of_validate_routers_for_collisions",
    "get_time_of_most_similar_command",
    "get_time_of_finds_appropriate_handler",
    "attempts_to_average",
    "run_benchmark",
    "run_all_benchmarks",
    "get_kernel_version"
]

import io
import os
import platform
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from contextlib import redirect_stdout
from decimal import ROUND_HALF_UP, Decimal

from argenta import App
from argenta.router import Router
from argenta.command.models import InputCommand
from .models import Benchmark, BenchmarkResult, Benchmarks


def get_time_of_pre_cycle_setup(app: App) -> float:
    start = time.perf_counter()
    with redirect_stdout(io.StringIO()):
        app._pre_cycle_setup()  # pyright: ignore[reportPrivateUsage]
    end = time.perf_counter()
    return (end - start) * 1000  # as milliseconds

def get_time_of_validate_routers_for_collisions(app: App) -> float:
    app._setup_system_router()  # pyright: ignore[reportPrivateUsage]
    start = time.perf_counter()
    with redirect_stdout(io.StringIO()):
        app._validate_routers_for_collisions()  # pyright: ignore[reportPrivateUsage]
    end = time.perf_counter()
    return (end - start) * 1000


def get_time_of_most_similar_command(app: App, unknown_command: str) -> float:
    start = time.perf_counter()
    with redirect_stdout(io.StringIO()):
        app._most_similar_command(unknown_command)  # pyright: ignore[reportPrivateUsage]
    end = time.perf_counter()
    return (end - start) * 1000


def get_time_of_finds_appropriate_handler(router: "Router", input_command: "InputCommand") -> float:
    start = time.perf_counter()
    with redirect_stdout(io.StringIO()):
        router.finds_appropriate_handler(input_command)
    end = time.perf_counter()
    return (end - start) * 1000


def get_kernel_version() -> dict[str, str]:
    system = platform.system()

    if system == "Windows":
        ver = sys.getwindowsversion()
        kernel_version = f"{ver.major}.{ver.minor}.{ver.build}"

        if ver.build >= 22000:
            product_name = "Windows 11"
        else:
            product_name = "Windows 10"

        return {
            'kernel_version': kernel_version,
            'product_name': product_name
        }

    elif system == "Linux":
        return {
            'kernel_version': platform.release(),
            'product_name': platform.system()
        }

    elif system == "Darwin":
        return {
            'kernel_version': platform.release(),
            'product_name': f"macOS {platform.mac_ver()[0]}"
        }
    else:
        return {
            'kernel_version': platform.release(),
            'product_name': platform.system(),
        }


def attempts_to_average(bench_attempts: list[float], iterations: int) -> Decimal:
    return Decimal(sum(bench_attempts) / iterations).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def run_all_benchmarks() -> dict[str, list[BenchmarkResult]]:
    all_benchmarks: list[Benchmark] = Benchmarks.get_benchmarks()

    workers = os.cpu_count() or 1
    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = executor.map(run_benchmark, all_benchmarks)

    type_paired_benchmarks: dict[str, list[BenchmarkResult]] = {}

    for result in results:
        type_paired_benchmarks.setdefault(result.type_, []).append(result)

    return type_paired_benchmarks


def run_benchmark(benchmark: Benchmark) -> BenchmarkResult:
    bench_attempts: list[float] = []
    for _ in range(benchmark.iterations):
        bench_attempts.append(benchmark.run())
    avg = attempts_to_average(bench_attempts, benchmark.iterations)
    return BenchmarkResult(benchmark.type_, benchmark.name, benchmark.description, benchmark.iterations, avg)
