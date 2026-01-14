from concurrent.futures import ProcessPoolExecutor
import os

from rich import Console

from metrics.utils import run_benchmark, BenchmarkResult
from .registry import Benchmarks, Benchmark


def main():
    console = Console()
    all_benchmarks: list[Benchmark] = Benchmarks.get_benchmarks()

    workers = os.cpu_count() or 1
    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = executor.map(run_benchmark, all_benchmarks)

    type_paired_benchmarks: dict[str, list[BenchmarkResult]] = {}

    for result in results:
        type_paired_benchmarks.setdefault(result.type_, []).append(result)

    for type_, benchmarks in type_paired_benchmarks.items():
        console.print('\n' + ('='*(len(type_)+14)))
        console.print(f'    TYPE: {type_.upper()}')
        console.print('='*(len(type_)+14) + '\n')

        for benchmark in benchmarks:
            console.print(f'Name: {benchmark.name}\n'
                          f'Description: {benchmark.description}\n'
                          f'Iterations: {benchmark.iterations}\n'
                          f'Average time per iteration: {benchmark.avg_time} ms\n')


if __name__ == "__main__":
    main()
