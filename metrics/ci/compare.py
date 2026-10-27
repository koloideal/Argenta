"""Compare benchmarks of two ``argenta`` installations and render a Markdown report.

Runs ``metrics.ci.measure`` under both interpreters on the same machine in
balanced rounds (base, head, head, base), takes the median of the per-run
best times and writes a GitHub-flavoured Markdown table.
"""

import argparse
import json
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from metrics.ci.models import Comparison, Measurement, Side
from metrics.ci.render import render

_DEFAULT_THRESHOLD = 1.1
_DEFAULT_BATCH_SECONDS = 0.02

RunSet = list[list[Measurement]]


def run_measure(side: Side, measure_args: list[str]) -> list[Measurement]:
    try:
        completed = subprocess.run(
            [side.python, "-m", "metrics.ci.measure", *measure_args],
            capture_output=True,
            text=True,
            check=True,
            cwd=side.directory,
        )
    except subprocess.CalledProcessError as error:
        # surface the child traceback instead of a bare CalledProcessError
        sys.stderr.write(error.stderr)
        raise
    return [Measurement(**entry) for entry in json.loads(completed.stdout)]


def medians(runs: RunSet) -> dict[str, float]:
    samples: defaultdict[str, list[float]] = defaultdict(list)
    for run in runs:
        for measurement in run:
            samples[measurement.name].append(measurement.seconds)
    return {name: statistics.median(timings) for name, timings in samples.items()}


def _all_rounds(
    base: Side, head: Side, rounds: int, measure_args: list[str]
) -> tuple[RunSet, RunSet]:
    base_runs: RunSet = []
    head_runs: RunSet = []
    for _ in range(rounds):
        base_runs.append(run_measure(base, measure_args))
        head_runs.append(run_measure(head, measure_args))
        head_runs.append(run_measure(head, measure_args))
        base_runs.append(run_measure(base, measure_args))
    return base_runs, head_runs


def _set_diffs(base_runs: RunSet, head_runs: RunSet) -> tuple[list[Measurement], list[Measurement]]:
    head_names = {measurement.name for measurement in head_runs[0]}
    base_names = {measurement.name for measurement in base_runs[0]}
    added = [measurement for measurement in head_runs[0] if measurement.name not in base_names]
    removed = [measurement for measurement in base_runs[0] if measurement.name not in head_names]
    return added, removed


def collect(
    base: Side,
    head: Side,
    *,
    rounds: int,
    measure_args: list[str],
) -> tuple[list[Comparison], list[Measurement], list[Measurement]]:
    # each side measures with the benchmark code from its own checkout —
    # the PR's metrics may reference argenta APIs the base tree lacks
    base_runs, head_runs = _all_rounds(base, head, rounds, measure_args)
    base_medians, head_medians = medians(base_runs), medians(head_runs)
    comparisons = [
        Comparison(
            type_=measurement.type_,
            description=measurement.description,
            base=base_medians[measurement.name],
            head=head_medians[measurement.name],
        )
        for measurement in base_runs[0]
        if measurement.name in head_medians
    ]
    return comparisons, *_set_diffs(base_runs, head_runs)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-python", required=True)
    parser.add_argument("--head-python", required=True)
    parser.add_argument("--base-dir", required=True, help="base source checkout dir")
    parser.add_argument("--head-dir", required=True, help="head source checkout dir")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--threshold", type=float, default=_DEFAULT_THRESHOLD)
    parser.add_argument("--batch-seconds", type=float, default=_DEFAULT_BATCH_SECONDS)
    parser.add_argument("--repeats", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    report = render(
        *collect(
            Side.from_cli(args.base_python, args.base_dir),
            Side.from_cli(args.head_python, args.head_dir),
            rounds=args.rounds,
            measure_args=[
                "--batch-seconds",
                str(args.batch_seconds),
                "--repeats",
                str(args.repeats),
            ],
        ),
        threshold=args.threshold,
        rounds=args.rounds,
    )
    args.output.write_text(report, encoding="utf-8")
    sys.stdout.write(report)


if __name__ == "__main__":
    main()
