from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console

from argenta.command.flag import ValidationStatus
from argenta.response import Response
from metrics.benchmarks.core.models import BenchmarkGroupResult
from metrics.benchmarks.entity import benchmarks as registered_benchmarks
from metrics.services.diagram_generator import DiagramGenerator
from metrics.services.report_table_generator import ReportTableGenerator

console = Console()


def is_flag_enabled(response: Response, flag_name: str) -> bool:
    return bool(
        response.input_flags.get_flag_by_name(flag_name, with_status=ValidationStatus.VALID)
    )


def print_system_info(report_generator: ReportTableGenerator) -> None:
    console.print(report_generator.generate_system_info_header())
    console.print(report_generator.generate_system_info_table())


def report_unknown_type(benchmark_type: str) -> None:
    console.print(f"[red]Error: No benchmarks found for type '{benchmark_type}'[/red]")
    console.print("\n[yellow]Available types:[/yellow]")
    for type_name in registered_benchmarks.get_types():
        console.print(f"  • {type_name}")


def resolve_iterations(response: Response) -> int:
    iterations_flag = response.input_flags.get_flag_by_name(
        "iterations", with_status=ValidationStatus.VALID
    )
    return int(iterations_flag.input_value) if iterations_flag else 100


def diagrams_output_dir() -> Path:
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = Path("metrics/reports/diagrams") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_group_diagrams(
    type_grouped_benchmarks: list[BenchmarkGroupResult], diagram_generator: DiagramGenerator
) -> int:
    console.print("[green]✓[/green] Benchmarks completed. Generating diagrams...\n")
    generated_count = 0
    for benchmark_group in type_grouped_benchmarks:
        console.print(f"[cyan]Generating diagram for:[/cyan] [bold]{benchmark_group.type_}[/bold]")
        comparison_path = diagram_generator.generate_comparison_diagram(benchmark_group)
        generated_count += 1
        console.print(f"  [green]✓[/green] {comparison_path.name}\n")
    return generated_count
