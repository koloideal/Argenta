import platform
import cpuinfo

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router
from .benchmarks.core.models import BenchmarkGroupResult
from .benchmarks.entity import benchmarks as registered_benchmarks

console = Console()
router = Router(title="Metrics commands:")


@router.command(Command("all-print", description="Print all benchmarks results"))
def all_print_handler(_: Response) -> None:
    cpu_info = cpuinfo.get_cpu_info()
    gpu_info = get_gpu_info()
    os_info = get_kernel_version()

    table = Table(show_header=True, header_style="bold cyan", border_style="blue", show_lines=True)
    table.add_column("Parameter", style="green")
    table.add_column("Value", style="yellow")

    table.add_row("OS", platform.system())
    table.add_row("OS Name", os_info['product_name'])
    table.add_row("OS Kernel Version", os_info['kernel_version'])
    table.add_row("Architecture", cpu_info['arch'])
    table.add_row("CPU", cpu_info['brand_raw'])
    table.add_row("GPU", gpu_info)
    table.add_row("Python Version", cpu_info['python_version'])
    table.add_row("Python Implementation", platform.python_implementation())

    header_text = Text("SYSTEM INFO", style="bold magenta")
    console.print(Panel(header_text, expand=False, border_style="magenta"))
    console.print(table, end="\n\n")

    type_grouped_benchmarks: list[BenchmarkGroupResult] = registered_benchmarks.run_benchmarks_grouped_by_type()

    for results in type_grouped_benchmarks:
        header_text = Text(f"TYPE: {results.type_.upper()} ; ITERATIONS: {results.iterations} ; ALL TIME IN MS", style="bold magenta")
        console.print(Panel(header_text, expand=False, border_style="magenta"))

        table = Table(show_header=True, header_style="bold cyan", border_style="blue", show_lines=True)
        table.add_column("Description", style="dim")
        table.add_column("Avg Time", justify="right", style="bold yellow")
        table.add_column("Median Time", justify="right", style="bold yellow")
        table.add_column("Stdev", justify="right", style="bold yellow")

        for benchmark in results.benchmark_results:
            table.add_row(
                benchmark.description,
                str(benchmark.avg_time),
                str(benchmark.median_time),
                str(benchmark.std_dev),
            )

        console.print(table)


@router.command(Command("release-generate", description="Generate release report"))
def release_generate_handler(_: Response) -> None:
    console.print("[yellow]Release report generation not implemented yet[/yellow]")


@router.command(Command("diagrams-generate", description="Generate diagrams"))
def diagrams_generate_handler(_: Response) -> None:
    console.print("[yellow]Diagrams generation not implemented yet[/yellow]")
