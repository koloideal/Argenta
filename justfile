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

# Format code (Ruff)
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

# Run all checks (format, mypy, ruff, wps)
check-format: format mypy ruff wps

# ── Changelog (scriv) ─────────────────────────────────────────────────────────

# Create a new changelog fragment and open it in $EDITOR
frag:
    uv run python -c "from pathlib import Path; Path('changelog.d').mkdir(exist_ok=True)"
    uv run scriv create --add

# Collect fragments into CHANGELOG.md for release  (usage: just release 1.2.3)
release version:
    uv run scriv collect --version {{ version }} --add
