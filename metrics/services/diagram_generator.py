__all__ = ["DiagramGenerator"]

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

from ..benchmarks.core.models import BenchmarkGroupResult


class DiagramGenerator:
    def __init__(self, output_dir: Path | str) -> None:
        self.output_dir: Path = Path(output_dir) if isinstance(output_dir, str) else output_dir

        matplotlib.use('Agg')
        plt.style.use('seaborn-v0_8-whitegrid')

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
            max(std_devs) if std_devs else 0
        )
        y_limit = max_value / 0.85 if max_value > 0 else 1.0

        items_count = len(descriptions)
        x_positions: list[int] = list(range(items_count))

        bar_width = 0.25

        x_std_dev = [x - bar_width for x in x_positions]
        x_avg = [x for x in x_positions]
        x_median = [x + bar_width for x in x_positions]

        fig, ax = plt.subplots(figsize=(16, 8))
        fig.patch.set_facecolor('white')

        bars_std = ax.bar(x_std_dev, std_devs, bar_width, label='Std Deviation',
                          color='#2ecc71', alpha=0.9, edgecolor='#27ae60', linewidth=1.5)
        bars_avg = ax.bar(x_avg, avg_times, bar_width, label='Average Time',
                          color='#3498db', alpha=0.9, edgecolor='#2980b9', linewidth=1.5)
        bars_median = ax.bar(x_median, median_times, bar_width, label='Median Time',
                             color='#e74c3c', alpha=0.9, edgecolor='#c0392b', linewidth=1.5)

        for bar_group in [bars_std, bars_avg, bars_median]:
            for bar in bar_group:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.,
                    height,
                    f'{height:.3f}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold'
                )

        ax.set_ylabel('Time (ms)', fontsize=14, fontweight='bold', labelpad=10)

        title_text = f'{benchmark_group.type_.replace("_", " ").title()}'
        metadata_text = f'Iterations: {benchmark_group.iterations} | GC: {"Disabled" if benchmark_group.is_gc_disabled else "Enabled"}'

        ax.text(0.5, 1.08, title_text, transform=ax.transAxes,
                fontsize=18, fontweight='bold', ha='center', color='#2c3e50')
        ax.text(0.5, 1.03, metadata_text, transform=ax.transAxes,
                fontsize=12, ha='center', color='#7f8c8d', style='italic')

        ax.set_xticks(x_positions)
        ax.set_xticklabels([])

        for i, (pos, desc) in enumerate(zip(x_positions, descriptions)):
            text_x_pos = pos - bar_width - (bar_width / 2)
            ax.text(
                text_x_pos,
                y_limit * 0.02,
                desc,
                rotation=90, va='bottom', ha='right', fontsize=10,
                color='#2c3e50'
            )

        ax.set_ylim(0, y_limit)

        legend = ax.legend(loc='upper left', fontsize=12, framealpha=0.95,
                           edgecolor='#34495e', fancybox=True, shadow=True)
        legend.get_frame().set_facecolor('#ecf0f1')

        ax.grid(axis='y', alpha=0.4, linestyle='--', linewidth=0.8)
        ax.set_axisbelow(True)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#7f8c8d')
        ax.spines['bottom'].set_color('#7f8c8d')

        plt.tight_layout()

        filename = f"{benchmark_group.type_}_comparison.png"
        output_path = self.output_dir / filename

        self.output_dir.mkdir(parents=True, exist_ok=True)

        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close(fig)

        return output_path
