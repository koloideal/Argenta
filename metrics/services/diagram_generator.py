import dataclasses
from operator import attrgetter
from pathlib import Path

import cairosvg
import pygal
from pygal.style import Style

from metrics.benchmarks.core.models import BenchmarkGroupResult

_TITLE_FONT_SIZE = 40
_LEGEND_FONT_SIZE = 34
_LABEL_FONT_SIZE = 32
_VALUE_FONT_SIZE = 28
_HEADROOM_RATIO = 0.85
_BASE_CHART_HEIGHT = 600
_ROW_HEIGHT = 150
_CHART_WIDTH = 3100


def _chart_style() -> Style:
    return Style(
        background="white",
        plot_background="white",
        foreground="#2c3e50",
        foreground_strong="#000000",
        foreground_subtle="#7f8c8d",
        opacity=".9",
        opacity_hover=".95",
        transition="150ms ease-in",
        colors=("#2ecc71", "#3498db", "#e74c3c"),
        title_font_size=_TITLE_FONT_SIZE,
        legend_font_size=_LEGEND_FONT_SIZE,
        label_font_size=_LABEL_FONT_SIZE,
        major_label_font_size=_LABEL_FONT_SIZE,
        value_font_size=_VALUE_FONT_SIZE,
        value_label_font_size=_VALUE_FONT_SIZE,
        tooltip_font_size=24,
        no_data_font_size=_VALUE_FONT_SIZE,
        font_family="Consolas, 'Courier New', monospace",
    )


@dataclasses.dataclass(frozen=True, slots=True)
class _ChartSeries:
    descriptions: list[str]
    avg_times: list[float]
    median_times: list[float]
    std_devs: list[float]


def _sorted_series(benchmark_group: BenchmarkGroupResult) -> _ChartSeries:
    sorted_results = sorted(benchmark_group.benchmark_results, key=attrgetter("avg_time"))
    return _ChartSeries(
        descriptions=[bench.description for bench in sorted_results],
        avg_times=[bench.avg_time for bench in sorted_results],
        median_times=[bench.median_time for bench in sorted_results],
        std_devs=[bench.std_dev for bench in sorted_results],
    )


def _y_axis_limit(*series: list[float]) -> float:
    peaks = [max(one_series) for one_series in series if one_series]
    max_value = max(peaks, default=0)
    return max_value / _HEADROOM_RATIO if max_value > 0 else 1.0


class DiagramGenerator:
    def __init__(self, output_dir: Path | str) -> None:
        self.output_dir: Path = Path(output_dir) if isinstance(output_dir, str) else output_dir
        self._style = _chart_style()

    def generate_comparison_diagram(self, benchmark_group: BenchmarkGroupResult) -> Path:
        series = _sorted_series(benchmark_group)
        chart = self._build_chart(benchmark_group, series)
        chart.x_labels = series.descriptions
        chart.add("Std Deviation", series.std_devs)
        chart.add("Average Time", series.avg_times)
        chart.add("Median Time", series.median_times)
        return self._write_chart(chart, benchmark_group.type_)

    def _build_chart(
        self,
        benchmark_group: BenchmarkGroupResult,
        series: _ChartSeries,
    ) -> pygal.HorizontalBar:
        y_limit = _y_axis_limit(series.avg_times, series.median_times, series.std_devs)
        chart_title = benchmark_group.type_.replace("_", " ").title()
        gc_state = "Disabled" if benchmark_group.is_gc_disabled else "Enabled"
        dynamic_height = _BASE_CHART_HEIGHT + (len(benchmark_group.benchmark_results) * _ROW_HEIGHT)

        chart = pygal.HorizontalBar(
            style=self._style,
            width=_CHART_WIDTH,
            height=dynamic_height,
            explicit_size=True,
            show_legend=True,
            legend_at_bottom=True,
            print_values=True,
            print_values_position="top",
            legend_at_bottom_columns=3,
            range=(0, y_limit),
            zero=0,
        )
        chart.title = f"{chart_title}\nIterations: {benchmark_group.iterations} | GC: {gc_state}"
        chart.x_title = "Time (ms)"
        chart.no_data_text = "No data"
        chart.value_formatter = lambda metric: f"{metric:.3f}"
        return chart

    def _write_chart(self, chart: pygal.HorizontalBar, benchmark_type: str) -> Path:
        output_path = self.output_dir / f"{benchmark_type}_comparison.png"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(bytestring=chart.render(), write_to=str(output_path))
        return output_path
