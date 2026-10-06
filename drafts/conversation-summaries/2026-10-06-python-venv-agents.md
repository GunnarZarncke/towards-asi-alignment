# 2026-10-06 — Python venv for agents

kind: housekeeping
uptake: rule

## Trigger
Agents keep failing on PyYAML because they run bare `python3` instead of the repo `.venv/`.

## Done
- housekeeping: Added `requirements.txt` (PyYAML) and `scripts/resolve_python.sh` (prefer `.venv/bin/python`, print setup hint on failure).
- housekeeping: Wired resolver into `scripts/generate_manuscript_tex.sh`, `scripts/check.sh`, `Makefile` wordcount/bookstats/todos, and `serve-site.sh` (prepends `.venv/bin` to `PATH`).
- housekeeping: `site/scripts/sync-chapter-reading-graph.mjs` prefers `.venv/bin/python`.
- rule: Documented in `AGENTS.md` (Build scripts) and `docs/BUILD.md` (Python virtualenv section); `requirements-dev.txt` includes `-r requirements.txt`.

## Decisions
- Auto-resolve in wrapper scripts rather than requiring manual `source .venv/bin/activate` for `./build.sh`, `make check`, and `./serve-site.sh`.
- Direct ad-hoc script invocations still documented as `.venv/bin/python scripts/foo.py`.

## Open / next
- CI (`.github/workflows/check.yml`) still relies on Ubuntu system `python3`; add explicit PyYAML install if that ever breaks.

## Key paths
- `scripts/resolve_python.sh`
- `requirements.txt`
- `AGENTS.md` (Build scripts → Python)
- `docs/BUILD.md` (Python virtualenv)

## Verification
- `./scripts/resolve_python.sh` → `.venv/bin/python`
- `make wordcount` → exit 0

## Commits
- (this session)
