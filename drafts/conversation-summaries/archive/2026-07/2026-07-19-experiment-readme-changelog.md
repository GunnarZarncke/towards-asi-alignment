# 2026-07-19 — Experiment README + CHANGELOG refactor

## Trigger
User asked that experiment README files (especially graded-lab, the latest line)
start with a self-contained explanation of each simulation, its structure, and entry
points; version logs should move into consistent CHANGELOG files.

## Done
- Rewrote READMEs for all five in-repo experiment lines + top-level `experiments/README.md`:
  self-contained “what it is”, three-plane/package layout, quick start, entry-point tables.
- Added `CHANGELOG.md` to each line (newest-first, current `CODE_VERSION` where applicable,
  links to FINDINGS / DESIGN / PLAN docs).
- Graded-lab README trimmed from ~230 lines of GL/status prose to operational guide;
  full version trail now in `experiments/graded-lab-simulation/CHANGELOG.md` (0.1.0 → 0.41.1).

## Decisions
- README/CHANGELOG split is the repo convention going forward (`experiments/README.md` documents it).
- `DESIGN.md` pre-registration sections left unchanged (not version logs); only README-contained history moved.
- Did not stage unrelated working-tree changes (graded-lab v4 code, drafts, site sync, etc.).

## Open / next
- Optional: add `changelogPath` to `metadata/experiments.yml` and trim duplicate CODE_VERSION paragraph in graded-lab `DESIGN.md` to point at CHANGELOG.
- `site/src/data/experiments.json` may need sync if companion site should surface CHANGELOG links.

## Key paths
- `experiments/README.md` — index + convention
- `experiments/*/README.md` — per-line entry points
- `experiments/*/CHANGELOG.md` — version/phase history

## Commits
- `282d72c` Restructure experiment READMEs with self-contained intros and CHANGELOG files.
