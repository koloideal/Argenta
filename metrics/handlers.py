from rich.console import Console

from argenta.command import Flag, PossibleValues
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router
from .benchmarks.core.models import BenchmarkGroupResult
from .benchmarks.entity import benchmarks as registered_benchmarks
from .services.report_generator import ReportGenerator
from .services.system_info_reader import get_system_info

console = Console()
router = Router(title="Metrics commands:")


@router.command(
    Command(
        "all-print",
        description="Print all benchmarks results",
        flags=Flag('without-gc', possible_values=PossibleValues.NEITHER)
    )
)
def all_print_handler(_: Response) -> None:
    report_generator = ReportGenerator(get_system_info())
    console.print(report_generator.generate_system_info_header())
    console.print(report_generator.generate_system_info_table())
    is_gc_disabled = _.input_flags.get_flag_by_name("without-gc")
    type_grouped_benchmarks: list[BenchmarkGroupResult] = registered_benchmarks.run_benchmarks_grouped_by_type(is_gc_disabled=is_gc_disabled)
    for benchmark_group_result in type_grouped_benchmarks:
        console.print(report_generator.generate_benchmark_table_header(benchmark_group_result))
        console.print(report_generator.generate_benchmark_report_table(benchmark_group_result))


@router.command(Command("release-generate", description="Generate release report"))
def release_generate_handler(_: Response) -> None:
    console.print("[yellow]Release report generation not implemented yet[/yellow]")


@router.command(Command("diagrams-generate", description="Generate diagrams"))
def diagrams_generate_handler(_: Response) -> None:
    console.print("[yellow]Diagrams generation not implemented yet[/yellow]")
