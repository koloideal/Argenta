__all__ = ["ReleaseGenerator"]

import json
import shutil
from pathlib import Path

from ..benchmarks.core.models import BenchmarkGroupResult
from .diagram_generator import DiagramGenerator


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
            
            diagram_generator = DiagramGenerator(type_dir)
            diagram_generator.generate_comparison_diagram(benchmark_group)
            
            json_data = {
                "type": benchmark_group.type_,
                "iterations": benchmark_group.iterations,
                "gc_disabled": benchmark_group.is_gc_disabled,
                "benchmarks": [
                    {
                        "name": br.name,
                        "description": br.description,
                        "avg_time": br.avg_time,
                        "median_time": br.median_time,
                        "std_dev": br.std_dev
                    }
                    for br in benchmark_group.benchmark_results
                ]
            }
            
            json_path = type_dir / f"{benchmark_group.type_}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        return self.output_dir
