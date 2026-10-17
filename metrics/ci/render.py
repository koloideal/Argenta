"""Render benchmark comparison results as a GitHub-flavoured Markdown report."""

import platform
from collections import defaultdict

from metrics.ci.formatting import cpu_name, format_ratio, format_time
from metrics.ci.models import Comparison, Measurement

_PERCENT_MULTIPLIER = 100


def _group_section(type_name: str, group: list[Comparison], threshold: float) -> str:
    table_rows = [
        f"| {entry.description} | {format_time(entry.base)} "
        f"| {format_time(entry.head)} | {format_ratio(entry, threshold)} |"
        for entry in group
    ]
    return "\n".join(
        [
            f"#### `{type_name}`",
            "",
            "| Benchmark | main | this branch | main / branch |",
            "|---|--:|--:|--:|",
            *table_rows,
        ]
    )


def _measurement_section(header: str, column: str, measurements: list[Measurement]) -> str:
    table_rows = [
        f"| `{entry.type_}` — {entry.description} | {format_time(entry.seconds)} |"
        for entry in measurements
    ]
    return "\n".join([header, "", f"| Benchmark | {column} |", "|---|--:|", *table_rows])


def _set_changes_section(added: list[Measurement], removed: list[Measurement]) -> str:
    sections = []
    if added:
        sections.append(_measurement_section("#### 🆕 Added benchmarks", "this branch", added))
    if removed:
        sections.append(_measurement_section("#### 🗑 Removed benchmarks", "main", removed))
    return "\n\n".join(sections)


def _group_sections(comparisons: list[Comparison], threshold: float) -> list[str]:
    groups: defaultdict[str, list[Comparison]] = defaultdict(list)
    for comparison in comparisons:
        groups[comparison.type_].append(comparison)
    return [_group_section(type_name, group, threshold) for type_name, group in groups.items()]


def _summary_line(
    comparisons: list[Comparison],
    added: list[Measurement],
    removed: list[Measurement],
    threshold: float,
) -> str:
    faster = sum(entry.ratio >= threshold for entry in comparisons)
    slower = sum(entry.ratio <= 1 / threshold for entry in comparisons)
    noise_percent = round((threshold - 1) * _PERCENT_MULTIPLIER)
    set_summary = ""
    if added or removed:
        set_summary = f" · {len(added)} added · {len(removed)} removed"
    counters = f"🟢 {faster} faster · 🔴 {slower} slower · {len(comparisons)} benchmarks compared"
    return f"{counters}{set_summary} · changes within ±{noise_percent}% are treated as noise"


def _footer_line(rounds: int) -> str:
    runner = (
        f"{cpu_name()} · {platform.python_implementation()} {platform.python_version()} · "
        f"{platform.system()} {platform.release()}"
    )
    note = (
        "Absolute times are specific to this runner: compare columns within "
        "this report only. `main / branch` > 1 means this branch is faster."
    )
    return f"<sub>Runner: {runner} · {rounds} balanced rounds, median of per-run best. {note}</sub>"


def render(
    comparisons: list[Comparison],
    added: list[Measurement],
    removed: list[Measurement],
    *,
    threshold: float,
    rounds: int,
) -> str:
    sections = _group_sections(comparisons, threshold)
    set_changes = _set_changes_section(added, removed)
    if set_changes:
        sections.append(set_changes)

    summary = _summary_line(comparisons, added, removed, threshold)
    body = "\n\n".join(sections)
    footer = _footer_line(rounds)
    return f"### ⚡ Benchmarks: `main` vs this branch\n\n{summary}\n\n{body}\n\n{footer}\n"
