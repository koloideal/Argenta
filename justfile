set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
set shell := ["bash", "-c"]

# List all available recipes
default:
    @just --list

# ── Testing ───────────────────────────────────────────────────────────────────

# Run tests via pytest
tests:
    uv run python -m pytest tests

# Run tests with coverage report
tests-cov:
    uv run python -m pytest --cov=argenta tests

# Run tests with coverage HTML report
tests-cov-html:
    uv run python -m pytest --cov=argenta tests --cov-report=html

# ── Code quality ──────────────────────────────────────────────────────────────

# Format code and fix imports (Ruff) — modifies files
format:
    uv run python -m ruff format ./src ./tests ./metrics ./examples
    uv run python -m ruff check --select I --fix ./src ./tests ./metrics ./examples

# Check types via mypy (strict for src, default for the rest)
mypy:
    uv run python -m mypy -p argenta --strict
    uv run python -m mypy tests metrics examples

# Check style via wemake-python-styleguide
wps:
    uv run python -m flake8 --format=wemake ./src ./tests ./metrics ./examples

# Run Ruff linter
ruff:
    uv run python -m ruff check ./src ./tests ./metrics ./examples

# Verify formatting without changing files
format-check:
    uv run python -m ruff format --check ./src ./tests ./metrics ./examples
    uv run python -m ruff check --select I ./src ./tests ./metrics ./examples

# Run all checks (format-check, mypy, ruff, wps) — never modifies files
check-format: format-check mypy ruff wps

# ── Documentation (Sphinx) ────────────────────────────────────────────────────

# Build the documentation (fails on warnings, like CI)
docs-build:
    uv run sphinx-build -b html -W docs docs/_build

# Live-reload documentation preview on 127.0.0.1:8000
docs-live:
    uv run sphinx-autobuild -b html docs docs/_build/html

# ── Fuzzing (atheris) ─────────────────────────────────────────────────────────

# Fuzz InputCommand.parse for N seconds (usage: just fuzz 300)
fuzz seconds="60":
    mkdir -p fuzz/corpus fuzz/artifacts
    uv run --group fuzz python fuzz/parse_fuzzer.py fuzz/corpus -artifact_prefix=fuzz/artifacts/ -max_total_time={{ seconds }}

# Quick smoke run of the fuzzer (1000 iterations)
fuzz-smoke:
    mkdir -p fuzz/corpus fuzz/artifacts
    uv run --group fuzz python fuzz/parse_fuzzer.py fuzz/corpus -artifact_prefix=fuzz/artifacts/ -runs=1000

# ── Changelog (scriv) ─────────────────────────────────────────────────────────

# Create a new changelog fragment and open it in $EDITOR
frag:
    uv run python -c "from pathlib import Path; Path('changelog.d').mkdir(exist_ok=True)"
    uv run scriv create --add

# Collect fragments into CHANGELOG.md for release  (usage: just release 1.2.3)
release version:
    uv run scriv collect --version {{ version }} --add
