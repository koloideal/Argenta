__all__ = [
    "get_time_of_pre_cycle_setup",
    "attempts_to_average"
]

import io
from contextlib import redirect_stdout
import time
from decimal import Decimal, ROUND_HALF_UP

from argenta import App


def get_time_of_pre_cycle_setup(app: App) -> float:
    start = time.monotonic()
    with redirect_stdout(io.StringIO()):
        app._pre_cycle_setup()  # pyright: ignore[reportPrivateUsage]
    end = time.monotonic()
    return end - start


def attempts_to_average(bench_attempts: list[float], iterations: int) -> Decimal:
    return Decimal(sum(bench_attempts) / iterations).quantize(Decimal("0.00001"), rounding=ROUND_HALF_UP)
