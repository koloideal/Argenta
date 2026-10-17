import json
import shutil
from pathlib import Path

from metrics.benchmarks.core.models import BenchmarkGroupResult
from metrics.services.diagram_generator import DiagramGenerator


def _dump_group_json(benchmark_group: BenchmarkGroupResult, type_dir: Path) -> None:
    json_data = {
        "type": benchmark_group.type_,
        "iterations": benchmark_group.iterations,
        "gc_disabled": benchmark_group.is_gc_disabled,
        "benchmarks": [
            {
                "name": bench_result.name,
                "description": bench_result.description,
                "avg_time": bench_result.avg_time,
                "median_time": bench_result.median_time,
                "std_dev": bench_result.std_dev,
            }
            for bench_result in benchmark_group.benchmark_results
        ],
    }
    json_path = type_dir / f"{benchmark_group.type_}.json"
    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=2, ensure_ascii=False)


class ReleaseGenerator:
    def __init__(self, lib_version: str) -> None:
        self.lib_version = lib_version
        self.output_dir = Path("metrics/reports/releases") / lib_version

    def generate_release(self, benchmark_groups: list[BenchmarkGroupResult]) -> Path:
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)

        for benchmark_group in benchmark_groups:
            type_dir = self.output_dir / benchmark_group.type_
            type_dir.mkdir(exist_ok=True)
            DiagramGenerator(type_dir).generate_comparison_diagram(benchmark_group)
            _dump_group_json(benchmark_group, type_dir)

        return self.output_dir
