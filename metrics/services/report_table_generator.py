from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from metrics.benchmarks.core.models import BenchmarkGroupResult
from metrics.services.system_models import SystemInfo


class ReportTableGenerator:
    def __init__(self, system_info: SystemInfo):
        self.system_info = system_info
        self._cached_benchmark_tables: dict[int, Table] = {}
        self._cached_system_info_table: Table | None = None

    def generate_benchmark_report_table(
        self, benchmark_group_result: BenchmarkGroupResult
    ) -> Table:
        cached_result = self._cached_benchmark_tables.get(id(benchmark_group_result))
        if cached_result is not None:
            return cached_result

        table = Table(
            show_header=True, header_style="bold cyan", border_style="blue", show_lines=True
        )
        table.add_column("Description", style="dim")
        table.add_column("Avg Time", justify="right", style="bold yellow")
        table.add_column("Median Time", justify="right", style="bold yellow")
        table.add_column("Stdev", justify="right", style="bold yellow")

        for benchmark in benchmark_group_result.benchmark_results:
            table.add_row(
                benchmark.description,
                str(benchmark.avg_time),
                str(benchmark.median_time),
                str(benchmark.std_dev),
            )
        self._cached_benchmark_tables[id(benchmark_group_result)] = table
        return table

    def generate_benchmark_table_header(
        self, benchmark_group_result: BenchmarkGroupResult
    ) -> Panel:
        type_name = benchmark_group_result.type_.upper()
        gc_state = "DISABLED" if benchmark_group_result.is_gc_disabled else "ENABLED"
        header_text = Text(
            f"TYPE: {type_name} ; ITERATIONS: {benchmark_group_result.iterations} ; "
            f"GC {gc_state} ; ALL TIME IN MS",
            style="bold magenta",
        )
        return Panel(header_text, expand=False, border_style="magenta")

    def generate_system_info_table(self) -> Table:
        if self._cached_system_info_table is not None:
            return self._cached_system_info_table

        table = Table(
            show_header=True, header_style="bold cyan", border_style="blue", show_lines=True
        )
        table.add_column("Parameter", style="green")
        table.add_column("Value", style="yellow")

        for parameter, row_text in self._system_info_rows():
            table.add_row(parameter, row_text)

        self._cached_system_info_table = table
        return table

    def generate_system_info_header(self) -> Panel:
        header_text = Text("SYSTEM INFO", style="bold magenta")
        return Panel(header_text, expand=False, border_style="magenta")

    def _system_info_rows(self) -> list[tuple[str, str]]:
        os_info = self.system_info.os_info
        cpu_info = self.system_info.cpu_info
        memory_info = self.system_info.memory_info
        python_info = self.system_info.python_info
        return [
            ("OS Name", os_info.name),
            ("OS Kernel Version", os_info.kernel_version),
            ("Architecture", cpu_info.architecture),
            ("CPU", cpu_info.name),
            ("CPU Physical Cores", str(cpu_info.physical_cores)),
            ("CPU Logical Cores", str(cpu_info.logical_cores)),
            ("CPU Max Frequency", f"{cpu_info.max_frequency} GHz"),
            ("Total RAM", f"{memory_info.total_ram} GB"),
            ("Used RAM", f"{memory_info.used_ram} GB"),
            ("Available RAM", f"{memory_info.available_ram} GB"),
            ("Python Version", python_info.version),
            ("Python Implementation", python_info.implementation),
            ("Python Compiler", python_info.compiler),
        ]
