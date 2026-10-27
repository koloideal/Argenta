# Argenta

## Code style hard rules

- Never use `from __future__ import annotations` — quote forward references instead.
- No `Any`, no `TYPE_CHECKING`; imports stay at module top level (lazy import only
  inside a function when it guards an optional dependency).

## Agent skills

### Issue tracker

Issues live as GitHub issues in `koloideal/Argenta` (uses the `gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical labels used as-is: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context — one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
