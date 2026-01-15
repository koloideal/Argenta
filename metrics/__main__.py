from concurrent.futures import ProcessPoolExecutor
import os

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

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
        header_text = Text(f"TYPE: {type_.upper()}", style="bold magenta")
        console.print(Panel(header_text, expand=False, border_style="magenta"))

        table = Table(show_header=True, header_style="bold cyan", border_style="blue", show_lines=True)
        table.add_column("Name", style="green")
        table.add_column("Description", style="dim")
        table.add_column("Iterations", justify="right")
        table.add_column("Avg Time (ms)", justify="right", style="bold yellow")

        for benchmark in benchmarks:
            table.add_row(
                benchmark.name,
                benchmark.description,
                str(benchmark.iterations),
                str(benchmark.avg_time)
            )

        console.print(table)
        console.print()


if __name__ == "__main__":
    main()
