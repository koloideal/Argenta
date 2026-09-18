set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
set shell := ["bash", "-c"]

# List all available recipes
default:
    @just --list

# ── Testing ───────────────────────────────────────────────────────────────────

# Run tests via pytest
tests:
    python -m pytest tests

# Run tests with coverage report
tests-cov:
    python -m pytest --cov=argenta tests

# Run tests with coverage HTML report
tests-cov-html:
    python -m pytest --cov=argenta tests --cov-report=html

# ── Code quality ──────────────────────────────────────────────────────────────

# Format code (Ruff + isort)
format:
    python -m ruff format ./src
    python -m isort ./src

# Check types via mypy (strict)
mypy:
    python -m mypy -p argenta --strict

# Check style via wemake-python-styleguide
wps:
    python -m flake8 --format=wemake ./src

# Run Ruff linter
ruff:
    python -m ruff check ./src

# Run all checks (format, mypy, ruff, wps)
check-format: format mypy ruff wps

# ── Changelog (scriv) ─────────────────────────────────────────────────────────

# Create a new changelog fragment and open it in $EDITOR
frag:
    if (-not (Test-Path "./changelog.d")) { New-Item -ItemType Directory -Path "./changelog.d" }
    scriv create --add

# Preview collected changelog without writing anything
changelog-preview:
    scriv collect --dry-run

# Collect fragments into CHANGELOG.md for release  (usage: just release 1.2.3)
release version:
    scriv collect --version {{ version }} --add
