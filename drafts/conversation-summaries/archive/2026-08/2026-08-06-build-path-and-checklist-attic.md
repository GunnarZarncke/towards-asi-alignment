# 2026-08-06 — Build path docs and checklist attic

## Trigger

User asked to keep rolled-out bridge-audit checklists in attic after reading-guide removal, then to clarify why site builds failed and review build-path instructions.

## Done

- Moved Phase 0–4 bridge-audit checklists to `metadata/concept-graph/attic/chapter-reading-checklists/` with attic README.
- Added build map to `docs/BUILD.md` (PDF vs site vs demos vs Lean; where `node_modules` belongs).
- Updated `AGENTS.md`, `INSTRUCTIONS.md` §11, `site/README.md`, `demos/README.md`, `CONTRIBUTING.md`.
- Gitignore stray repo-root `/node_modules/` and `/.astro/`.

## Decisions

- Checklists are editorial audit snapshots, not live generator output.
- Repo root has no `package.json`; npm only under `site/` and `demos/`.

## Open / next

- None from this session.

## Key paths

- `docs/BUILD.md`
- `metadata/concept-graph/attic/chapter-reading-checklists/`

## Commits

- `0f22a4db` Archive bridge-audit checklists and clarify build paths
