# 2026-07-06 — Repo structure cleanup

## Trigger
User asked for folder-structure review follow-through: fix `.gitignore`, sync documentation, consolidate epigraph research, move Lean implementation brief, rename `src/` → `demos/`.

## Done
- **`.gitignore`:** added `.venv-test/` and `experiments/toy-simulation/logs/`; untracked 22 committed toy-sim log files via `git rm --cached`.
- **Docs synced:** `AGENTS.md` (all four experiment lines + `site/`, `review/`, `docs/` in layout); `CONTRIBUTING.md` and `experiments/README.md` (goal-agent + lab-simulation); Lean brief path updates in `docs/BUILD.md`, `formal/README.md`, `metadata/source-canon.md`, `Core.lean`.
- **Epigraph:** consolidated 270 rows from `epigraph-data.json` into single lookup `drafts/epigraph-candidates.md` (45 chapters, sorted Ch1…Ch48 with Ch39b handling); removed 11 `epigraph-research-*.md`, both dated candidate tables, and `epigraph-data.json`.
- **Lean brief:** `git mv` to `formal/LeanProofSpineImplementationBrief.md`.
- **`src/` → `demos/`:** renamed root folder, flattened `demos/demos/chNN-*` to `demos/chNN-*`; updated `serve.py`, `build-demos.mjs`, `serve-demos.sh`, `scripts/demo-backends.sh`, site sync/publish scripts, CI workflow, GitHub links in site pages; standalone URLs now `/chNN-slug/` not `/demos/chNN-slug/`. Demo vitest: 10 passed.

## Decisions
- Kept historical conversation logs mentioning `src/` unchanged (intentional record).
- Site `src/data/demos.json` is gitignored; regenerated via `node site/scripts/sync-demos.mjs` (filters `ch*` dirs only after flatten).

## Open / next
- None required. Optional: `./clean.sh` for local LaTeX root clutter (not in this session).

## Key paths
- `demos/` — chapter demo root (was `src/`)
- `drafts/epigraph-candidates.md` — epigraph lookup
- `formal/LeanProofSpineImplementationBrief.md`

## Commits
- `11fe166` — Rename src/ to demos/ and tidy repo layout for clearer navigation.
