import re
from importlib.metadata import version

from argenta import Command, Response, Router
from argenta.command import Flag, Flags, PossibleValues
from argenta.command.flag import ValidationStatus
from metrics.benchmarks.core.models import (
    BenchmarkGroupResult,
    run_benchmarks_by_type,
    run_benchmarks_grouped_by_type,
)
from metrics.benchmarks.entity import benchmarks as registered_benchmarks
from metrics.cli_helpers import (
    console,
    diagrams_output_dir,
    generate_group_diagrams,
    is_flag_enabled,
    print_system_info,
    report_unknown_type,
    resolve_iterations,
)
from metrics.services import (
    DiagramGenerator,
    ReleaseGenerator,
    ReportTableGenerator,
    get_system_info,
)

router = Router(title="Metrics commands:", disable_redirect_stdout=True)

POSITIVE_INTEGER_PATTERN = re.compile(r"^[1-9]\d*$")
_WITHOUT_GC_FLAG = "without-gc"
_WITHOUT_SYSTEM_INFO_FLAG = "without-system-info"


@router.command(
    Command(
        "run-all",
        description="Print all benchmarks results",
        flags=Flags(
            [
                Flag(_WITHOUT_GC_FLAG, possible_values=PossibleValues.NEITHER),
                Flag(_WITHOUT_SYSTEM_INFO_FLAG, possible_values=PossibleValues.NEITHER),
            ]
        ),
    )
)
def all_print_handler(response: Response) -> None:
    report_generator = ReportTableGenerator(get_system_info())

    if not is_flag_enabled(response, _WITHOUT_SYSTEM_INFO_FLAG):
        print_system_info(report_generator)

    type_grouped_benchmarks: list[BenchmarkGroupResult] = run_benchmarks_grouped_by_type(
        registered_benchmarks,
        is_gc_disabled=is_flag_enabled(response, _WITHOUT_GC_FLAG),
    )

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
        flags=Flags(
            [
                Flag("type", possible_values=registered_benchmarks.get_types()),
                Flag(_WITHOUT_GC_FLAG, possible_values=PossibleValues.NEITHER),
                Flag(_WITHOUT_SYSTEM_INFO_FLAG, possible_values=PossibleValues.NEITHER),
            ]
        ),
    )
)
def run_type_handler(response: Response) -> None:
    type_flag = response.input_flags.get_flag_by_name("type")

    if not type_flag:
        console.print("[red]Error: --type flag is required[/red]")
        console.print("[yellow]Usage: run-type --type <type_name>[/yellow]")
        return

    if type_flag.status != ValidationStatus.VALID:
        report_unknown_type(type_flag.input_value)
        return

    report_generator = ReportTableGenerator(get_system_info())

    if not is_flag_enabled(response, _WITHOUT_SYSTEM_INFO_FLAG):
        print_system_info(report_generator)

    benchmark_group_result = run_benchmarks_by_type(
        registered_benchmarks,
        type_flag.input_value,
        is_gc_disabled=is_flag_enabled(response, _WITHOUT_GC_FLAG),
    )

    console.print(report_generator.generate_benchmark_table_header(benchmark_group_result))
    console.print(report_generator.generate_benchmark_report_table(benchmark_group_result))


@router.command(Command("release-generate", description="Generate release report"))
def release_generate_handler(_: Response) -> None:
    lib_version = version("argenta")

    console.print(f"[cyan]Generating release report for version:[/cyan] [bold]{lib_version}[/bold]")
    console.print("[dim]Running benchmarks (1000 iterations, GC disabled)...[/dim]\n")

    type_grouped_benchmarks: list[BenchmarkGroupResult] = run_benchmarks_grouped_by_type(
        registered_benchmarks, iterations=1000, is_gc_disabled=True
    )

    release_generator = ReleaseGenerator(lib_version)
    output_dir = release_generator.generate_release(type_grouped_benchmarks)

    console.print("[green]✓[/green] Benchmarks completed. Generating release report...\n")

    for benchmark_group in type_grouped_benchmarks:
        console.print(f"[cyan]Generated for:[/cyan] [bold]{benchmark_group.type_}[/bold]")
        console.print(f"  [green]✓[/green] {benchmark_group.type_}_comparison.png")
        console.print(f"  [green]✓[/green] {benchmark_group.type_}.json\n")

    console.print("[bold green]✓ Release report generated successfully[/bold green]")
    console.print(f"[cyan]Output directory:[/cyan] [bold]{output_dir}[/bold]")


@router.command(
    Command(
        "diagrams-generate",
        description="Generate diagrams for all benchmarks",
        flags=Flags(
            [
                Flag(_WITHOUT_GC_FLAG, possible_values=PossibleValues.NEITHER),
                Flag("iterations", possible_values=POSITIVE_INTEGER_PATTERN),
            ]
        ),
    )
)
def diagrams_generate_handler(response: Response) -> None:
    iterations = resolve_iterations(response)
    is_gc_disabled = is_flag_enabled(response, _WITHOUT_GC_FLAG)

    console.print("[cyan]Running all benchmarks...[/cyan]")
    console.print(f"[dim]Iterations: {iterations}, GC Disabled: {is_gc_disabled}[/dim]\n")

    output_dir = diagrams_output_dir()
    generated_count = generate_group_diagrams(
        run_benchmarks_grouped_by_type(
            registered_benchmarks, iterations=iterations, is_gc_disabled=is_gc_disabled
        ),
        DiagramGenerator(output_dir),
    )

    console.print(f"[bold green]✓ Successfully generated {generated_count} diagrams[/bold green]")
    console.print(f"[cyan]Output directory:[/cyan] [bold]{output_dir}[/bold]")
