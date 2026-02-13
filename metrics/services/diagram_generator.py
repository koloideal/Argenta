__all__ = ["DiagramGenerator"]

from pathlib import Path

import cairosvg
import pygal
from pygal.style import Style

from ..benchmarks.core.models import BenchmarkGroupResult


class DiagramGenerator:
    def __init__(self, output_dir: Path | str) -> None:
        self.output_dir: Path = Path(output_dir) if isinstance(output_dir, str) else output_dir

        self._style = Style(
            background="white",
            plot_background="white",
            foreground="#2c3e50",
            foreground_strong="#000000",
            foreground_subtle="#7f8c8d",
            opacity=".9",
            opacity_hover=".95",
            transition="150ms ease-in",
            colors=("#2ecc71", "#3498db", "#e74c3c"),
            title_font_size=40,
            legend_font_size=34,
            label_font_size=32,  #
            major_label_font_size=32,
            value_font_size=28,
            value_label_font_size=28,
            tooltip_font_size=24,
            no_data_font_size=28,
            font_family="Consolas, 'Courier New', monospace",
        )

    def generate_comparison_diagram(self, benchmark_group: BenchmarkGroupResult) -> Path:
        results = benchmark_group.benchmark_results
        sorted_results = sorted(results, key=lambda br: br.avg_time)

        descriptions: list[str] = [br.description for br in sorted_results]
        avg_times: list[float] = [br.avg_time for br in sorted_results]
        median_times: list[float] = [br.median_time for br in sorted_results]
        std_devs: list[float] = [br.std_dev for br in sorted_results]

        max_value = max(
            max(avg_times) if avg_times else 0,
            max(median_times) if median_times else 0,
            max(std_devs) if std_devs else 0,
        )
        y_limit = max_value / 0.85 if max_value > 0 else 1.0

        title_text = f"{benchmark_group.type_.replace('_', ' ').title()}"
        metadata_text = (
            f"Iterations: {benchmark_group.iterations} | GC: "
            f"{'Disabled' if benchmark_group.is_gc_disabled else 'Enabled'}"
        )

        filename = f"{benchmark_group.type_}_comparison.png"
        output_path = self.output_dir / filename
        self.output_dir.mkdir(parents=True, exist_ok=True)

        dynamic_height = 600 + (len(descriptions) * 150)

        chart = pygal.HorizontalBar(
            style=self._style,
            width=3100,
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

        chart.title = f"{title_text}\n{metadata_text}"
        chart.x_title = "Time (ms)"
        chart.no_data_text = "No data"
        chart.value_formatter = lambda x: f"{x:.3f}"

        chart.x_labels = descriptions

        chart.add("Std Deviation", std_devs)
        chart.add("Average Time", avg_times)
        chart.add("Median Time", median_times)

        svg_bytes = chart.render()
        cairosvg.svg2png(bytestring=svg_bytes, write_to=str(output_path))

        return output_path
