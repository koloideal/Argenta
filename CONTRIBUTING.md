# Contributing to Argenta

First off, thanks for taking the time to contribute! ❤️

The full contributor guide lives in the documentation:
**[Contributing to the Project](https://argenta.wiki/latest/root/contributing.html)**

It covers the development environment setup, the issue triage pipeline, what CI checks run on every pull request, the repository layout, and the commit message styleguide.

Quick reference:

```bash
uv sync             # create .venv and install all dev dependencies from uv.lock
just tests-cov      # run the test suite — 100% coverage is required
just check-format   # ruff + mypy --strict + wemake-python-styleguide (read-only)
just frag           # changelog fragment — required if you touch src/
just docs-live      # live-reload docs preview on 127.0.0.1:8000
```

Before starting on anything non-trivial, please open an [issue](https://github.com/koloideal/Argenta/issues/new/choose) — it keeps effort from being duplicated.
