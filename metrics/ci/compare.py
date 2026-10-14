"""Compare benchmarks of two ``argenta`` installations and render a Markdown report.

Runs ``metrics.ci.measure`` under both interpreters on the same machine in
balanced rounds (base, head, head, base), takes the median of the per-run
best times and writes a GitHub-flavoured Markdown table.
"""

import argparse
import json
import platform
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from metrics.ci.models import Comparison, Measurement


def run_measure(python: str, measure_args: list[str]) -> list[Measurement]:
    completed = subprocess.run(
        [python, "-m", "metrics.ci.measure", *measure_args],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    return [Measurement(**item) for item in json.loads(completed.stdout)]


def medians(runs: list[list[Measurement]]) -> dict[str, float]:
    samples: defaultdict[str, list[float]] = defaultdict(list)
    for run in runs:
        for measurement in run:
            samples[measurement.name].append(measurement.seconds)
    return {name: statistics.median(values) for name, values in samples.items()}


def collect(
    base_python: str, head_python: str, *, rounds: int, measure_args: list[str]
) -> list[Comparison]:
    base_runs: list[list[Measurement]] = []
    head_runs: list[list[Measurement]] = []
    for _ in range(rounds):
        base_runs.append(run_measure(base_python, measure_args))
        head_runs.append(run_measure(head_python, measure_args))
        head_runs.append(run_measure(head_python, measure_args))
        base_runs.append(run_measure(base_python, measure_args))

    base, head = medians(base_runs), medians(head_runs)
    return [
        Comparison(
            type_=measurement.type_,
            description=measurement.description,
            base=base[measurement.name],
            head=head[measurement.name],
        )
        for measurement in base_runs[0]
    ]


def format_time(seconds: float) -> str:
    if seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    if seconds < 1:
        return f"{seconds * 1e3:.3f} ms"
    return f"{seconds:.3f} s"


def format_ratio(comparison: Comparison, threshold: float) -> str:
    if comparison.ratio >= threshold:
        return f"**{comparison.ratio:.2f}x** 🟢"
    if comparison.ratio <= 1 / threshold:
        return f"**{comparison.ratio:.2f}x** 🔴"
    return f"{comparison.ratio:.2f}x"


def cpu_name() -> str:
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text().splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    return platform.processor() or platform.machine()


def render(comparisons: list[Comparison], *, threshold: float, rounds: int) -> str:
    groups: defaultdict[str, list[Comparison]] = defaultdict(list)
    for comparison in comparisons:
        groups[comparison.type_].append(comparison)

    sections = [
        "\n".join(
            [
                f"#### `{type_}`",
                "",
                "| Benchmark | main | this branch | main / branch |",
                "|---|--:|--:|--:|",
                *(
                    f"| {item.description} | {format_time(item.base)} "
                    f"| {format_time(item.head)} | {format_ratio(item, threshold)} |"
                    for item in group
                ),
            ]
        )
        for type_, group in groups.items()
    ]

    faster = sum(item.ratio >= threshold for item in comparisons)
    slower = sum(item.ratio <= 1 / threshold for item in comparisons)
    noise_percent = round((threshold - 1) * 100)
    summary = (
        f"🟢 {faster} faster · 🔴 {slower} slower · {len(comparisons)} benchmarks"
        f" · changes within ±{noise_percent}% are treated as noise"
    )
    footer = (
        f"<sub>Runner: {cpu_name()} · {platform.python_implementation()} "
        f"{platform.python_version()} · {platform.system()} {platform.release()} · "
        f"{rounds} balanced rounds, median of per-run best. "
        "Absolute times are specific to this runner: compare columns within "
        "this report only. `main / branch` > 1 means this branch is faster.</sub>"
    )
    body = "\n\n".join(sections)
    return f"### ⚡ Benchmarks: `main` vs this branch\n\n{summary}\n\n{body}\n\n{footer}\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-python", required=True)
    parser.add_argument("--head-python", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--threshold", type=float, default=1.10)
    parser.add_argument("--batch-seconds", type=float, default=0.02)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()

    comparisons = collect(
        args.base_python,
        args.head_python,
        rounds=args.rounds,
        measure_args=["--batch-seconds", str(args.batch_seconds), "--repeats", str(args.repeats)],
    )
    report = render(comparisons, threshold=args.threshold, rounds=args.rounds)
    args.output.write_text(report, encoding="utf-8")
    sys.stdout.write(report)


if __name__ == "__main__":
    main()
