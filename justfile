set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
set shell := ["bash", "-c"]

# List all available recipes
default:
    @just --list

# ── Testing ───────────────────────────────────────────────────────────────────

# Run tests via pytest
tests:
    uv run pytest tests

# Run tests with coverage report
tests-cov:
    uv run pytest --cov=argenta tests

# Run tests with coverage HTML report
tests-cov-html:
    uv run pytest --cov=argenta tests --cov-report=html

# Regenerate Syrupy snapshots after intentional output changes
snapshot-update:
    uv run pytest tests --snapshot-update

# ── Code quality ──────────────────────────────────────────────────────────────

# Format code and fix imports (Ruff) — modifies files
format:
    uv run ruff format ./src ./tests ./metrics ./examples ./repl_framed ./repl_compact ./dual_runtime ./script_runtime
    uv run ruff check --select I --fix ./src ./tests ./metrics ./examples ./repl_framed ./repl_compact ./dual_runtime ./script_runtime

# Check types via mypy (strict for src, default for the rest)
mypy:
    uv run mypy -p argenta --strict
    uv run mypy tests metrics examples repl_framed repl_compact dual_runtime script_runtime

# Check style via wemake-python-styleguide
wps:
    uv run flake8 --format=wemake ./src ./tests ./metrics ./examples ./repl_framed ./repl_compact ./dual_runtime ./script_runtime

# Run Ruff linter
ruff:
    uv run ruff check ./src ./tests ./metrics ./examples ./repl_framed ./repl_compact ./dual_runtime ./script_runtime

# Verify formatting without changing files
format-check:
    uv run ruff format --check ./src ./tests ./metrics ./examples ./repl_framed ./repl_compact ./dual_runtime ./script_runtime
    uv run ruff check --select I ./src ./tests ./metrics ./examples ./repl_framed ./repl_compact ./dual_runtime ./script_runtime

# Run all checks (format-check, mypy, ruff, wps) — never modifies files
check-format: format-check mypy ruff wps

# Run everything CI gates on — green here means green in the PR
ci-check: tests-cov check-format docs-build

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
    uv run python -c "from pathlib import Path; Path('fuzz/corpus').mkdir(parents=True, exist_ok=True); Path('fuzz/artifacts').mkdir(parents=True, exist_ok=True)"
    uv run --group fuzz python fuzz/parse_fuzzer.py fuzz/corpus -artifact_prefix=fuzz/artifacts/ -max_total_time={{ seconds }}

# Quick smoke run of the fuzzer (1000 iterations)
fuzz-smoke:
    uv run python -c "from pathlib import Path; Path('fuzz/corpus').mkdir(parents=True, exist_ok=True); Path('fuzz/artifacts').mkdir(parents=True, exist_ok=True)"
    uv run --group fuzz python fuzz/parse_fuzzer.py fuzz/corpus -artifact_prefix=fuzz/artifacts/ -runs=1000

# ── Font assets ───────────────────────────────────────────────────────────────

# Recompile bundled .flf fonts into .flfd dumps (run after editing _fonts/*.flf)
fonts-compile:
    uv run argenta fonts compile src/argenta/app/presentation/ascii_art/_fonts/tarty1.flf
    uv run argenta fonts compile src/argenta/app/presentation/ascii_art/_fonts/chunky.flf

# ── Changelog (scriv) ─────────────────────────────────────────────────────────

# Create a new changelog fragment and open it in $EDITOR
frag:
    uv run python -c "from pathlib import Path; Path('changelog.d').mkdir(exist_ok=True)"
    uv run scriv create --add

# Collect fragments into CHANGELOG.md for release  (usage: just release 1.2.3)
release version:
    uv run scriv collect --version {{ version }} --add

# ── A2UI example ──────────────────────────────────────────────────────────────

# Run the A2UI example agent (default sse; -t ws/socket/stdio/grpc to switch)
a2ui-example-agent:
    uv run --extra a2ui argenta example a2ui agent

# Serve the A2UI Lit browser client on http://127.0.0.1:8080
a2ui-example-client:
    uv run --extra a2ui argenta example a2ui client

# Run the terminal gRPC client against the agent started with -t grpc
a2ui-example-grpc-client:
    uv run --extra a2ui argenta example a2ui client grpc
