"""Time every registered benchmark once against the installed ``argenta``.

Prints a JSON list of ``Measurement`` objects to stdout. Each value is the
best per-call time out of several equally sized batches (GC disabled).
"""

import argparse
import io
import json
import sys
import timeit
from contextlib import redirect_stdout
from dataclasses import asdict

from metrics.benchmarks.core.models import FuncForBenchmark
from metrics.benchmarks.entity import benchmarks
from metrics.ci.models import Measurement

_DEFAULT_BATCH_SECONDS = 0.02


def time_per_call(func: FuncForBenchmark, *, batch_seconds: float, repeats: int) -> float:
    timer = timeit.Timer(func)
    loops = max(1, int(batch_seconds / timer.timeit(number=1)))
    timer.timeit(number=loops)
    return min(timer.repeat(repeat=repeats, number=loops)) / loops


def measure_all(*, batch_seconds: float, repeats: int) -> list[Measurement]:
    with redirect_stdout(io.StringIO()):
        return [
            Measurement(
                name=bench.name,
                type_=bench.type_,
                description=bench.description,
                seconds=time_per_call(bench.func, batch_seconds=batch_seconds, repeats=repeats),
            )
            for bench in benchmarks.get_all_benchmarks()
        ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-seconds", type=float, default=_DEFAULT_BATCH_SECONDS)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()

    measurements = measure_all(batch_seconds=args.batch_seconds, repeats=args.repeats)
    json.dump([asdict(measurement) for measurement in measurements], sys.stdout)


if __name__ == "__main__":
    main()
