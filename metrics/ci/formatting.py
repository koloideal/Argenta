"""Formatting helpers for benchmark comparison reports."""

import platform
from pathlib import Path

from metrics.ci.models import Comparison

_MICROSECONDS_THRESHOLD = 0.001
_MICROS_IN_SECOND = 1_000_000
_MILLIS_IN_SECOND = 1_000


def format_time(seconds: float) -> str:
    if seconds < _MICROSECONDS_THRESHOLD:
        microseconds = seconds * _MICROS_IN_SECOND
        return f"{microseconds:.2f} µs"
    if seconds < 1:
        milliseconds = seconds * _MILLIS_IN_SECOND
        return f"{milliseconds:.3f} ms"
    return f"{seconds:.3f} s"


def format_ratio(comparison: Comparison, threshold: float) -> str:
    if comparison.ratio >= threshold:
        return f"**{comparison.ratio:.2f}x** 🟢"
    if comparison.ratio <= 1 / threshold:
        return f"**{comparison.ratio:.2f}x** 🔴"
    return f"{comparison.ratio:.2f}x"


def cpu_name() -> str:
    cpuinfo_file = Path("/proc/cpuinfo")
    if cpuinfo_file.exists():
        for line in cpuinfo_file.read_text().splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    return platform.processor() or platform.machine()
