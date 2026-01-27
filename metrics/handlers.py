import re
from datetime import datetime
from importlib.metadata import version
from pathlib import Path

from rich.console import Console

from argenta.command import Flag, PossibleValues, Flags
from argenta.command.flag import ValidationStatus
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router
from .benchmarks.core.models import BenchmarkGroupResult
from .benchmarks.entity import benchmarks as registered_benchmarks
from .services.report_table_generator import ReportTableGenerator
from .services.system_info_reader import get_system_info
from .services.diagram_generator import DiagramGenerator
from .services.release_generator import ReleaseGenerator

console = Console()
router = Router(title="Metrics commands:", disable_redirect_stdout=True)

POSITIVE_INTEGER_PATTERN = re.compile(r"^[1-9]\d*$")


@router.command(
    Command(
        "run-all",
        description="Print all benchmarks results",
        flags=Flags([
            Flag('without-gc', possible_values=PossibleValues.NEITHER),
            Flag('without-system-info', possible_values=PossibleValues.NEITHER)
        ])
    )
)
def all_print_handler(response: Response) -> None:
    report_generator = ReportTableGenerator(get_system_info())
    
    without_system_info = response.input_flags.get_flag_by_name("without-system-info", with_status=ValidationStatus.VALID)
    if not without_system_info:
        console.print(report_generator.generate_system_info_header())
        console.print(report_generator.generate_system_info_table())

    is_gc_disabled = response.input_flags.get_flag_by_name("without-gc", with_status=ValidationStatus.VALID)
    type_grouped_benchmarks: list[BenchmarkGroupResult] = registered_benchmarks.run_benchmarks_grouped_by_type(is_gc_disabled=bool(is_gc_disabled))

    for benchmark_group_result in type_grouped_benchmarks:
        console.print(report_generator.generate_benchmark_table_header(benchmark_group_result))
        console.print(report_generator.generate_benchmark_report_table(benchmark_group_result))


@router.command(Command("list-types", description="List all benchmark types"))
def list_types_handler(_: Response) -> None:
    types = registered_benchmarks.get_types()
    
    if not types:
        console.print("[yellow]No benchmark types found[/yellow]")
        return
    
    console.print("[bold cyan]Available benchmark types:[/bold cyan]\n")
    for type_ in types:
        benchmarks_count = len(registered_benchmarks.get_benchmarks_by_type(type_))
        console.print(f"  [green]•[/green] [bold]{type_}[/bold] ({benchmarks_count} benchmarks)")


@router.command(
    Command(
        "run-type",
        description="Run benchmarks by specific type",
        flags=Flags([
            Flag('type', possible_values=registered_benchmarks.get_types()),
            Flag('without-gc', possible_values=PossibleValues.NEITHER),
            Flag('without-system-info', possible_values=PossibleValues.NEITHER)
        ])
    )
)
def run_type_handler(response: Response) -> None:
    type_flag = response.input_flags.get_flag_by_name("type")
    
    if not type_flag:
        console.print("[red]Error: --type flag is required[/red]")
        console.print("[yellow]Usage: run-type --type <type_name>[/yellow]")
        return
    
    benchmark_type = type_flag.input_value
    
    if not type_flag.status == ValidationStatus.VALID:
        console.print(f"[red]Error: No benchmarks found for type '{benchmark_type}'[/red]")
        console.print("\n[yellow]Available types:[/yellow]")
        types = registered_benchmarks.get_types()
        for t in types:
            console.print(f"  • {t}")
        return
    
    report_generator = ReportTableGenerator(get_system_info())
    
    without_system_info = response.input_flags.get_flag_by_name("without-system-info", with_status=ValidationStatus.VALID)
    if not without_system_info:
        console.print(report_generator.generate_system_info_header())
        console.print(report_generator.generate_system_info_table())
    
    is_gc_disabled = response.input_flags.get_flag_by_name("without-gc", with_status=ValidationStatus.VALID, default=False)
    benchmark_group_result = registered_benchmarks.run_benchmarks_by_type(benchmark_type, is_gc_disabled=bool(is_gc_disabled))
    
    console.print(report_generator.generate_benchmark_table_header(benchmark_group_result))
    console.print(report_generator.generate_benchmark_report_table(benchmark_group_result))


@router.command(Command("release-generate", description="Generate release report"))
def release_generate_handler(_: Response) -> None:
    lib_version = version("argenta")
    
    console.print(f"[cyan]Generating release report for version:[/cyan] [bold]{lib_version}[/bold]")
    console.print("[dim]Running benchmarks (1000 iterations, GC disabled)...[/dim]\n")
    
    type_grouped_benchmarks: list[BenchmarkGroupResult] = registered_benchmarks.run_benchmarks_grouped_by_type(
        iterations=1000,
        is_gc_disabled=True
    )
    
    release_generator = ReleaseGenerator(lib_version)
    output_dir = release_generator.generate_release(type_grouped_benchmarks)
    
    console.print(f"[green]✓[/green] Benchmarks completed. Generating release report...\n")
    
    for benchmark_group in type_grouped_benchmarks:
        console.print(f"[cyan]Generated for:[/cyan] [bold]{benchmark_group.type_}[/bold]")
        console.print(f"  [green]✓[/green] {benchmark_group.type_}_comparison.png")
        console.print(f"  [green]✓[/green] {benchmark_group.type_}.json\n")
    
    console.print(f"[bold green]✓ Release report generated successfully[/bold green]")
    console.print(f"[cyan]Output directory:[/cyan] [bold]{output_dir}[/bold]")


@router.command(
    Command(
        "diagrams-generate",
        description="Generate diagrams for all benchmarks",
        flags=Flags([
            Flag('without-gc', possible_values=PossibleValues.NEITHER),
            Flag('iterations', possible_values=POSITIVE_INTEGER_PATTERN)
        ])
    )
)
def diagrams_generate_handler(response: Response) -> None:
    iterations = 100
    iterations_flag = response.input_flags.get_flag_by_name("iterations", with_status=ValidationStatus.VALID)
    if iterations_flag:
        iterations = int(iterations_flag.input_value)
    
    is_gc_disabled = bool(response.input_flags.get_flag_by_name("without-gc", with_status=ValidationStatus.VALID))
    
    console.print("[cyan]Running all benchmarks...[/cyan]")
    console.print(f"[dim]Iterations: {iterations}, GC Disabled: {is_gc_disabled}[/dim]\n")
    
    type_grouped_benchmarks: list[BenchmarkGroupResult] = registered_benchmarks.run_benchmarks_grouped_by_type(
        iterations=iterations,
        is_gc_disabled=is_gc_disabled
    )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = Path("metrics/reports/diagrams") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    diagram_generator = DiagramGenerator(output_dir)
    
    console.print(f"[green]✓[/green] Benchmarks completed. Generating diagrams...\n")
    
    generated_count = 0
    
    for benchmark_group in type_grouped_benchmarks:
        console.print(f"[cyan]Generating diagram for:[/cyan] [bold]{benchmark_group.type_}[/bold]")
        
        comparison_path = diagram_generator.generate_comparison_diagram(benchmark_group)
        generated_count += 1
        console.print(f"  [green]✓[/green] {comparison_path.name}\n")
    
    console.print(f"[bold green]✓ Successfully generated {generated_count} diagrams[/bold green]")
    console.print(f"[cyan]Output directory:[/cyan] [bold]{output_dir}[/bold]")
