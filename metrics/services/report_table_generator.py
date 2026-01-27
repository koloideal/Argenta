from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..benchmarks.core.models import BenchmarkGroupResult
from metrics.services.system_info_reader import SystemInfo


class ReportTableGenerator:
    def __init__(self, system_info: SystemInfo):
        self.system_info = system_info
        self._cached_benchmark_tables: dict[int, Table] = {}
        self._cached_system_info_table: Table | None = None

    def generate_benchmark_report_table(self, benchmark_group_result: BenchmarkGroupResult) -> Table:
        if cached_result := self._cached_benchmark_tables.get(id(benchmark_group_result)):
            return cached_result

        table = Table(show_header=True, header_style="bold cyan", border_style="blue", show_lines=True)
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

    @staticmethod
    def generate_benchmark_table_header(benchmark_group_result: BenchmarkGroupResult) -> Panel:
        header_text = Text(f"TYPE: {benchmark_group_result.type_.upper()} ; "
                           f"ITERATIONS: {benchmark_group_result.iterations} ; "
                           f"GC {"DISABLED" if benchmark_group_result.is_gc_disabled else "ENABLED"} ; "
                           f"ALL TIME IN MS",
                           style="bold magenta")
        return Panel(header_text, expand=False, border_style="magenta")

    def generate_system_info_table(self) -> Table:
        if self._cached_system_info_table is not None:
            return self._cached_system_info_table

        table = Table(show_header=True, header_style="bold cyan", border_style="blue", show_lines=True)
        table.add_column("Parameter", style="green")
        table.add_column("Value", style="yellow")

        table.add_row("OS Name", self.system_info.os_info.name)
        table.add_row("OS Kernel Version", self.system_info.os_info.kernel_version)
        table.add_row("Architecture", self.system_info.cpu_info.architecture)
        table.add_row("CPU", self.system_info.cpu_info.name)
        table.add_row("CPU Physical Cores", str(self.system_info.cpu_info.physical_cores))
        table.add_row("CPU Logical Cores", str(self.system_info.cpu_info.logical_cores))
        table.add_row("CPU Max Frequency", str(self.system_info.cpu_info.max_frequency) + ' GHz')
        table.add_row("Total RAM", str(self.system_info.memory_info.total_ram) + ' GB')
        table.add_row("Used RAM", str(self.system_info.memory_info.used_ram) + ' GB')
        table.add_row("Available RAM", str(self.system_info.memory_info.available_ram) + ' GB')
        table.add_row("Python Version", self.system_info.python_info.version)
        table.add_row("Python Implementation", self.system_info.python_info.implementation)
        table.add_row("Python Compiler", self.system_info.python_info.compiler)

        self._cached_system_info_table = table
        return table

    @staticmethod
    def generate_system_info_header() -> Panel:
        header_text = Text("SYSTEM INFO", style="bold magenta")
        return Panel(header_text, expand=False, border_style="magenta")